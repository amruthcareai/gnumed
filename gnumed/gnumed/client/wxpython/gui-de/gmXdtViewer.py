#!/usr/bin/env python

#=============================================================================
# $Source: /home/ncq/Projekte/cvs2git/vcs-mirror/gnumed/gnumed/client/wxpython/gui-de/Attic/gmXdtViewer.py,v $
# $Id: gmXdtViewer.py,v 1.1 2003-02-13 15:25:15 ncq Exp $
__version__ = "$Revision: 1.1 $"
__author__ = "S.Hilbert, K.Hilbert"

import sys,os,fileinput,string,linecache
#modules = {}
# location of our modules
sys.path.append(os.path.join('..', '..', 'python-common'))
sys.path.append(os.path.join('..', '..', 'business'))

import gmLog
#<DEBUG>
gmLog.gmDefLog.SetAllLogLevels(gmLog.lData)
#</DEBUG>
_log = gmLog.gmDefLog

from wxPython.wx import *
from wxPython.lib.mixins.listctrl import wxColumnSorterMixin, wxListCtrlAutoWidthMixin

import gmCLI
from gmXdtMappings import xdt_id_map, xdt_packet_type_map
#=============================================================================
class gmXdtListCtrl(wxListCtrl, wxListCtrlAutoWidthMixin):
	def __init__(self, parent, ID, pos=wxDefaultPosition, size=wxDefaultSize, style=0):
		wxListCtrl.__init__(self, parent, ID, pos, size, style)
		wxListCtrlAutoWidthMixin.__init__(self)
#=============================================================================
class gmXdtViewerPanel(wxPanel):
	def __init__(self, parent):
		wxPanel.__init__(self, parent, -1, style=wxWANTS_CHARS)

		tID = wxNewId()

		self.list = gmXdtListCtrl(
			self,
			tID,
			style=wxLC_REPORT|wxSUNKEN_BORDER|wxLC_VRULES)#|wxLC_HRULES)

		self.PopulateList()

		EVT_SIZE(self, self.OnSize)
		EVT_LIST_ITEM_SELECTED(self, tID, self.OnItemSelected)
		EVT_LIST_ITEM_DESELECTED(self, tID, self.OnItemDeselected)
		EVT_LIST_ITEM_ACTIVATED(self, tID, self.OnItemActivated)
		EVT_LIST_DELETE_ITEM(self, tID, self.OnItemDelete)
		EVT_LIST_COL_CLICK(self, tID, self.OnColClick)
		EVT_LIST_COL_RIGHT_CLICK(self, tID, self.OnColRightClick)
		EVT_LIST_COL_BEGIN_DRAG(self, tID, self.OnColBeginDrag)
		EVT_LIST_COL_DRAGGING(self, tID, self.OnColDragging)
		EVT_LIST_COL_END_DRAG(self, tID, self.OnColEndDrag)

		EVT_LEFT_DCLICK(self.list, self.OnDoubleClick)
		EVT_RIGHT_DOWN(self.list, self.OnRightDown)

		# for wxMSW
		EVT_COMMAND_RIGHT_CLICK(self.list, tID, self.OnRightClick)

		# for wxGTK
		EVT_RIGHT_UP(self.list, self.OnRightClick)
	#-------------------------------------------------------------------------
	def PopulateList(self):
		# for normal, simple columns, you can add them like this:
		self.list.InsertColumn(0, "Feldart")
		self.list.InsertColumn(1, "Feldinhalt")

		items = self.__decode_xdt()
		for item_idx in range(len(items),0,-1):
			data = items[item_idx]
			idx = self.list.InsertItem(info=wxListItem())
			self.list.SetStringItem(index=idx, col=0, label=data[0])
			self.list.SetStringItem(index=idx, col=1, label=data[1])
			#self.list.SetItemData(item_idx, item_idx)

		self.list.SetColumnWidth(0, wxLIST_AUTOSIZE)
		self.list.SetColumnWidth(1, wxLIST_AUTOSIZE)

		# show how to select an item
		#self.list.SetItemState(5, wxLIST_STATE_SELECTED, wxLIST_STATE_SELECTED)

		# show how to change the colour of a couple items
		#item = self.list.GetItem(1)
		#item.SetTextColour(wxBLUE)
		#self.list.SetItem(item)
		#item = self.list.GetItem(4)
		#item.SetTextColour(wxRED)
		#self.list.SetItem(item)

		self.currentItem = 0
	#-------------------------------------------------------------------------
	def __decode_xdt(self):
		cfgName = ""
		# has the user manually supplied a config file on the command line ?
		if gmCLI.has_arg('--file'):
			cfgName = gmCLI.arg['--file']
			_log.Log(gmLog.lData, '--file=%s' % cfgName)
			# file valid ?
			if os.path.exists(cfgName):
				_log.Log(gmLog.lData, 'Found file [%s].' % cfgName)
			else:
				_log.Log(gmLog.lErr, "file [%s] not found. Aborting." % cfgName)
		else:
			_log.Log(gmLog.lData, "No config file given on command line. Format: --file=<file>")
			return None

		xDTFile = fileinput.input(cfgName)
		items = {}
		i = 1
		for line in xDTFile:
			# remove trailing CR and/or LF
			line = string.replace(line,'\015','')
			line = string.replace(line,'\012','') 
			length ,ID, content = line[:3], line[3:7], line[7:]

			if ID == '8000':
				tmp = xdt_packet_type_map[content]
				content = tmp
			try:
				items[i] = (xdt_id_map[ID], content)
			except:
				pass
			i = i + 1

		fileinput.close()
		return items
	#-------------------------------------------------------------------------
	def OnRightDown(self, event):
		self.x = event.GetX()
		self.y = event.GetY()
		item, flags = self.list.HitTest((self.x, self.y))
		if flags & wxLIST_HITTEST_ONITEM:
			self.list.Select(item)
		event.Skip()
	#-------------------------------------------------------------------------
	def getColumnText(self, index, col):
		item = self.list.GetItem(index, col)
		return item.GetText()
	#-------------------------------------------------------------------------
	def OnItemSelected(self, event):
		self.currentItem = event.m_itemIndex
	#-------------------------------------------------------------------------
	def OnItemDeselected(self, evt):
		item = evt.GetItem()

		# Show how to reselect something we don't want deselected
		if evt.m_itemIndex == 11:
			wxCallAfter(self.list.SetItemState, 11, wxLIST_STATE_SELECTED, wxLIST_STATE_SELECTED)
	#-------------------------------------------------------------------------
	def OnItemActivated(self, event):
		self.currentItem = event.m_itemIndex
	#-------------------------------------------------------------------------
	def OnItemDelete(self, event):
		pass
	#-------------------------------------------------------------------------
	def OnColClick(self, event):
		pass
	#-------------------------------------------------------------------------
	def OnColRightClick(self, event):
		item = self.list.GetColumn(event.GetColumn())
	#-------------------------------------------------------------------------
	def OnColBeginDrag(self, event):
		pass
		## Show how to not allow a column to be resized
		#if event.GetColumn() == 0:
		#    event.Veto()
	#-------------------------------------------------------------------------
	def OnColDragging(self, event):
		pass
	#-------------------------------------------------------------------------
	def OnColEndDrag(self, event):
		pass
	#-------------------------------------------------------------------------
	def OnDoubleClick(self, event):
		event.Skip()
	#-------------------------------------------------------------------------
	def OnRightClick(self, event):
		return
		menu = wxMenu()
		tPopupID1 = 0
		tPopupID2 = 1
		tPopupID3 = 2
		tPopupID4 = 3
		tPopupID5 = 5

		# Show how to put an icon in the menu
		item = wxMenuItem(menu, tPopupID1,"One")
		item.SetBitmap(images.getSmilesBitmap())

		menu.AppendItem(item)
		menu.Append(tPopupID2, "Two")
		menu.Append(tPopupID3, "ClearAll and repopulate")
		menu.Append(tPopupID4, "DeleteAllItems")
		menu.Append(tPopupID5, "GetItem")
		EVT_MENU(self, tPopupID1, self.OnPopupOne)
		EVT_MENU(self, tPopupID2, self.OnPopupTwo)
		EVT_MENU(self, tPopupID3, self.OnPopupThree)
		EVT_MENU(self, tPopupID4, self.OnPopupFour)
		EVT_MENU(self, tPopupID5, self.OnPopupFive)
		self.PopupMenu(menu, wxPoint(self.x, self.y))
		menu.Destroy()
		event.Skip()
	#-------------------------------------------------------------------------
	def OnPopupOne(self, event):
		print "FindItem:", self.list.FindItem(-1, "Roxette")
		print "FindItemData:", self.list.FindItemData(-1, 11)
	#-------------------------------------------------------------------------
	def OnPopupTwo(self, event):
		pass
	#-------------------------------------------------------------------------
	def OnPopupThree(self, event):
		self.list.ClearAll()
		wxCallAfter(self.PopulateList)
		#wxYield()
		#self.PopulateList()
	#-------------------------------------------------------------------------
	def OnPopupFour(self, event):
		self.list.DeleteAllItems()
	#-------------------------------------------------------------------------
	def OnPopupFive(self, event):
		item = self.list.GetItem(self.currentItem)
		print item.m_text, item.m_itemId, self.list.GetItemData(self.currentItem)
	#-------------------------------------------------------------------------
	def OnSize(self, event):
		w,h = self.GetClientSizeTuple()
		self.list.SetDimensions(0, 0, w, h)
#=============================================================================
class gmBDT(wxPanel):
    def __init__(self, parent):
    
	    self.contentlist = []
    	    # begin wxGlade: wxPanel.__init__
	    wxPanel.__init__(self, parent, -1)
	    self.LBOX_data = wxListBox(self, -1,size=(200,500), choices=[])
    	    self.__set_properties()
    	    self.__do_layout()
	    self.__decodeBDT()

    def __set_properties(self):
    	    # begin wxGlade: MyPanel.__set_properties
    	    self.LBOX_data.SetSelection(0)
    	    # end wxGlade

    def __do_layout(self):
    	    # begin wxGlade: MyPanel.__do_layout
    	    sizer_1 = wxBoxSizer(wxHORIZONTAL)
    	    sizer_1.Add(self.LBOX_data, 0, 0, 0)
    	    self.SetAutoLayout(1)
    	    self.SetSizer(sizer_1)
    	    sizer_1.Fit(self)
    	    sizer_1.SetSizeHints(self)
    	    self.Layout()
    	    # end wxGlade

#======================================================
# main
#------------------------------------------------------
if __name__ == '__main__':
	try:
		application = wxPyWidgetTester(size=(800,600))
		application.SetWidget(gmXdtViewerPanel)
		application.MainLoop()
	except:
		exc = sys.exc_info()
		_log.LogException('Unhandled exception.', exc, fatal=1)
		raise
else:
	import gmPlugin

	class gmBDT(gmPlugin.wxNotebookPlugin):
		def name (self):
			return _("BDT")

		def GetWidget (self, parent):
			return gmBDT (parent)

		def MenuInfo (self):
			return ('tools', _('&show BDT'))
#=============================================================================
# $Log: gmXdtViewer.py,v $
# Revision 1.1  2003-02-13 15:25:15  ncq
# - first version, works standalone only
#
