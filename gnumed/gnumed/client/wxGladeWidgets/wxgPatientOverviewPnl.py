# -*- coding: UTF-8 -*-
#
# generated by wxGlade
#

import wx

# begin wxGlade: dependencies
import gettext
# end wxGlade

# begin wxGlade: extracode
from Gnumed.wxpython.gmListWidgets import cReportListCtrl
from Gnumed.wxpython.gmDateTimeInput import cIntervalPhraseWheel
# end wxGlade


class wxgPatientOverviewPnl(wx.ScrolledWindow):
	def __init__(self, *args, **kwds):
		# begin wxGlade: wxgPatientOverviewPnl.__init__
		kwds["style"] = kwds.get("style", 0) | wx.TAB_TRAVERSAL
		wx.ScrolledWindow.__init__(self, *args, **kwds)
		self.SetSize((300, 300))
		self._LCTRL_identity = cReportListCtrl(self, wx.ID_ANY, style=wx.BORDER_SIMPLE | wx.LC_NO_HEADER | wx.LC_REPORT)
		self._LCTRL_contacts = cReportListCtrl(self, wx.ID_ANY, style=wx.BORDER_SIMPLE | wx.LC_NO_HEADER | wx.LC_REPORT)
		self._LCTRL_encounters = cReportListCtrl(self, wx.ID_ANY, style=wx.BORDER_SIMPLE | wx.LC_NO_HEADER | wx.LC_REPORT)
		self._LCTRL_meds = cReportListCtrl(self, wx.ID_ANY, style=wx.BORDER_SIMPLE | wx.LC_NO_HEADER | wx.LC_REPORT)
		self._LCTRL_problems = cReportListCtrl(self, wx.ID_ANY, style=wx.BORDER_SIMPLE | wx.LC_NO_HEADER | wx.LC_REPORT)
		self._LCTRL_history = cReportListCtrl(self, wx.ID_ANY, style=wx.BORDER_SIMPLE | wx.LC_NO_HEADER | wx.LC_REPORT)
		self._LCTRL_inbox = cReportListCtrl(self, wx.ID_ANY, style=wx.BORDER_SIMPLE | wx.LC_NO_HEADER | wx.LC_REPORT)
		self._LCTRL_results = cReportListCtrl(self, wx.ID_ANY, style=wx.BORDER_SIMPLE | wx.LC_NO_HEADER | wx.LC_REPORT)
		self._LCTRL_documents = cReportListCtrl(self, wx.ID_ANY, style=wx.BORDER_SIMPLE | wx.LC_NO_HEADER | wx.LC_REPORT)

		self.__set_properties()
		self.__do_layout()
		# end wxGlade

	def __set_properties(self):
		# begin wxGlade: wxgPatientOverviewPnl.__set_properties
		self.SetSize((300, 300))
		self.SetScrollRate(10, 10)
		self._LCTRL_problems.SetBackgroundColour(wx.Colour(255, 238, 180))
		# end wxGlade

	def __do_layout(self):
		# begin wxGlade: wxgPatientOverviewPnl.__do_layout
		self._SZR_main = wx.BoxSizer(wx.HORIZONTAL)
		__szr_right = wx.BoxSizer(wx.VERTICAL)
		__szr_middle = wx.BoxSizer(wx.VERTICAL)
		__szr_left = wx.BoxSizer(wx.VERTICAL)
		__lbl_identity = wx.StaticText(self, wx.ID_ANY, _("Identity:"))
		__szr_left.Add(__lbl_identity, 0, wx.ALIGN_CENTER_VERTICAL | wx.BOTTOM, 3)
		__szr_left.Add(self._LCTRL_identity, 1, wx.BOTTOM | wx.EXPAND, 5)
		__lbl_contacts = wx.StaticText(self, wx.ID_ANY, _("Contacts:"))
		__szr_left.Add(__lbl_contacts, 0, wx.ALIGN_CENTER_VERTICAL | wx.BOTTOM, 3)
		__szr_left.Add(self._LCTRL_contacts, 1, wx.BOTTOM | wx.EXPAND, 5)
		__lbl_encounters = wx.StaticText(self, wx.ID_ANY, _("Activity:"))
		__szr_left.Add(__lbl_encounters, 0, wx.ALIGN_CENTER_VERTICAL | wx.BOTTOM, 1)
		__szr_left.Add(self._LCTRL_encounters, 1, wx.EXPAND, 5)
		self._SZR_main.Add(__szr_left, 1, wx.EXPAND | wx.RIGHT, 5)
		__lbl_meds = wx.StaticText(self, wx.ID_ANY, _("Current meds and substances:"))
		__szr_middle.Add(__lbl_meds, 0, wx.ALIGN_CENTER_VERTICAL | wx.BOTTOM, 3)
		__szr_middle.Add(self._LCTRL_meds, 2, wx.BOTTOM | wx.EXPAND, 5)
		__lbl_problem_list = wx.StaticText(self, wx.ID_ANY, _("Active Problems:"))
		__szr_middle.Add(__lbl_problem_list, 0, wx.ALIGN_CENTER_VERTICAL | wx.BOTTOM, 3)
		__szr_middle.Add(self._LCTRL_problems, 2, wx.BOTTOM | wx.EXPAND, 5)
		__lbl_history = wx.StaticText(self, wx.ID_ANY, _("History:"))
		__szr_middle.Add(__lbl_history, 0, wx.ALIGN_CENTER_VERTICAL | wx.BOTTOM, 3)
		__szr_middle.Add(self._LCTRL_history, 3, wx.EXPAND, 5)
		self._SZR_main.Add(__szr_middle, 1, wx.EXPAND | wx.RIGHT, 5)
		__lbl_inbox = wx.StaticText(self, wx.ID_ANY, _("Reminders:"))
		__szr_right.Add(__lbl_inbox, 0, wx.ALIGN_CENTER_VERTICAL | wx.BOTTOM, 3)
		__szr_right.Add(self._LCTRL_inbox, 3, wx.BOTTOM | wx.EXPAND, 5)
		__lbl_measurements = wx.StaticText(self, wx.ID_ANY, _("Measurements:"))
		__szr_right.Add(__lbl_measurements, 0, wx.ALIGN_CENTER_VERTICAL | wx.BOTTOM, 3)
		__szr_right.Add(self._LCTRL_results, 2, wx.BOTTOM | wx.EXPAND, 5)
		__lbl_documents = wx.StaticText(self, wx.ID_ANY, _("Documents:"))
		__szr_right.Add(__lbl_documents, 0, wx.ALIGN_CENTER_VERTICAL | wx.BOTTOM, 3)
		__szr_right.Add(self._LCTRL_documents, 2, wx.EXPAND, 5)
		self._SZR_main.Add(__szr_right, 1, wx.EXPAND, 0)
		self.SetSizer(self._SZR_main)
		self.Layout()
		# end wxGlade

# end of class wxgPatientOverviewPnl
