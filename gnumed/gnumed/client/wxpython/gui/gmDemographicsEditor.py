"""GnuMed demographics editor plugin.
"""
#================================================================
# $Source: /home/ncq/Projekte/cvs2git/vcs-mirror/gnumed/gnumed/client/wxpython/gui/Attic/gmDemographicsEditor.py,v $
# $Id: gmDemographicsEditor.py,v 1.14 2005-05-24 19:59:44 ncq Exp $
__version__ = "$Revision: 1.14 $"
__author__ = "Karsten Hilbert <Karsten.Hilbert@gmx.net>"
__license__ = 'GPL'

from Gnumed.pycommon import gmLog, gmI18N
from Gnumed.wxpython import gmPlugin, gmDemographicsWidgets

gmLog.gmDefLog.Log(gmLog.lInfo, __version__)

#======================================================================
class gmDemographicsEditor(gmPlugin.cNotebookPlugin):
	"""Plugin to encapsulate patient demographics editor."""
	tab_name = _("Patient Details")

	def name (self):
		return gmDemographicsEditor.tab_name

	def GetWidget (self, parent):
		self._widget = gmDemographicsWidgets.cNotebookedPatEditionPanel(parent, -1)
		return self._widget

	def MenuInfo (self):
		return ('patient', 'Edit demographics')

	def can_receive_focus(self):
		# need patient
		if not self._verify_patient_avail():
			return None
		return 1
#================================================================
# MAIN
#----------------------------------------------------------------
if __name__ == '__main__':
	import sys
	from wxPython import wx

	# catch all remaining exceptions
	try:
		application = wx.wxPyWidgetTester(size = (640, 400))
		application.SetWidget(gmDemographicsEditor, -1)
		application.MainLoop()
	except StandardError:
		gmLog.gmDefLog.LogException("unhandled exception caught !", sys.exc_info(), verbose=1)
		# but re-raise them
		raise

#================================================================

# $Log: gmDemographicsEditor.py,v $
# Revision 1.14  2005-05-24 19:59:44  ncq
# - use Carlos' new notebooked demographics editor - ugly but
#   promises to be ready in time for 0.1
#
# Revision 1.13  2005/04/12 10:06:40  ncq
# - fix import
#
# Revision 1.12  2005/02/18 11:16:41  ihaywood
# new demographics UI code won't crash the whole client now ;-)
# still needs much work
# RichardSpace working
#
# Revision 1.11  2004/10/16 22:42:12  sjtan
#
# script for unitesting; guard for unit tests where unit uses gmPhraseWheel; fixup where version of wxPython doesn't allow
# a child widget to be multiply inserted (gmDemographics) ; try block for later versions of wxWidgets that might fail
# the Add (.. w,h, ... ) because expecting Add(.. (w,h) ...)
#
# Revision 1.10  2004/08/24 14:28:42  ncq
# - cleanup
#
# Revision 1.9  2004/08/04 17:16:02  ncq
# - wxNotebookPlugin -> cNotebookPlugin
# - derive cNotebookPluginOld from cNotebookPlugin
# - make cNotebookPluginOld warn on use and implement old
#   explicit "main.notebook.raised_plugin"/ReceiveFocus behaviour
# - ReceiveFocus() -> receive_focus()
#
# Revision 1.8  2004/06/20 16:50:51  ncq
# - carefully fool epydoc
#
# Revision 1.7  2004/06/20 06:49:21  ihaywood
# changes required due to Epydoc's OCD
#
# Revision 1.6  2004/06/13 22:31:49  ncq
# - gb['main.toolbar'] -> gb['main.top_panel']
# - self.internal_name() -> self.__class__.__name__
# - remove set_widget_reference()
# - cleanup
# - fix lazy load in _on_patient_selected()
# - fix lazy load in ReceiveFocus()
# - use self._widget in self.GetWidget()
# - override populate_with_data()
# - use gb['main.notebook.raised_plugin']
#
# Revision 1.5  2004/03/07 22:05:08  ncq
# - some cleanup
#
# Revision 1.4  2004/03/07 13:19:18  ihaywood
# more work on forms
#
# Revision 1.3  2004/02/25 09:46:22  ncq
# - import from pycommon now, not python-common
#
# Revision 1.2  2004/02/18 06:30:30  ihaywood
# Demographics editor now can delete addresses
# Contacts back up on screen.
#
# Revision 1.1  2003/11/17 11:04:34  sjtan
#
# added.
#
# Revision 1.1  2003/10/23 06:02:40  sjtan
#
# manual edit areas modelled after r.terry's specs.
#
# Revision 1.2  2003/07/19 20:22:22  ncq
# - use panel now, not scrolled window anymore
#
# Revision 1.1  2003/07/03 15:26:26  ncq
# - first checkin
#
