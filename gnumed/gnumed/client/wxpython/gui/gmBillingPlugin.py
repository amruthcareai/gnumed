#======================================================================
# GNUmed billing plugin
#
# @copyright: authors
#======================================================================
__author__ = "Nico Latzer <nl@mnet-online.de>, Karsten Hilbert <Karsten.Hilbert@gmx.net>"
__license__ = 'GPL v2 or later (details at http://www.gnu.org)'

import logging


import wx


from Gnumed.wxpython import gmPlugin
from Gnumed.wxpython import gmBillingWidgets
from Gnumed.wxpython import gmAccessPermissionWidgets


_log = logging.getLogger('gm.billing')

#======================================================================
class gmBillingPlugin(gmPlugin.cNotebookPlugin):

	tab_name = _('Billing')
	required_minimum_role = 'doctor'

	@gmAccessPermissionWidgets.verify_minimum_required_role (
		required_minimum_role,
		activity = _('loading plugin <%s>') % tab_name,
		return_value_on_failure = False,
		fail_silently = False
	)
	def register(self):
		gmPlugin.cNotebookPlugin.register(self)

	def name(self):
		return gmBillingPlugin.tab_name

	def GetWidget(self, parent):
		self._widget = gmBillingWidgets.cBillingPluginPnl(parent, -1)
		return self._widget

	def MenuInfo(self):
		pass

	def can_receive_focus(self):
		if not self._verify_patient_avail():
			return None
		return 1

#======================================================================
if __name__ == '__main__':
    pass
