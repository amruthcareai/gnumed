# -*- coding: utf-8 -*-
"""Billing code.

Copyright: authors
"""
#============================================================
__author__ = "Nico Latzer <nl@mnet-online.de>, Karsten Hilbert <Karsten.Hilbert@gmx.net>"
__license__ = 'GPL v2 or later (details at http://www.gnu.org)'

import sys
import logging
import zlib


if __name__ == '__main__':
	sys.path.insert(0, '../../')
from Gnumed.pycommon import gmPG2
from Gnumed.pycommon import gmBusinessDBObject
from Gnumed.pycommon import gmTools
from Gnumed.pycommon import gmDateTime

from Gnumed.business import gmDemographicRecord
from Gnumed.business import gmDocuments

_log = logging.getLogger('gm.bill')

INVOICE_DOCUMENT_TYPE = u'invoice'
# default: old style
DEFAULT_INVOICE_ID_TEMPLATE = u'GM%(pk_pat)s / %(date)s / %(time)s'

#============================================================
# billables
#------------------------------------------------------------
_SQL_get_billable_fields = u"SELECT * FROM ref.v_billables WHERE %s"

class cBillable(gmBusinessDBObject.cBusinessDBObject):
	"""Items which can be billed to patients."""

	_cmd_fetch_payload = _SQL_get_billable_fields % u"pk_billable = %s"
	_cmds_store_payload = [
		u"""UPDATE ref.billable SET
				fk_data_source = %(pk_data_source)s,
				code = %(billable_code)s,
				term = %(billable_description)s,
				comment = gm.nullify_empty_string(%(comment)s),
				amount = %(raw_amount)s,
				currency = %(currency)s,
				vat_multiplier = %(vat_multiplier)s,
				active = %(active)s
				--, discountable = %(discountable)s
			WHERE
				pk = %(pk_billable)s
					AND
				xmin = %(xmin_billable)s
			RETURNING
				xmin AS xmin_billable
		"""]

	_updatable_fields = [
		'billable_code',
		'billable_description',
		'raw_amount',
		'vat_multiplier',
		'comment',
		'currency',
		'active',
		'pk_data_source'
	]
	#--------------------------------------------------------
	def format(self):
		txt = u'%s                                    [#%s]\n\n' % (
			gmTools.bool2subst (
				self._payload[self._idx['active']],
				_('Active billable item'),
				_('Inactive billable item')
			),
			self._payload[self._idx['pk_billable']]
		)
		txt += u' %s: %s\n' % (
			self._payload[self._idx['billable_code']],
			self._payload[self._idx['billable_description']]
		)
		txt += _(' %(curr)s%(raw_val)s + %(perc_vat)s%% VAT = %(curr)s%(val_w_vat)s\n') % {
			'curr': self._payload[self._idx['currency']],
			'raw_val': self._payload[self._idx['raw_amount']],
			'perc_vat': self._payload[self._idx['vat_multiplier']] * 100,
			'val_w_vat': self._payload[self._idx['amount_with_vat']]
		}
		txt += u' %s %s%s (%s)' % (
			self._payload[self._idx['catalog_short']],
			self._payload[self._idx['catalog_version']],
			gmTools.coalesce(self._payload[self._idx['catalog_language']], u'', ' - %s'),
			self._payload[self._idx['catalog_long']]
		)
		txt += gmTools.coalesce(self._payload[self._idx['comment']], u'', u'\n %s')

		return txt
	#--------------------------------------------------------
	def _get_is_in_use(self):
		cmd = u'SELECT EXISTS(SELECT 1 FROM bill.bill_item WHERE fk_billable = %(pk)s LIMIT 1)'
		rows, idx = gmPG2.run_ro_queries(queries = [{'cmd': cmd, 'args': {'pk': self._payload[self._idx['pk_billable']]}}])
		return rows[0][0]

	is_in_use = property(_get_is_in_use, lambda x:x)

#------------------------------------------------------------
def get_billables(active_only=True, order_by=None):

	if order_by is None:
		order_by = u' ORDER BY catalog_long, catalog_version, billable_code'
	else:
		order_by = u' ORDER BY %s' % order_by

	if active_only:
		where = u'active IS true'
	else:
		where = u'true'

	cmd = (_SQL_get_billable_fields % where) + order_by
	rows, idx = gmPG2.run_ro_queries(queries = [{'cmd': cmd}], get_col_idx = True)
	return [ cBillable(row = {'data': r, 'idx': idx, 'pk_field': 'pk_billable'}) for r in rows ]

#------------------------------------------------------------
def create_billable(code=None, term=None, data_source=None, return_existing=False):
	args = {
		'code': code.strip(),
		'term': term.strip(),
		'data_src': data_source
	}
	cmd = u"""
		INSERT INTO ref.billable (code, term, fk_data_source)
		SELECT
			%(code)s,
			%(term)s,
			%(data_src)s
		WHERE NOT EXISTS (
			SELECT 1 FROM ref.billable
			WHERE
				code = %(code)s
					AND
				term = %(term)s
					AND
				fk_data_source = %(data_src)s
		)
		RETURNING pk"""
	rows, idx = gmPG2.run_rw_queries(queries = [{'cmd': cmd, 'args': args}], get_col_idx = False, return_data = True)
	if len(rows) > 0:
		return cBillable(aPK_obj = rows[0]['pk'])

	if not return_existing:
		return None

	cmd = u"""
		SELECT * FROM ref.v_billables
		WHERE
			code = %(code)s
				AND
			term = %(term)s
				AND
			pk_data_source = %(data_src)s
	"""
	rows, idx = gmPG2.run_ro_queries(queries = [{'cmd': cmd, 'args': args}], get_col_idx = True)
	return cBillable(row = {'data': rows[0], 'idx': idx, 'pk_field': 'pk_billable'})

#------------------------------------------------------------
def delete_billable(pk_billable=None):
	cmd = u"""
		DELETE FROM ref.billable
		WHERE
			pk = %(pk)s
				AND
			NOT EXISTS (
				SELECT 1 FROM bill.bill_item WHERE fk_billable = %(pk)s
			)
	"""
	args = {'pk': pk_billable}
	gmPG2.run_rw_queries(queries = [{'cmd': cmd, 'args': args}])

#============================================================
# bill items
#------------------------------------------------------------
_SQL_get_bill_item_fields = u"SELECT * FROM bill.v_bill_items WHERE %s"

class cBillItem(gmBusinessDBObject.cBusinessDBObject):

	_cmd_fetch_payload = _SQL_get_bill_item_fields % u"pk_bill_item = %s"
	_cmds_store_payload = [
		u"""UPDATE bill.bill_item SET
				fk_provider = %(pk_provider)s,
				fk_encounter = %(pk_encounter_to_bill)s,
				date_to_bill = %(raw_date_to_bill)s,
				description = gm.nullify_empty_string(%(item_detail)s),
				net_amount_per_unit = %(net_amount_per_unit)s,
				currency = gm.nullify_empty_string(%(currency)s),
				fk_bill = %(pk_bill)s,
				unit_count = %(unit_count)s,
				amount_multiplier = %(amount_multiplier)s
			WHERE
				pk = %(pk_bill_item)s
					AND
				xmin = %(xmin_bill_item)s
			RETURNING
				xmin AS xmin_bill_item
		"""]

	_updatable_fields = [
		'pk_provider',
		'pk_encounter_to_bill',
		'raw_date_to_bill',
		'item_detail',
		'net_amount_per_unit',
		'currency',
		'pk_bill',
		'unit_count',
		'amount_multiplier'
	]
	#--------------------------------------------------------
	def format(self):
		txt = u'%s (%s %s%s)         [#%s]\n' % (
			gmTools.bool2subst(
				self._payload[self._idx['pk_bill']] is None,
				_('Open item'),
				_('Billed item'),
			),
			self._payload[self._idx['catalog_short']],
			self._payload[self._idx['catalog_version']],
			gmTools.coalesce(self._payload[self._idx['catalog_language']], u'', ' - %s'),
			self._payload[self._idx['pk_bill_item']]
		)
		txt += u' %s: %s\n' % (
			self._payload[self._idx['billable_code']],
			self._payload[self._idx['billable_description']]
		)
		txt += gmTools.coalesce (
			self._payload[self._idx['billable_comment']],
			u'',
			u'  (%s)\n',
		)
		txt += gmTools.coalesce (
			self._payload[self._idx['item_detail']],
			u'',
			_(' Details: %s\n'),
		)

		txt += u'\n'
		txt += _(' %s of units: %s\n') % (
			gmTools.u_numero,
			self._payload[self._idx['unit_count']]
		)
		txt += _(' Amount per unit: %(curr)s%(val_p_unit)s (%(cat_curr)s%(cat_val)s per catalog)\n') % {
			'curr': self._payload[self._idx['currency']],
			'val_p_unit': self._payload[self._idx['net_amount_per_unit']],
			'cat_curr': self._payload[self._idx['billable_currency']],
			'cat_val': self._payload[self._idx['billable_amount']]
		}
		txt += _(' Amount multiplier: %s\n') % self._payload[self._idx['amount_multiplier']]
		txt += _(' VAT would be: %(perc_vat)s%% %(equals)s %(curr)s%(vat)s\n') % {
			'perc_vat': self._payload[self._idx['vat_multiplier']] * 100,
			'equals': gmTools.u_corresponds_to,
			'curr': self._payload[self._idx['currency']],
			'vat': self._payload[self._idx['vat']]
		}

		txt += u'\n'
		txt += _(' Charge date: %s') % gmDateTime.pydt_strftime (
			self._payload[self._idx['date_to_bill']],
			'%Y %b %d',
			accuracy = gmDateTime.acc_days
		)
		bill = self.bill
		if bill is not None:
			txt += _('\n On bill: %s') % bill['invoice_id']

		return txt
	#--------------------------------------------------------
	def _get_billable(self):
		return cBillable(aPK_obj = self._payload[self._idx['pk_billable']])

	billable = property(_get_billable, lambda x:x)
	#--------------------------------------------------------
	def _get_bill(self):
		if self._payload[self._idx['pk_bill']] is None:
			return None
		return cBill(aPK_obj = self._payload[self._idx['pk_bill']])

	bill = property(_get_bill, lambda x:x)
	#--------------------------------------------------------
	def _get_is_in_use(self):
		return self._payload[self._idx['pk_bill']] is not None

	is_in_use = property(_get_is_in_use, lambda x:x)
#------------------------------------------------------------
def get_bill_items(pk_patient=None, non_invoiced_only=False):
	if non_invoiced_only:
		cmd = _SQL_get_bill_item_fields % u"pk_patient = %(pat)s AND pk_bill IS NULL"
	else:
		cmd = _SQL_get_bill_item_fields % u"pk_patient = %(pat)s"
	args = {'pat': pk_patient}
	rows, idx = gmPG2.run_ro_queries(queries = [{'cmd': cmd, 'args': args}], get_col_idx = True)
	return [ cBillItem(row = {'data': r, 'idx': idx, 'pk_field': 'pk_bill_item'}) for r in rows ]

#------------------------------------------------------------
def create_bill_item(pk_encounter=None, pk_billable=None, pk_staff=None):

	billable = cBillable(aPK_obj = pk_billable)
	cmd = u"""
		INSERT INTO bill.bill_item (
			fk_provider,
			fk_encounter,
			net_amount_per_unit,
			currency,
			fk_billable
		) VALUES (
			%(staff)s,
			%(enc)s,
			%(val)s,
			%(curr)s,
			%(billable)s
		)
		RETURNING pk"""
	args = {
		'staff': pk_staff,
		'enc': pk_encounter,
		'val': billable['raw_amount'],
		'curr': billable['currency'],
		'billable': pk_billable
	}
	rows, idx = gmPG2.run_rw_queries(queries = [{'cmd': cmd, 'args': args}], return_data = True)
	return cBillItem(aPK_obj = rows[0][0])

#------------------------------------------------------------
def delete_bill_item(link_obj=None, pk_bill_item=None):
	cmd = u'DELETE FROM bill.bill_item WHERE pk = %(pk)s AND fk_bill IS NULL'
	args = {'pk': pk_bill_item}
	gmPG2.run_rw_queries(link_obj = link_obj, queries = [{'cmd': cmd, 'args': args}])

#============================================================
# bills
#------------------------------------------------------------
_SQL_get_bill_fields = u"""SELECT * FROM bill.v_bills WHERE %s"""

class cBill(gmBusinessDBObject.cBusinessDBObject):
	"""Represents a bill"""

	_cmd_fetch_payload = _SQL_get_bill_fields % u"pk_bill = %s"
	_cmds_store_payload = [
		u"""UPDATE bill.bill SET
				invoice_id = gm.nullify_empty_string(%(invoice_id)s),
				close_date = %(close_date)s,
				apply_vat = %(apply_vat)s,
				comment = gm.nullify_empty_string(%(comment)s),
				fk_receiver_identity = %(pk_receiver_identity)s,
				fk_receiver_address = %(pk_receiver_address)s,
				fk_doc = %(pk_doc)s
			WHERE
				pk = %(pk_bill)s
					AND
				xmin = %(xmin_bill)s
			RETURNING
				pk as pk_bill,
				xmin as xmin_bill
		"""
	]
	_updatable_fields = [
		u'invoice_id',
		u'pk_receiver_identity',
		u'close_date',
		u'apply_vat',
		u'comment',
		u'pk_receiver_address',
		u'pk_doc'
	]
	#--------------------------------------------------------
	def format(self, include_receiver=True, include_doc=True):
		txt = u'%s                       [#%s]\n' % (
			gmTools.bool2subst (
				(self._payload[self._idx['close_date']] is None),
				_('Open bill'),
				_('Closed bill')
			),
			self._payload[self._idx['pk_bill']]
		)
		txt += _(' Invoice ID: %s\n') % self._payload[self._idx['invoice_id']]

		if self._payload[self._idx['close_date']] is not None:
			txt += _(' Closed: %s\n') % gmDateTime.pydt_strftime (
				self._payload[self._idx['close_date']],
				'%Y %b %d',
				accuracy = gmDateTime.acc_days
			)

		if self._payload[self._idx['comment']] is not None:
			txt += _(' Comment: %s\n') % self._payload[self._idx['comment']]

		txt += _(' Bill value: %(curr)s%(val)s\n') % {
			'curr': self._payload[self._idx['currency']],
			'val': self._payload[self._idx['total_amount']]
		}

		if self._payload[self._idx['apply_vat']] is None:
			txt += _(' VAT: undecided\n')
		elif self._payload[self._idx['apply_vat']] is True:
			txt += _(' VAT: %(perc_vat)s%% %(equals)s %(curr)s%(vat)s\n') % {
				'perc_vat': self._payload[self._idx['percent_vat']],
				'equals': gmTools.u_corresponds_to,
				'curr': self._payload[self._idx['currency']],
				'vat': self._payload[self._idx['total_vat']]
			}
			txt += _(' Value + VAT: %(curr)s%(val)s\n') % {
				'curr': self._payload[self._idx['currency']],
				'val': self._payload[self._idx['total_amount_with_vat']]
			}
		else:
			txt += _(' VAT: does not apply\n')

		if self._payload[self._idx['pk_bill_items']] is None:
			txt += _(' Items billed: 0\n')
		else:
			txt += _(' Items billed: %s\n') % len(self._payload[self._idx['pk_bill_items']])
		if include_doc:
			txt += _(' Invoice: %s\n') % (
				gmTools.bool2subst (
					self._payload[self._idx['pk_doc']] is None,
					_('not available'),
					u'#%s' % self._payload[self._idx['pk_doc']]
				)
			)
		txt += _(' Patient: #%s\n') % self._payload[self._idx['pk_patient']]
		if include_receiver:
			txt += gmTools.coalesce (
				self._payload[self._idx['pk_receiver_identity']],
				u'',
				_(' Receiver: #%s\n')
			)
			if self._payload[self._idx['pk_receiver_address']] is not None:
				txt += u'\n '.join(gmDemographicRecord.get_patient_address(pk_patient_address = self._payload[self._idx['pk_receiver_address']]).format())

		return txt
	#--------------------------------------------------------
	def add_items(self, items=None):
		"""Requires no pending changes within the bill itself."""
		# should check for item consistency first
		conn = gmPG2.get_connection(readonly = False)
		for item in items:
			item['pk_bill'] = self._payload[self._idx['pk_bill']]
			item.save(conn = conn)
		conn.commit()
		self.refetch_payload()		# make sure aggregates are re-filled from view
	#--------------------------------------------------------
	def _get_bill_items(self):
		return [ cBillItem(aPK_obj = pk) for pk in self._payload[self._idx['pk_bill_items']] ]

	bill_items = property(_get_bill_items, lambda x:x)
	#--------------------------------------------------------
	def _get_invoice(self):
		if self._payload[self._idx['pk_doc']] is None:
			return None
		return gmDocuments.cDocument(aPK_obj = self._payload[self._idx['pk_doc']])

	invoice = property(_get_invoice, lambda x:x)
	#--------------------------------------------------------
	def _get_address(self):
		if self._payload[self._idx['pk_receiver_address']] is None:
			return None
		return gmDemographicRecord.get_address_from_patient_address_pk (
			pk_patient_address = self._payload[self._idx['pk_receiver_address']]
		)

	address = property(_get_address, lambda x:x)
	#--------------------------------------------------------
	def _get_default_address(self):
		return gmDemographicRecord.get_patient_address_by_type (
			pk_patient = self._payload[self._idx['pk_patient']],
			adr_type = u'billing'
		)

	default_address = property(_get_default_address, lambda x:x)
	#--------------------------------------------------------
	def _get_home_address(self):
		return gmDemographicRecord.get_patient_address_by_type (
			pk_patient = self._payload[self._idx['pk_patient']],
			adr_type = u'home'
		)

	home_address = property(_get_home_address, lambda x:x)
	#--------------------------------------------------------
	def set_missing_address_from_default(self):
		if self._payload[self._idx['pk_receiver_address']] is not None:
			return True
		adr = self.default_address
		if adr is None:
			adr = self.home_address
			if adr is None:
				return False
		self['pk_receiver_address'] = adr['pk_lnk_person_org_address']
		return self.save_payload()

#------------------------------------------------------------
def get_bills(order_by=None, pk_patient=None):

	args = {'pat': pk_patient}
	where_parts = [u'true']

	if pk_patient is not None:
		where_parts.append(u'pk_patient = %(pat)s')

	if order_by is None:
		order_by = u''
	else:
		order_by = u' ORDER BY %s' % order_by

	cmd = (_SQL_get_bill_fields % u' AND '.join(where_parts)) + order_by
	rows, idx = gmPG2.run_ro_queries(queries = [{'cmd': cmd, 'args': args}], get_col_idx = True)
	return [ cBill(row = {'data': r, 'idx': idx, 'pk_field': 'pk_bill'}) for r in rows ]

#------------------------------------------------------------
def get_bills4document(pk_document=None):
	args = {'pk_doc': pk_document}
	cmd = _SQL_get_bill_fields % u'pk_doc = %(pk_doc)s'
	rows, idx = gmPG2.run_ro_queries(queries = [{'cmd': cmd, 'args': args}], get_col_idx = True)
	return [ cBill(row = {'data': r, 'idx': idx, 'pk_field': 'pk_bill'}) for r in rows ]

#------------------------------------------------------------
def create_bill(conn=None, invoice_id=None):

	args = {u'inv_id': invoice_id}
	cmd = u"""
		INSERT INTO bill.bill (invoice_id)
		VALUES (gm.nullify_empty_string(%(inv_id)s))
		RETURNING pk
	"""
	rows, idx = gmPG2.run_rw_queries(link_obj = conn, queries = [{'cmd': cmd, 'args': args}], return_data = True, get_col_idx = False)

	return cBill(aPK_obj = rows[0]['pk'])

#------------------------------------------------------------
def delete_bill(link_obj=None, pk_bill=None):
	args = {'pk': pk_bill}
	cmd = u"DELETE FROM bill.bill WHERE pk = %(pk)s"
	gmPG2.run_rw_queries(link_obj = link_obj, queries = [{'cmd': cmd, 'args': args}])
	return True

#------------------------------------------------------------
def get_bill_receiver(pk_patient=None):
	pass

#------------------------------------------------------------
def generate_invoice_id(template=None, pk_patient=None, person=None, date_format='%Y-%m-%d', time_format='%H%M%S'):
	"""Generate invoice ID string, based on template.

	No template given -> generate old style fixed format invoice ID.

	Placeholders:
		%(pk_pat)s
		%(date)s
		%(time)s
			if included, $counter$ is not *needed* (but still possible)
		%(firstname)s
		%(lastname)s
		%(dob)s

		#counter#
			will be replaced by a counter, counting up from 1 until the invoice id is unique, max 999999
	"""
	assert (None in [pk_patient, person]), u'either of <pk_patient> or <person> can be defined, but not both'

	if (template is None) or (template.strip() == u''):
		template = DEFAULT_INVOICE_ID_TEMPLATE
		date_format = '%Y-%m-%d'
		time_format = '%H%M%S'
	template = template.strip()
	_log.debug('invoice ID template: %s', template)
	if pk_patient is None:
		if person is not None:
			pk_patient = person.ID
	now = gmDateTime.pydt_now_here()
	data = {}
	data['pk_pat'] = gmTools.coalesce(pk_patient, '?')
	data['date'] = gmDateTime.pydt_strftime(now, date_format).strip()
	data['time'] = gmDateTime.pydt_strftime(now, time_format).strip()
	if person is None:
		data['firstname'] = u'?'
		data['lastname'] = u'?'
		data['dob'] = u'?'
	else:
		data['firstname'] = person['firstnames'].replace(' ', gmTools.u_space_as_open_box).strip()
		data['lastname'] = person['lastnames'].replace(' ', gmTools.u_space_as_open_box).strip()
		data['dob'] = person.get_formatted_dob (
			format = date_format,
			encoding = 'utf8',
			none_string = u'?',
			honor_estimation = False
		).strip()
	candidate_invoice_id = template % data
	if u'#counter#' not in candidate_invoice_id:
		if u'%(time)s' in template:
			return candidate_invoice_id

		candidate_invoice_id = candidate_invoice_id + u' [##counter#]'

	_log.debug('invoice id candidate: %s', candidate_invoice_id)
	# get existing invoice IDs consistent with candidate
	search_term = u'^\s*%s\s*$' % gmPG2.sanitize_pg_regex(expression = candidate_invoice_id).replace(u'#counter#', '\d+')
	cmd = u'SELECT invoice_id FROM bill.bill WHERE invoice_id ~* %(search_term)s UNION ALL SELECT invoice_id FROM audit.log_bill WHERE invoice_id ~* %(search_term)s'
	args = {'search_term': search_term}
	rows, idx = gmPG2.run_ro_queries(queries = [{'cmd': cmd, 'args': args}])
	if len(rows) == 0:
		return candidate_invoice_id.replace(u'#counter#', u'1')

	existing_invoice_ids = [ r['invoice_id'].strip() for r in rows ]
	counter = None
	counter_max = 999999
	for idx in range(1, counter_max):
		candidate = candidate_invoice_id.replace(u'#counter#', '%s' % idx)
		if candidate not in existing_invoice_ids:
			counter = idx
			break
	if counter is None:
		# exhausted the range, unlikely (1 million bills are possible
		# even w/o any other invoice ID data) but technically possible
		_log.debug('exhausted uniqueness space of [%s] invoice IDs per template', counter_max)
		counter = '>%s[%s]' % (counter_max, data['time'])

	return candidate_invoice_id.replace(u'#counter#', '%s' % counter)

#------------------------------------------------------------
def lock_invoice_id(invoice_id):
	_log.debug('locking invoice ID: %s', invoice_id)
	crc32 = zlib.crc32(invoice_id)
	adler32 = zlib.adler32(invoice_id)
	_log.debug('crc32: %s', crc32)
	_log.debug('adler32: %s', adler32)
	cmd = u"""SELECT pg_try_advisory_lock(%s, %s)""" % (crc32, adler32)
	rows, idx = gmPG2.run_ro_queries(queries = [{'cmd': cmd}])
	if rows[0][0]:
		return True

	_log.warning('cannot lock invoice ID: [%s] (%s/%s)', invoice_id, crc32, adler32)
	return False

#------------------------------------------------------------
def unlock_invoice_id(invoice_id):
	_log.debug('unlocking invoice ID: %s', invoice_id)
	crc32 = zlib.crc32(invoice_id)
	adler32 = zlib.adler32(invoice_id)
	_log.debug('crc32: %s', crc32)
	_log.debug('adler32: %s', adler32)
	cmd = u"""SELECT pg_advisory_unlock(%s, %s)""" % (crc32, adler32)
	rows, idx = gmPG2.run_ro_queries(queries = [{'cmd': cmd}])
	if rows[0][0]:
		return True

	_log.warning('cannot unlock invoice ID: [%s] (%s/%s)', invoice_id, crc32, adler32)
	return False

#============================================================
# main
#------------------------------------------------------------
if __name__ == "__main__":

	if len(sys.argv) < 2:
		sys.exit()

	if sys.argv[1] != 'test':
		sys.exit()

#	from Gnumed.pycommon import gmLog2
#	from Gnumed.pycommon import gmI18N
#	from Gnumed.business import gmPerson

#	gmI18N.activate_locale()
##	gmDateTime.init()

	def test_default_address():
		bills = get_bills(pk_patient = 12)
		first_bill = bills[0]
		print first_bill.default_address

	#--------------------------------------------------
	def test_me():
		print "--------------"
		me = cBillable(aPK_obj=1)
		fields = me.get_fields()
		for field in fields:
			print field, ':', me[field]
		print "updatable:", me.get_updatable_fields()
		#me['vat']=4; me.store_payload()

	#--------------------------------------------------
	def test_generate_invoice_id():
		from Gnumed.pycommon import gmI18N
		gmI18N.activate_locale()
		gmI18N.install_domain()
		import gmPerson
		for idx in range(1,15):
			print ''
			print 'classic:', generate_invoice_id(pk_patient = idx)
			pat = gmPerson.cPerson(idx)
			template = u'%(firstname).4s%(lastname).4s%(date)s'
			print 'new: template = "%s" => %s' % (
				template,
				generate_invoice_id (
					template = template,
					pk_patient = None,
					person = pat,
					date_format='%d%m%Y',
					time_format='%H%M%S'
				)
			)
			template = u'%(firstname).4s%(lastname).4s%(date)s-#counter#'
			print 'new: template = "%s" => %s' % (
				template,
				generate_invoice_id (
					template = template,
					pk_patient = None,
					person = pat,
					date_format='%d%m%Y',
					time_format='%H%M%S'
				)
			)

		#generate_invoice_id(template=None, pk_patient=None, person=None, date_format='%Y-%m-%d', time_format='%H%M%S')

	#--------------------------------------------------

	#test_me()
	test_default_address()
	test_generate_invoice_id()
