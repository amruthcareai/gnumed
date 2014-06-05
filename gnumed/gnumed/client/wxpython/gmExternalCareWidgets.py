"""GNUmed external patient care widgets."""
#================================================================
__author__ = "Karsten.Hilbert@gmx.net"
__license__ = "GPL v2 or later"

# std lib
import sys
import logging
#import os.path


# 3rd party
import wx


# GNUmed libs
if __name__ == '__main__':
	sys.path.insert(0, '../../')

from Gnumed.pycommon import gmTools
from Gnumed.pycommon import gmDispatcher
#from Gnumed.pycommon import gmMimeLib
#from Gnumed.pycommon import gmDateTime
#from Gnumed.pycommon import gmPrinting
#from Gnumed.pycommon import gmShellAPI

from Gnumed.business import gmExternalCare
from Gnumed.business import gmPerson

from Gnumed.wxpython import gmListWidgets
from Gnumed.wxpython import gmEditArea
#from Gnumed.wxpython import gmRegetMixin
#from Gnumed.wxpython import gmGuiHelpers


_log = logging.getLogger('gm.ui')

#============================================================
def manage_external_care(parent=None):

	pat = gmPerson.gmCurrentPatient()
	emr = pat.get_emr()

	if parent is None:
		parent = wx.GetApp().GetTopWindow()

	#-----------------------------------------
	def edit(external_care_item=None):
		return edit_external_care_item(parent = parent, external_care_item = external_care_item)
	#-----------------------------------------
	def delete(external_care_item=None):
		if gmExternalCare.delete_external_care(pk_external_care = external_care_item['pk_external_care']):
			return True

		gmDispatcher.send (
			signal = u'statustext',
			msg = _('Cannot delete external care item.'),
			beep = True
		)
		return False
	#------------------------------------------------------------
	def get_tooltip(data):
		if data is None:
			return None
		return u'\n'.join(data.format(with_health_issue = True))
	#------------------------------------------------------------
	def refresh(lctrl):
		care = emr.get_external_care_items(order_by = u'issue, provider, unit, organization')
		items = [ [
			u'%s @ %s' % (
				c['unit'],
				c['organization']
			),
			gmTools.coalesce(c['provider'], u''),
			c['issue'],
			gmTools.coalesce(c['comment'], u'')
		] for c in care ]
		lctrl.set_string_items(items)
		lctrl.set_data(care)
	#------------------------------------------------------------
	gmListWidgets.get_choices_from_list (
		parent = parent,
		msg = _('External care of this patient.'),
		caption = _('Showing external care network.'),
		columns = [ _('Location'), _('Provider'), _('Care issue'), _('Comment') ],
		single_selection = True,
		can_return_empty = True,
		ignore_OK_button = True,
		refresh_callback = refresh,
		edit_callback = edit,
		new_callback = edit,
		delete_callback = delete,
		list_tooltip_callback = get_tooltip
#		left_extra_button=None,
#		middle_extra_button=None,
#		right_extra_button=None
	)

#----------------------------------------------------------------
def edit_external_care_item(parent=None, external_care_item=None):
	ea = cExternalCareEAPnl(parent = parent, id = -1)
	ea.data = external_care_item
	ea.mode = gmTools.coalesce(external_care_item, 'new', 'edit')
	dlg = gmEditArea.cGenericEditAreaDlg2(parent = parent, id = -1, edit_area = ea, single_entry = True)
	dlg.SetTitle(gmTools.coalesce(external_care_item, _('Adding external care'), _('Editing external care')))
	if dlg.ShowModal() == wx.ID_OK:
		dlg.Destroy()
		return True
	dlg.Destroy()
	return False

#====================================================================
from Gnumed.wxGladeWidgets import wxgExternalCareEAPnl

class cExternalCareEAPnl(wxgExternalCareEAPnl.wxgExternalCareEAPnl, gmEditArea.cGenericEditAreaMixin):

	def __init__(self, *args, **kwargs):

		try:
			data = kwargs['care']
			del kwargs['care']
		except KeyError:
			data = None

		wxgExternalCareEAPnl.wxgExternalCareEAPnl.__init__(self, *args, **kwargs)
		gmEditArea.cGenericEditAreaMixin.__init__(self)

		self.mode = 'new'
		self.data = data
		if data is not None:
			self.mode = 'edit'

		#self.__init_ui()
	#----------------------------------------------------------------
#	def __init_ui(self):
#		# adjust phrasewheels etc
	#----------------------------------------------------------------
	# generic Edit Area mixin API
	#----------------------------------------------------------------
	def _valid_for_save(self):

		# its best to validate bottom -> top such that the
		# cursor ends up in the topmost failing field

		# remove when implemented:
		return False

		validity = True

		if self._TCTRL_xxx.GetValue().strip() == u'':
			validity = False
			self.display_tctrl_as_valid(tctrl = self._TCTRL_xxx, valid = False)
			self.status_message = _('No entry in field xxx.')
			self._TCTRL_xxx.SetFocus()
		else:
			self.display_tctrl_as_valid(tctrl = self._TCTRL_xxx, valid = True)

		if self._PRW_xxx.GetData() is None:
			validity = False
			self._PRW_xxx.display_as_valid(False)
			self.status_message = _('No entry in field xxx.')
			self._PRW_xxx.SetFocus()
		else:
			self._PRW_xxx.display_as_valid(True)

		return validity
	#----------------------------------------------------------------
	def _save_as_new(self):

		# remove when implemented:
		return False

		# save the data as a new instance
		data = gmXXXX.create_xxxx()

		data[''] = self._
		data[''] = self._

		data.save()

		# must be done very late or else the property access
		# will refresh the display such that later field
		# access will return empty values
		self.data = data
		return False
		return True
	#----------------------------------------------------------------
	def _save_as_update(self):

		# remove when implemented:
		return False

		# update self.data and save the changes
		self.data[''] = self._TCTRL_xxx.GetValue().strip()
		self.data[''] = self._PRW_xxx.GetData()
		self.data[''] = self._CHBOX_xxx.GetValue()
		self.data.save()
		return True
	#----------------------------------------------------------------
	def _refresh_as_new(self):
		self._PRW_issue.SetText(u'', None)
		self._PRW_care_location.SetText(u'', None)
		self._TCTRL_provider.SetValue(u'')
		self._TCTRL_comment.SetValue(u'')

		self._PRW_issue.SetFocus()
	#----------------------------------------------------------------
	def _refresh_as_new_from_existing(self):
		self._refresh_as_new()
	#----------------------------------------------------------------
	def _refresh_from_existing(self):
		self._PRW_issue.SetText(value = self.data['issue'], data = self.data['pk_health_issue'], suppress_smarts = True)
		self._PRW_care_location.SetText(value = u'%s @ %s' % (self.data['unit'], self.data['organization']), data = self.data['pk_org_unit'])
		self._TCTRL_provider.SetValue(gmTools.coalesce(self.data['provider']))
		self._TCTRL_comment.SetValue(gmTools.coalesce(self.data['comment']))

		self._TCTRL_comment.SetFocus()
	#----------------------------------------------------------------
