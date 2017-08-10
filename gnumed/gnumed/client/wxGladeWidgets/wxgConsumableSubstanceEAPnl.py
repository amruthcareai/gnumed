#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.6.8
#

import wx

# begin wxGlade: dependencies
import gettext
# end wxGlade

# begin wxGlade: extracode
from Gnumed.wxpython.gmTextCtrl import cTextCtrl
from Gnumed.wxpython.gmMeasurementWidgets import cUnitPhraseWheel
from Gnumed.wxpython.gmSubstanceMgmtWidgets import cATCPhraseWheel
# end wxGlade


class wxgConsumableSubstanceEAPnl(wx.ScrolledWindow):
	def __init__(self, *args, **kwds):
		# begin wxGlade: wxgConsumableSubstanceEAPnl.__init__
		kwds["style"] = wx.NO_BORDER | wx.TAB_TRAVERSAL
		wx.ScrolledWindow.__init__(self, *args, **kwds)
		self._TCTRL_substance = cTextCtrl(self, wx.ID_ANY, "", style=wx.NO_BORDER)
		self._TCTRL_amount = cTextCtrl(self, wx.ID_ANY, "", style=wx.NO_BORDER)
		self._PRW_unit = cUnitPhraseWheel(self, wx.ID_ANY, "", style=wx.NO_BORDER)
		self._HL_atc_list = wx.HyperlinkCtrl(self, wx.ID_ANY, _("ATC Code"), _("http://www.whocc.no/atc_ddd_index/"), style=wx.HL_ALIGN_CENTRE | wx.HL_CONTEXTMENU | wx.HL_DEFAULT_STYLE)
		self._PRW_atc = cATCPhraseWheel(self, wx.ID_ANY, "", style=wx.NO_BORDER)

		self.__set_properties()
		self.__do_layout()
		# end wxGlade

	def __set_properties(self):
		# begin wxGlade: wxgConsumableSubstanceEAPnl.__set_properties
		self.SetScrollRate(10, 10)
		self._TCTRL_substance.SetToolTipString(_("Enter the name of the consumable substance.\n\nExamples:\n- metoprolol\n- tobacco\n- alcohol\n- marihuana\n- aloe vera\n- ibuprofen"))
		self._TCTRL_amount.SetToolTipString(_("Enter the amount of substance."))
		self._HL_atc_list.SetToolTipString(_("Browse ATC list."))
		# end wxGlade

	def __do_layout(self):
		# begin wxGlade: wxgConsumableSubstanceEAPnl.__do_layout
		_gszr_main = wx.FlexGridSizer(3, 2, 1, 3)
		__szr_amount = wx.BoxSizer(wx.HORIZONTAL)
		__lbl_substance = wx.StaticText(self, wx.ID_ANY, _("Substance"))
		__lbl_substance.SetForegroundColour(wx.Colour(255, 0, 0))
		_gszr_main.Add(__lbl_substance, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		_gszr_main.Add(self._TCTRL_substance, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
		__lbl_amount = wx.StaticText(self, wx.ID_ANY, _("Amount"))
		__lbl_amount.SetForegroundColour(wx.Colour(255, 0, 0))
		_gszr_main.Add(__lbl_amount, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		__szr_amount.Add(self._TCTRL_amount, 1, wx.RIGHT | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 10)
		__lbl_unit = wx.StaticText(self, wx.ID_ANY, _("Unit:"))
		__lbl_unit.SetForegroundColour(wx.Colour(255, 0, 0))
		__szr_amount.Add(__lbl_unit, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)
		__szr_amount.Add(self._PRW_unit, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
		_gszr_main.Add(__szr_amount, 1, wx.EXPAND, 0)
		_gszr_main.Add(self._HL_atc_list, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		_gszr_main.Add(self._PRW_atc, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
		self.SetSizer(_gszr_main)
		_gszr_main.Fit(self)
		_gszr_main.AddGrowableCol(1)
		# end wxGlade

# end of class wxgConsumableSubstanceEAPnl