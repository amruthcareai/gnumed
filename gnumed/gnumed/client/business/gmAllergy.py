# -*- coding: utf-8 -*-
"""GNUmed allergy related business object."""
#============================================================
__author__ = "Carlos Moro <cfmoro1976@yahoo.es>"
__license__ = "GPL v2 or later"

import types, sys, logging, datetime as pyDT


if __name__ == '__main__':
	sys.path.insert(0, '../../')
from Gnumed.pycommon import gmPG2
from Gnumed.pycommon import gmI18N
from Gnumed.pycommon import gmBusinessDBObject
from Gnumed.pycommon import gmDateTime
from Gnumed.pycommon import gmTools


_log = logging.getLogger('gm.domain')
#============================================================
# allergy state related code
#============================================================
allergy_states = [
	None,		# unknown
	0,			# no allergies
	1			# some allergies
]
#------------------------------------------------------------
def ensure_has_allergy_state(encounter=None):

	_log.debug('checking allergy state for identity of encounter [%s]', encounter)

	args = {'enc': encounter}
	cmd_create = u"""
		INSERT INTO clin.allergy_state (
			fk_encounter,
			has_allergy
		)	SELECT
				%(enc)s,
				NULL
			WHERE NOT EXISTS (
				SELECT 1 FROM clin.v_pat_allergy_state
				WHERE pk_patient = (
					SELECT fk_patient FROM clin.encounter WHERE pk = %(enc)s
				)
			)
	"""
	cmd_search = u"""
		SELECT pk_allergy_state FROM clin.v_pat_allergy_state
		WHERE pk_patient = (
			SELECT fk_patient FROM clin.encounter WHERE pk = %(enc)s
		)
	"""
	rows, idx = gmPG2.run_rw_queries (
		queries = [
			{'cmd': cmd_create, 'args': args},
			{'cmd': cmd_search, 'args': args}
		],
		return_data = True
	)

	return cAllergyState(aPK_obj = rows[0][0])

#------------------------------------------------------------
class cAllergyState(gmBusinessDBObject.cBusinessDBObject):
	"""Represents the allergy state of one patient."""

	_cmd_fetch_payload = u"select * from clin.v_pat_allergy_state where pk_allergy_state = %s"
	_cmds_store_payload = [
		u"""update clin.allergy_state set
				last_confirmed = %(last_confirmed)s,
				has_allergy = %(has_allergy)s,
				comment = gm.nullify_empty_string(%(comment)s)
			where
				pk = %(pk_allergy_state)s and
				xmin = %(xmin_allergy_state)s""",
		u"""select xmin_allergy_state from clin.v_pat_allergy_state where pk_allergy_state = %(pk_allergy_state)s"""
	]
	_updatable_fields = [
		'last_confirmed',		# special value u'now' will set to datetime.datetime.now() in the local time zone
		'has_allergy',			# verified against allergy_states (see above)
		'comment'				# u'' maps to None / NULL
	]
	#--------------------------------------------------------
	# properties
	#--------------------------------------------------------
	def _get_as_string(self):
		if self._payload[self._idx['has_allergy']] is None:
			return _('unknown allergy state')
		if self._payload[self._idx['has_allergy']] == 0:
			return _('no known allergies')
		if self._payload[self._idx['has_allergy']] == 1:
			return _('*does* have allergies')
		_log.error('unknown allergy state [%s]', self._payload[self._idx['has_allergy']])
		return _('ERROR: unknown allergy state [%s]') % self._payload[self._idx['has_allergy']]

	def _set_string(self, value):
		raise AttributeError('invalid to set allergy state string')

	state_string = property(_get_as_string, _set_string)

	#--------------------------------------------------------
	def _get_as_symbol(self):
		if self._payload[self._idx['has_allergy']] is None:
			if self._payload[self._idx['comment']] is None:
				return u'?'
			else:
				return u'?!'
		if self._payload[self._idx['has_allergy']] == 0:
			if self._payload[self._idx['comment']] is None:
				return u'\u2300'
			else:
				return u'\u2300!'
		if self._payload[self._idx['has_allergy']] == 1:
			return '!'
		_log.error('unknown allergy state [%s]', self._payload[self._idx['has_allergy']])
		return _('ERROR: unknown allergy state [%s]') % self._payload[self._idx['has_allergy']]

	state_symbol = property(_get_as_symbol, lambda x:x)

	#--------------------------------------------------------
	def _get_as_amts_latex(self, strict=True):
		table_rows = []
		# Zwischenüberschrift: 31 Zeichen, $..., 14pt, no frame, \textwidth
		state = u'%s (%s)' % (
			self.state_string,
			gmDateTime.pydt_strftime(self['last_confirmed'], '%b %Y')
		)
		if strict:
			state = state[:31]
		table_rows.append(u'\\multicolumn{11}{>{\\RaggedRight}p{27.9cm}}{\\rule{0pt}{4.5mm} \\fontsize{14pt}{16pt}\selectfont %s\label{AnchorAllergieDetails}}\\tabularnewline' % gmTools.tex_escape_string(state))
		# Freitextzeile: 200 Zeichen, @..., \textwidth
		if self['comment'] is not None:
			if strict:
				cmt = self['comment'].strip()[:200]
			else:
				cmt = self['comment'].strip()
			table_rows.append(u'\\multicolumn{11}{>{\\RaggedRight}p{27.9cm}}{%s}\\tabularnewline') % gmTools.tex_escape_string(cmt)
		return table_rows

	as_amts_latex = property(_get_as_amts_latex, lambda x:x)

	#--------------------------------------------------------
	def _get_as_amts_data(self, strict=True):
		lines = []
		# Zwischenüberschrift: 31 Zeichen, $..., \textwidth
		txt = u'$%s (%s)' % (
			self.state_string,
			gmDateTime.pydt_strftime(self['last_confirmed'], '%b %Y')
		)
		if strict:
			lines.append(txt[:32])
		else:
			lines.append(txt)
		# Freitextzeile: 200 Zeichen, @..., \textwidth
		if self['comment'] is not None:
			if strict:
				lines.append(u'@%s' % self['comment'][:200])
			else:
				lines.append(u'@%s' % self['comment'])
		return lines

	as_amts_data = property(_get_as_amts_data, lambda x:x)

	#--------------------------------------------------------
	def __setitem__(self, attribute, value):
		if attribute == u'comment':
			if value is not None:
				if value.strip() == u'':
					value = None

		elif attribute == u'last_confirmed':
			if value == u'now':
				value = pyDT.datetime.now(tz = gmDateTime.gmCurrentLocalTimezone)

		elif attribute == u'has_allergy':
			if value not in allergy_states:
				raise ValueError('invalid allergy state [%s]' % value)

		gmBusinessDBObject.cBusinessDBObject.__setitem__(self, attribute, value)

#============================================================
class cAllergy(gmBusinessDBObject.cBusinessDBObject):
	"""Represents one allergy item.

	Actually, those things are really things to "avoid".
	Allergy is just one of several reasons for that.
	See Adrian's post on gm-dev.

	Another word might be Therapeutic Precautions.
	"""
	_cmd_fetch_payload = u"SELECT * FROM clin.v_pat_allergies WHERE pk_allergy = %s"
	_cmds_store_payload = [
		u"""UPDATE clin.allergy SET
				clin_when = %(date)s,
				substance = %(substance)s,
				substance_code = %(substance_code)s,
				generics = %(generics)s,
				allergene = %(allergene)s,
				atc_code = %(atc_code)s,
				fk_type = %(pk_type)s,
				generic_specific = %(generic_specific)s::boolean,
				definite = %(definite)s::boolean,
				narrative = %(reaction)s
			WHERE
				pk = %(pk_allergy)s AND
				xmin = %(xmin_allergy)s""",
		u"""SELECT xmin_allergy FROM clin.v_pat_allergies WHERE pk_allergy=%(pk_allergy)s"""
	]
	_updatable_fields = [
		'date',
		'substance',
		'substance_code',
		'generics',
		'allergene',
		'atc_code',
		'pk_type',
		'generic_specific',
		'definite',
		'reaction'
	]
	#--------------------------------------------------------
	def __setitem__(self, attribute, value):
		if attribute == 'pk_type':
			if value in ['allergy', 'sensitivity']:
				cmd = u'select pk from clin._enum_allergy_type where value=%s'
				rows, idx = gmPG2.run_ro_queries(queries = [{'cmd': cmd, 'args': [value]}])
				value = rows[0][0]

		gmBusinessDBObject.cBusinessDBObject.__setitem__(self, attribute, value)

	#--------------------------------------------------------
	def _get_as_amts_latex(self, strict=True):
		# Freitextzeile: 200 Zeichen, @...
		cells = [u'\\multicolumn{1}{>{\\RaggedRight}p{4cm}}{%s}' % gmTools.tex_escape_string(self['descriptor'])]
		txt = u'%s%s' % (
			self['l10n_type'],
			gmTools.coalesce(self['reaction'], u'', u': %s')
		)
		if strict:
			txt = txt[:(200-len(self['descriptor']))]
		cells.append(u'\\multicolumn{10}{>{\\RaggedRight}p{23.9cm}}{%s}' % gmTools.tex_escape_string(txt))
		table_row = u' & '.join(cells)
		table_row += u'\\tabularnewline'
		return table_row

	as_amts_latex = property(_get_as_amts_latex, lambda x:x)

	#--------------------------------------------------------
	def _get_as_amts_data(self, strict=True):
		# Freitextzeile: 200 Zeichen, @..., \textwidth
		txt = u'@%s %s%s' % (
			self['descriptor'],
			self['l10n_type'],
			gmTools.coalesce(self['reaction'], u'', u': %s')
		)
		if strict:
			return txt[:200]
		return txt

	as_amts_data = property(_get_as_amts_data, lambda x:x)

#============================================================
# convenience functions
#------------------------------------------------------------
def create_allergy(allergene=None, allg_type=None, episode_id=None, encounter_id=None):
	"""Creates a new allergy clinical item.

	allergene - allergic substance
	allg_type - allergy or sensitivity, pk or string
	encounter_id - encounter's primary key
	episode_id - episode's primary key
	"""
	cmd = u"""
		SELECT pk_allergy
		FROM clin.v_pat_allergies
		WHERE
			pk_patient = (SELECT fk_patient FROM clin.encounter WHERE pk = %(enc)s)
				AND
			allergene = %(allergene)s
	"""
	#args = {'enc': encounter_id, 'substance': substance}
	args = {'enc': encounter_id, 'allergene': allergene}
	rows, idx = gmPG2.run_ro_queries(queries = [{'cmd': cmd, 'args': args}])
	if len(rows) > 0:
		# don't implicitely change existing data
		return cAllergy(aPK_obj = rows[0][0])

	# insert new allergy
	queries = []

	if type(allg_type) == types.IntType:
		cmd = u"""
			insert into clin.allergy (fk_type, fk_encounter, fk_episode, allergene, substance)
			values (%s, %s, %s, %s, %s)"""
	else:
		cmd = u"""
			insert into clin.allergy (fk_type, fk_encounter, fk_episode,  allergene, substance)
			values ((select pk from clin._enum_allergy_type where value = %s), %s, %s, %s, %s)"""
	queries.append({'cmd': cmd, 'args': [allg_type, encounter_id, episode_id, allergene, allergene]})

	cmd = u"select currval('clin.allergy_id_seq')"
	queries.append({'cmd': cmd})

	rows, idx = gmPG2.run_rw_queries(queries=queries, return_data=True)
	allergy = cAllergy(aPK_obj = rows[0][0])

	return allergy
#============================================================
# main - unit testing
#------------------------------------------------------------
if __name__ == '__main__':

	allg = cAllergy(aPK_obj=1)
	print allg
	fields = allg.get_fields()
	for field in fields:
		print field, ':', allg[field]
	print "updatable:", allg.get_updatable_fields()
	enc_id = allg['pk_encounter']
	epi_id = allg['pk_episode']
	status, allg = create_allergy (
		allergene = 'test substance',
		allg_type = 1,
		episode_id = epi_id,
		encounter_id = enc_id
	)
	print allg
	allg['reaction'] = 'hehehe'
	status, data = allg.save_payload()
	print 'status:', status
	print 'data:', data
	print allg
