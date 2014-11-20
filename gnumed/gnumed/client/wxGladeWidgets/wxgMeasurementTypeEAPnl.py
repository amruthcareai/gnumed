#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 from "/home/ncq/Projekte/gm-cvs/branches/HEAD/gnumed/gnumed/client/wxg/wxgMeasurementTypeEAPnl.wxg"

import wx

# begin wxGlade: extracode
# end wxGlade



class wxgMeasurementTypeEAPnl(wx.ScrolledWindow):
    def __init__(self, *args, **kwds):

        from Gnumed.wxpython import gmPhraseWheel
        from Gnumed.wxpython import gmMeasurementWidgets

        # begin wxGlade: wxgMeasurementTypeEAPnl.__init__
        kwds["style"] = wx.NO_BORDER | wx.TAB_TRAVERSAL
        wx.ScrolledWindow.__init__(self, *args, **kwds)
        self._PRW_name = gmPhraseWheel.cPhraseWheel(self, wx.ID_ANY, "", style=wx.NO_BORDER)
        self._PRW_abbrev = gmPhraseWheel.cPhraseWheel(self, wx.ID_ANY, "", style=wx.NO_BORDER)
        self._PRW_reference_unit = gmMeasurementWidgets.cUnitPhraseWheel(self, wx.ID_ANY, "", style=wx.NO_BORDER)
        self._PRW_loinc = gmPhraseWheel.cPhraseWheel(self, wx.ID_ANY, "", style=wx.NO_BORDER)
        self._TCTRL_loinc_info = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_READONLY | wx.NO_BORDER)
        self._TCTRL_comment_type = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.NO_BORDER)
        self._PRW_test_org = gmMeasurementWidgets.cMeasurementOrgPhraseWheel(self, wx.ID_ANY, "", style=wx.NO_BORDER)
        self._PRW_meta_type = gmMeasurementWidgets.cMetaTestTypePRW(self, wx.ID_ANY, "", style=wx.NO_BORDER)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: wxgMeasurementTypeEAPnl.__set_properties
        self.SetScrollRate(10, 10)
        self._PRW_name.SetToolTipString(_("A descriptive name for this test type."))
        self._PRW_name.SetFocus()
        self._PRW_abbrev.SetToolTipString(_("An abbreviation for the name of this test type."))
        self._PRW_reference_unit.SetToolTipString(_("The base unit to convert results from different labs into when comparing time series."))
        self._PRW_loinc.SetToolTipString(_("The LOINC code corresponding to this test type."))
        self._TCTRL_loinc_info.Enable(False)
        self._TCTRL_comment_type.SetToolTipString(_("A comment on this test type, e.g. pertaining to typical context information."))
        self._PRW_test_org.SetToolTipString(_("The path lab/diagnostic organisation reporting on this test."))
        self._PRW_meta_type.SetToolTipString(_("Select the meta type as which to aggregate for display results with this test type."))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: wxgMeasurementTypeEAPnl.__do_layout
        _gszr_main = wx.FlexGridSizer(7, 2, 1, 3)
        __szr_loinc = wx.BoxSizer(wx.HORIZONTAL)
        __szr_abbrev_unit = wx.BoxSizer(wx.HORIZONTAL)
        __lbl_name = wx.StaticText(self, wx.ID_ANY, _("Name"))
        __lbl_name.SetForegroundColour(wx.Colour(255, 0, 0))
        _gszr_main.Add(__lbl_name, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(self._PRW_name, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_abbrev = wx.StaticText(self, wx.ID_ANY, _("Abbreviation"))
        __lbl_abbrev.SetForegroundColour(wx.Colour(255, 0, 0))
        _gszr_main.Add(__lbl_abbrev, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_abbrev_unit.Add(self._PRW_abbrev, 1, wx.RIGHT | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 10)
        __lbl_unit = wx.StaticText(self, wx.ID_ANY, _("Base unit"))
        __lbl_unit.SetForegroundColour(wx.Colour(255, 0, 0))
        __szr_abbrev_unit.Add(__lbl_unit, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)
        __szr_abbrev_unit.Add(self._PRW_reference_unit, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(__szr_abbrev_unit, 1, wx.EXPAND, 0)
        __lbl_loinc = wx.StaticText(self, wx.ID_ANY, _("LOINC"))
        _gszr_main.Add(__lbl_loinc, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_loinc.Add(self._PRW_loinc, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 10)
        _gszr_main.Add(__szr_loinc, 1, wx.EXPAND, 0)
        _gszr_main.Add((20, 20), 0, wx.EXPAND, 0)
        _gszr_main.Add(self._TCTRL_loinc_info, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_comment_type = wx.StaticText(self, wx.ID_ANY, _("Test comment"))
        _gszr_main.Add(__lbl_comment_type, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(self._TCTRL_comment_type, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_test_org = wx.StaticText(self, wx.ID_ANY, _("Lab"))
        _gszr_main.Add(__lbl_test_org, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(self._PRW_test_org, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 10)
        __lbl_meta_type = wx.StaticText(self, wx.ID_ANY, _("Meta type"))
        _gszr_main.Add(__lbl_meta_type, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(self._PRW_meta_type, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
        self.SetSizer(_gszr_main)
        _gszr_main.Fit(self)
        _gszr_main.AddGrowableCol(1)
        # end wxGlade

# end of class wxgMeasurementTypeEAPnl


