"""Automatic GNUmed audit trail generation.

This module creates SQL DDL commands for the audit
trail triggers and functions to be created in the schema "audit".

Theory of operation:

Any table that needs to be audited (all modifications
logged) must be recorded in the table "audit.audited_tables".

This script creates the triggers, functions and tables
neccessary to establish the audit trail. Some or all
audit trail tables may have been created previously but
need not contain all columns of the audited table. Do not
put any constraints on the audit trail tables except for
"not null" on those columns that cannot be null in the
audited table.
"""
#==================================================================
# $Source: /home/ncq/Projekte/cvs2git/vcs-mirror/gnumed/gnumed/server/bootstrap/gmAuditSchemaGenerator.py,v $
__version__ = "$Revision: 1.30 $"
__author__ = "Horst Herb, Karsten.Hilbert@gmx.net"
__license__ = "GPL"		# (details at http://www.gnu.org)

import sys, os.path, string


from Gnumed.pycommon import gmLog, gmPG2


_log = gmLog.gmDefLog
if __name__ == "__main__" :
	_log.SetAllLogLevels(gmLog.lData)
_log.Log(gmLog.lInfo, __version__)

# the audit trail tables start with this prefix
audit_trail_table_prefix = u'log_'
# and inherit from this table
audit_trail_parent_table = u'audit_trail'
# audited tables inherit these fields
audit_fields_table = u'audit_fields'
# audit stuff lives in this schema
audit_schema = u'audit'

#==================================================================
# SQL statements for auditing setup script
#------------------------------------------------------------------
# audit triggers are named "zt_*_*" to make
# reasonably sure they are executed last

# insert
tmpl_insert_trigger = """CREATE TRIGGER zt_ins_%s
	BEFORE INSERT ON %s.%s
	FOR EACH ROW EXECUTE PROCEDURE audit.ft_ins_%s()"""

tmpl_insert_function = """
\unset ON_ERROR_STOP
drop function audit.ft_ins_%s() cascade;
\set ON_ERROR_STOP 1

create FUNCTION audit.ft_ins_%s()
	RETURNS trigger
	LANGUAGE 'plpgsql'
	SECURITY DEFINER
	AS '
BEGIN
	NEW.row_version := 0;
	NEW.modified_when := CURRENT_TIMESTAMP;
	NEW.modified_by := SESSION_USER;
	return NEW;
END;'"""

# update
tmpl_update_trigger = """CREATE TRIGGER zt_upd_%s
	BEFORE UPDATE ON %s.%s
	FOR EACH ROW EXECUTE PROCEDURE audit.ft_upd_%s()"""

tmpl_update_function = """
\unset ON_ERROR_STOP
drop function audit.ft_upd_%s() cascade;
\set ON_ERROR_STOP 1

create FUNCTION audit.ft_upd_%s()
	RETURNS trigger
	LANGUAGE 'plpgsql'
	SECURITY DEFINER
	AS '
BEGIN
	NEW.row_version := OLD.row_version + 1;
	NEW.modified_when := CURRENT_TIMESTAMP;
	NEW.modified_by := SESSION_USER;
	INSERT INTO audit.%s (
		orig_version, orig_when, orig_by, orig_tableoid, audit_action,
		%s
	) VALUES (
		OLD.row_version, OLD.modified_when, OLD.modified_by, TG_RELID, TG_OP,
		%s
	);
	return NEW;
END;'"""

# delete
tmpl_delete_trigger = """
CREATE TRIGGER zt_del_%s
	BEFORE DELETE ON %s.%s
	FOR EACH ROW EXECUTE PROCEDURE audit.ft_del_%s()"""

tmpl_delete_function = """
\unset ON_ERROR_STOP
drop function audit.ft_del_%s() cascade;
\set ON_ERROR_STOP 1

create FUNCTION audit.ft_del_%s()
	RETURNS trigger
	LANGUAGE 'plpgsql'
	SECURITY DEFINER
	AS '
BEGIN
	INSERT INTO audit.%s (
		orig_version, orig_when, orig_by, orig_tableoid, audit_action,
		%s
	) VALUES (
		OLD.row_version, OLD.modified_when, OLD.modified_by, TG_RELID, TG_OP,
		%s
	);
	return OLD;
END;'"""

tmpl_create_audit_trail_table = """
create table audit.%s (
%s
) inherits (%s);"""

#grant insert on %s.%s to group "gm-public"

#------------------------------------------------------------------
#------------------------------------------------------------------
def audit_trail_table_ddl(aCursor=None, schema='audit', table2audit=None):

	audit_trail_table = '%s%s' % (audit_trail_table_prefix, table2audit)

	# which columns to potentially audit
	cols2potentially_audit = gmPG2.get_col_defs(link_obj = aCursor, schema = schema, table = table2audit)
	# which to skip
	cols2skip = gmPG2.get_col_names(link_obj = aCursor, schema = audit_schema, table = audit_fields_table)
	# which ones to really audit
	cols2really_audit = []
	for col in cols2potentially_audit[0]:
		if col in cols2skip:
			continue
		cols2really_audit.append("\t%s %s" % (col, cols2potentially_audit[1][col]))

	# does the audit trail target table exist ?
	exists = gmPG2.table_exists(aCursor, 'audit', audit_trail_table)
	if exists is None:
		_log.Log(gmLog.lErr, 'cannot check existance of table [audit.%s]' % audit_trail_table)
		return None
	if exists:
		_log.Log(gmLog.lInfo, 'audit trail table [audit.%s] already exists' % audit_trail_table)
		# sanity check table structure
		currently_audited_cols = gmPG2.get_col_defs(link_obj = aCursor, schema = u'audit', table = audit_trail_table)
		currently_audited_cols = [ '\t%s %s' % (c, currently_audited_cols[1][c]) for c in currently_audited_cols[0] ]
		for col in cols2really_audit:
			try:
				currently_audited_cols.index(col)
			except ValueError:
				_log.Log(gmLog.lErr, 'table structure incompatible: column [%s] not found in audit table' % col)
				_log.Log(gmLog.lErr, '%s.%s:' % (schema, table2audit))
				_log.Log(gmLog.lErr, '%s' % ','.join(cols2really_audit))
				_log.Log(gmLog.lErr, '%s.%s:' % (audit_schema, audit_trail_table))
				_log.Log(gmLog.lErr, '%s' % ','.join(currently_audited_cols))
				return None
#			if len(currently_audited_cols) != len(cols2really_audit):
#				_log.Log(gmLog.lErr, 'table structure incompatible:')
#				_log.Log(gmLog.lErr, '%s.%s:' % (schema, table2audit))
#				_log.Log(gmLog.lErr, ' %s' % ', '.join(cols2really_audit))
#				_log.Log(gmLog.lErr, '%s.%s:' % (audit_schema, audit_trail_table))
#				_log.Log(gmLog.lErr, ' %s' % ', '.join(currently_audited_cols))
#				return None
		return []

	# must create audit trail table
	_log.Log(gmLog.lInfo, 'no audit trail table found for [%s.%s]' % (schema, table2audit))
	_log.Log(gmLog.lInfo, 'creating audit trail table [audit.%s]' % audit_trail_table)

	# create audit table DDL
	attributes = ',\n'.join(cols2really_audit)
	table_def = tmpl_create_audit_trail_table % (
		audit_trail_table,
		attributes,
		audit_trail_parent_table			# FIXME: use audit_schema
	)
	return [table_def, '']
#------------------------------------------------------------------
def trigger_ddl(aCursor='default', schema='audit', audited_table=None):
	audit_trail_table = '%s%s' % (audit_trail_table_prefix, audited_table)

	target_columns = gmPG2.get_col_names(link_obj = aCursor, schema = schema, table = audited_table)
	columns2skip = gmPG2.get_col_names(link_obj = aCursor, schema = audit_schema, table =  audit_fields_table)
	columns = []
	values = []
	for column in target_columns:
		if column not in columns2skip:
			columns.append(column)
			values.append('OLD.%s' % column)
	columns_clause = string.join(columns, ', ')
	values_clause = string.join(values, ', ')

	ddl = []

	# insert
	ddl.append(tmpl_insert_function % (audited_table, audited_table))
	ddl.append('')
	ddl.append(tmpl_insert_trigger % (audited_table, schema, audited_table, audited_table))
	ddl.append('')

	# update
	ddl.append(tmpl_update_function % (audited_table, audited_table, audit_trail_table, columns_clause, values_clause))
	ddl.append('')
	ddl.append(tmpl_update_trigger % (audited_table, schema, audited_table, audited_table))
	ddl.append('')

	# delete
	ddl.append(tmpl_delete_function % (audited_table, audited_table, audit_trail_table, columns_clause, values_clause))
	ddl.append('')
	ddl.append(tmpl_delete_trigger % (audited_table, schema, audited_table, audited_table))
	ddl.append('')

	# disallow delete/update on auditing table

	return ddl
#------------------------------------------------------------------
def create_audit_ddl(aCursor):
	# get list of all marked tables
	cmd = u"select schema, table_name from audit.audited_tables"
	rows, idx = gmPG2.run_ro_queries(link_obj=aCursor, queries = [{'cmd': cmd}])
	if len(rows) == 0:
		_log.Log(gmLog.lInfo, 'no tables to audit')
		return None
	_log.Log(gmLog.lData, rows)
	# for each marked table
	ddl = []
	for row in rows:
		audit_trail_ddl = audit_trail_table_ddl(aCursor=aCursor, schema=row['schema'], table2audit=row['table_name'])
		if audit_trail_ddl is None:
			_log.Log(gmLog.lErr, 'cannot generate audit trail DDL for audited table [%s]' % row['table_name'])
			return None
		ddl.extend(audit_trail_ddl)
		if len(audit_trail_ddl) != 0:
			ddl.append('-- ----------------------------------------------')
		# create corresponding triggers
		ddl.extend(trigger_ddl(aCursor = aCursor, schema = row['schema'], audited_table = row['table_name']))
		ddl.append('-- ----------------------------------------------')
	return ddl
#==================================================================
# main
#------------------------------------------------------------------
if __name__ == "__main__" :
	tmp = ''
	try:
		tmp = raw_input("audit trail parent table [%s]: " % audit_trail_parent_table)
	except KeyboardError:
		pass
	if tmp != '':
		audit_trail_parent_table = tmp

	conn = gmPG2.get_connection(readonly=False, pooled=False)
	curs = conn.cursor()

	schema = create_audit_ddl(curs)

	curs.close()
	conn.close()

	if schema is None:
		print "error creating schema"
		sys.exit(-1)

	file = open ('audit-trail-schema.sql', 'wb')
	for line in schema:
		file.write("%s;\n" % line)
	file.close()
#==================================================================
# $Log: gmAuditSchemaGenerator.py,v $
# Revision 1.30  2007-12-09 20:45:45  ncq
# - a bit of cleanup
# - when we detect a pre-existing audit log table we better check
#   its structure - and bingo, a mismatch is found right away
#
# Revision 1.29  2006/12/18 17:38:19  ncq
# - u''ify 2 queries
#
# Revision 1.28  2006/12/06 16:11:08  ncq
# - port to gmPG2
#
# Revision 1.27  2006/11/14 23:27:56  ncq
# - explicitely (cascade) drop audit trigger functions so we can
#   change return type from opaque to trigger
# - make sure audit tables are created in "audit."
#
# Revision 1.26  2006/05/24 12:10:46  ncq
# - use session_user
#
# Revision 1.25  2006/01/05 16:07:11  ncq
# - generate audit trail tables and functions in schema "audit"
# - adjust configuration
# - audit trigger functions now "security definer" (== gm-dbo)
# - grant SELECT only to non-gm-dbo users
# - return language_handler not opaque from language call handler functions
#
# Revision 1.24  2005/12/04 09:34:44  ncq
# - make fit for schema support
# - move some queries to gmPG
# - improve DDL templates (use or replace on functions)
#
# Revision 1.23  2005/09/13 11:51:06  ncq
# - use "drop function ... cascade;"
#
# Revision 1.22  2004/07/17 21:23:49  ncq
# - run_query now has verbosity argument, so use it
#
# Revision 1.21  2004/06/28 13:31:17  ncq
# - really fix imports, now works again
#
# Revision 1.20  2004/06/28 13:23:20  ncq
# - fix import statements
#
# Revision 1.19  2003/11/05 16:03:02  ncq
# - allow gm-public to insert into log tables
#
# Revision 1.18  2003/10/25 16:58:40  ncq
# - fix audit trigger function generation omitting target column names
#
# Revision 1.17  2003/10/19 12:56:27  ncq
# - streamline
#
# Revision 1.16  2003/10/01 15:43:45  ncq
# - use table audited_tables now instead of inheriting from audit_mark
#
# Revision 1.15  2003/08/17 00:09:37  ncq
# - add auto-generation of missing audit trail tables
# - use that
#
# Revision 1.14  2003/07/05 13:45:49  ncq
# - modify -> modified
#
# Revision 1.13  2003/07/05 12:53:29  ncq
# - actually use ";"s correctly (verified)
#
# Revision 1.12  2003/07/05 12:29:57  ncq
# - just a bit of cleanup
#
# Revision 1.11  2003/07/05 12:26:01  ncq
# - need ; at end of chained SQL statements !
#
# Revision 1.10  2003/06/29 12:41:34  ncq
# - remove excessive quoting
# - check fail of get_children
# - check for audit_mark/audit_fields split compliance
#
# Revision 1.9  2003/06/26 21:44:25  ncq
# - %s; quoting bug, cursor(cmd, args) style
#
# Revision 1.8  2003/06/03 13:48:19  ncq
# - clarify log message
#
# Revision 1.7  2003/05/22 12:54:48  ncq
# - update comments
# - make audit prefix configurable
#
# Revision 1.6  2003/05/17 18:43:24  ncq
# - make triggers zt* so other things (like notify triggers) can easier run afterwards as, say zzt*
#
# Revision 1.5  2003/05/15 10:18:32  ncq
# - name triggers "zzt_*" so they are executed last
# - name trigger function "ft_*"
# - better __doc__
#
# Revision 1.4  2003/05/14 22:03:28  ncq
# - better names for template definitions and lots of other items
# - attributes -> columns
# - check whether target table exists, fail if not
#
# Revision 1.3  2003/05/13 14:55:43  ncq
# - take list of columns to be audited from target audit table,
#   not from source table, this implies that the target table MUST exist
#   prior to running this script
#
# Revision 1.2  2003/05/13 14:39:11  ncq
# - separate triggers/functions for insert/update/delete
# - seems to work now
#
# Revision 1.1  2003/05/12 20:57:19  ncq
# - audit schema generator
#
#
# @change log:
#	12.07.2001 hherb first draft, untested
