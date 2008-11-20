"""gmRegetMixin - GNUmed data change callback mixin.

Widget code can mix in this class as a base class and
thus gain the infrastructure to update it's display
when data changes. If the widget is not visible it will
only schedule refetching data from the business layer.
If it *is* visible it will immediately fetch and redisplay.

You must call cRegetOnPaintMixin.__init__() in your own
__init__() after calling __init__() on the appropriate
wx.Widgets class your widget inherits from.

You must then make sure to call _schedule_data_reget()
whenever you learn of backend data changes. This will
in most cases happen after you receive a gmDispatcher
signal indicating a change in the backend.

The _populate_with_data(self) method must be overriden in the
including class and must return True if the UI was successfully
repopulated with content.

@copyright: authors
"""
#===========================================================================
# $Source: /home/ncq/Projekte/cvs2git/vcs-mirror/gnumed/gnumed/client/wxpython/gmRegetMixin.py,v $
# $Id: gmRegetMixin.py,v 1.29 2008-11-20 20:12:57 ncq Exp $
__version__ = "$Revision: 1.29 $"
__author__ = "K.Hilbert <Karsten.Hilbert@gmx.net>"
__license__ = 'GPL (details at http://www.gnu.org)'

import wx

#===========================================================================
class cRegetOnPaintMixin:
	"""Mixin to add redisplay_data-on-wx.EVT_PAINT aspect.

	Any code mixing in this class will gain the mechanism
	to reget data on wxPaint events. The code must be an
	instance of a wx.Window and must implement a
	_populate_with_data() method. It must also call
	_schedule_data_reget() at appropriate times.
	"""
	def __init__(self):
		self._data_stale = True
		try:
			wx.EVT_PAINT(self, self.__on_paint_event)
		except:
			print 'you likely need to call "cRegetOnPaintMixin.__init__(self)" later in %s__init__()' % self.__class__.__name__
			raise
	#-----------------------------------------------------
	def __on_paint_event(self, event):
		"""Called just before the widget is repainted.

		Checks whether data needs to be refetched.
		"""
		self.__repopulate_ui()
		event.Skip()
	#-----------------------------------------------------
	def __repopulate_ui(self):
		"""Checks whether data must be refetched and does so 

		Called on different occasions such as "notebook page
		raised" or "paint event received".
		"""
		if self._data_stale:
			self._data_stale = not self._populate_with_data()

		return not self._data_stale
	#-----------------------------------------------------
	# API for child classes
	#-----------------------------------------------------
	def _populate_with_data(self):
		"""Actually fills the UI with data.

		This must be overridden in child classes !

		Must return True/False.
		"""
		raise NotImplementedError, "[%s] _populate_with_data() not implemented" % self.__class__.__name__
	#-----------------------------------------------------
	def _schedule_data_reget(self):
		"""Flag data as stale and schedule refetch/redisplay.

		- if not visible schedules refetch only
		- if visible redisplays immediately (virtue of Refresh()
		  calling __on_paint_event() if visible) thereby invoking
		  the actual data refetch

		Called by the child class whenever it learns of data changes
		such as from database listener threads, dispatcher signals etc.
		"""
		self._data_stale = True

		# Master Robin Dunn sayeth this is The Way(tm) but
		# neither this:
		#wx.GetApp().GetTopWindow().Refresh()
		# nor this:
		#top_parent = wx.GetTopLevelParent(self)
		#top_parent.Refresh()
		# appear to work as expected :-(
		# The issues I have with them are:
		# 1) It appears to cause refreshes "too often", eg whenever
		#    *any*  child of self calls this method - but this may
		#    not matter much as only those that have self._data_stale
		#    set to True will trigger backend refetches.
		# 2) Even this does not in all cases cause a proper redraw
		#    of the visible widgets - likely because nothing has
		#    really changed in them, visually.

		# further testing by Hilmar revealed that the
		# following appears to work:
		self.Refresh()
		# the logic should go like this:
		# database insert -> after-insert trigger
		# -> notify
		# -> middleware listener
		# -> flush optional middleware cache
		# -> dispatcher signal to frontend listener*s*
		# -> frontend listeners schedule a data reget and a Refresh()
		# problem: those that are not visible are refreshed, too
		# FIXME: is this last assumption true ?
		return True
	#-----------------------------------------------------
	# notebook plugin API if needed
	#-----------------------------------------------------
	def repopulate_ui(self):
		"""Just a glue method to make this compatible with notebook plugins."""
		self.__repopulate_ui()
#===========================================================================
# main
#---------------------------------------------------------------------------
if __name__ == '__main__':
	print "no unit test available"

#===========================================================================
# $Log: gmRegetMixin.py,v $
# Revision 1.29  2008-11-20 20:12:57  ncq
# - better docs
#
# Revision 1.28  2008/03/29 16:22:47  ncq
# - significant clarification
#
# Revision 1.27  2007/10/29 13:19:07  ncq
# - cleanup
#
# Revision 1.26  2006/05/31 09:48:14  ncq
# - cleanup
#
# Revision 1.25  2006/05/28 16:14:18  ncq
# - cleanup, remove gmLog dependancy, improve docs
# - comment out on-set-focus listening
# - lots of debugging help for the time being
# - add repopulate_ui() for external callers
#
# Revision 1.24  2005/09/28 21:27:30  ncq
# - a lot of wx2.6-ification
#
# Revision 1.23  2005/09/28 15:57:48  ncq
# - a whole bunch of wx.Foo -> wx.Foo
#
# Revision 1.22  2005/09/27 20:44:59  ncq
# - wx.wx* -> wx.*
#
# Revision 1.21  2005/09/26 18:01:51  ncq
# - use proper way to import wx26 vs wx2.4
# - note: THIS WILL BREAK RUNNING THE CLIENT IN SOME PLACES
# - time for fixup
#
# Revision 1.20  2005/08/03 20:02:11  ncq
# - Hilmar eventually seems to have found a way to
#   update data in visible widgets immediately
#
# Revision 1.19  2005/07/31 16:23:27  ncq
# - Hilmar's latest refresh fixes
#
# Revision 1.18  2005/07/27 09:53:30  ncq
# - petty cleanup
#
# Revision 1.17  2005/07/26 19:24:26  hinnef
# - fixed refresh bug on MSW platform
#
# Revision 1.16  2005/06/07 09:05:53  ncq
# - better docs
#
# Revision 1.15  2005/05/29 22:06:19  ncq
# - unsuccessfully try yet another technique for forcing a repaint
#
# Revision 1.14  2005/05/24 19:46:47  ncq
# - call top level window refresh at the end of _schedule_data_reget()
#   which should cause a repaint of the visible widgets, which in turn
#   will cause them to reget data from the business objects which in
#   turn will cause those to reload from the backend, suggested by
#   Robin Dunn
#
# Revision 1.13  2005/05/17 08:07:19  ncq
# - cleanup
#
# Revision 1.12  2005/05/08 21:42:17  ncq
# - import gmLog
#
# Revision 1.11  2005/05/06 15:31:03  ncq
# - slightly improved docs
#
# Revision 1.10  2005/05/05 06:35:02  ncq
# - add some device context measurements in _schedule_data_reget
#   so we can maybe find a way to detect whether we are indeed
#   visible or obscured
#
# Revision 1.9  2005/04/30 13:32:14  sjtan
#
# if current wxWindow that inherits gmRegetMixin IsShown() is true, then it requires
# refresh, so Reget is not scheduled , but immediate.
#
# Revision 1.8  2005/03/20 17:51:41  ncq
# - although not sure whether conceptually it's the right thing to do it
#   sure seems appropriated to Refresh() on focus events
#
# Revision 1.7  2005/01/13 14:27:33  ncq
# - grammar fix
#
# Revision 1.6  2004/10/17 15:52:21  ncq
# - cleanup
#
# Revision 1.5  2004/10/17 00:05:36  sjtan
#
# fixup for paint event re-entry when notification dialog occurs over medDocTree graphics
# area, and triggers another paint event, and another notification dialog , in a loop.
# Fixup is set flag to stop _repopulate_tree, and to only unset this flag when
# patient activating signal gmMedShowDocs to schedule_reget, which is overridden
# to include resetting of flag, before calling mixin schedule_reget.
#
# Revision 1.4  2004/09/05 14:55:19  ncq
# - improve comments, some cleanup
#
# Revision 1.3  2004/08/04 17:12:06  ncq
# - fix comment
#
# Revision 1.2  2004/08/02 17:52:54  hinnef
# Added hint to _repopulate_with_data return value
#
# Revision 1.1  2004/07/28 15:27:31  ncq
# - first checkin, used in gmVaccWidget
#
#
