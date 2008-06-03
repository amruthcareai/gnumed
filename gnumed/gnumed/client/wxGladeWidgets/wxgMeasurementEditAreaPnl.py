#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
# generated by wxGlade 0.6.3 from "/home/ncq/Projekte/gm-cvs/branches/HEAD/gnumed/gnumed/client/wxg/wxgMeasurementEditAreaPnl.wxg"

import wx

# begin wxGlade: extracode
# end wxGlade



class wxgMeasurementEditAreaPnl(wx.ScrolledWindow):
    def __init__(self, *args, **kwds):

        from Gnumed.wxpython import gmDateTimeInput, gmMeasurementWidgets, gmProviderInboxWidgets, gmEMRStructWidgets

        # begin wxGlade: wxgMeasurementEditAreaPnl.__init__
        kwds["style"] = wx.NO_BORDER|wx.TAB_TRAVERSAL
        wx.ScrolledWindow.__init__(self, *args, **kwds)
        self._DPRW_evaluated = gmDateTimeInput.cFuzzyTimestampInput(self, -1, "", style=wx.NO_BORDER)
        self._PRW_test = gmMeasurementWidgets.cMeasurementTypePhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._TCTRL_result = wx.TextCtrl(self, -1, "", style=wx.NO_BORDER)
        self._PRW_units = gmMeasurementWidgets.cUnitPhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._PRW_abnormality_indicator = wx.TextCtrl(self, -1, "", style=wx.NO_BORDER)
        self._TCTRL_note_test_org = wx.TextCtrl(self, -1, "", style=wx.NO_BORDER)
        self._PRW_intended_reviewer = gmProviderInboxWidgets.cProviderPhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._PRW_problem = gmEMRStructWidgets.cEpisodeSelectionPhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._TCTRL_narrative = wx.TextCtrl(self, -1, "", style=wx.NO_BORDER)
        self._TCTRL_normal_min = wx.TextCtrl(self, -1, "", style=wx.NO_BORDER)
        self._TCTRL_normal_max = wx.TextCtrl(self, -1, "", style=wx.NO_BORDER)
        self._TCTRL_normal_range = wx.TextCtrl(self, -1, "", style=wx.NO_BORDER)
        self._TCTRL_target_min = wx.TextCtrl(self, -1, "", style=wx.NO_BORDER)
        self._TCTRL_target_max = wx.TextCtrl(self, -1, "", style=wx.NO_BORDER)
        self._TCTRL_target_range = wx.TextCtrl(self, -1, "", style=wx.NO_BORDER)
        self._TCTRL_norm_ref_group = wx.TextCtrl(self, -1, "", style=wx.NO_BORDER)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: wxgMeasurementEditAreaPnl.__set_properties
        self.SetScrollRate(10, 10)
        self._DPRW_evaluated.SetToolTipString(_("When was this result actually obtained. Usually the same or between the time for \"sample taken\" and \"result reported\"."))
        self._PRW_test.SetToolTipString(_("The type of measurement or test this result is about."))
        self._PRW_test.SetFocus()
        self._TCTRL_result.SetToolTipString(_("The result of the measurement. Numeric and alphanumeric input is allowed."))
        self._PRW_units.SetToolTipString(_("The units this result comes in."))
        self._PRW_abnormality_indicator.SetToolTipString(_("Enter an indicator for the degree of abnormality.\nOften +, -, !, ?, () or any combination thereof."))
        self._TCTRL_note_test_org.SetToolTipString(_("A technical comment on the result.\nUsually by the entering Medical Technical Assistant."))
        self._PRW_intended_reviewer.SetToolTipString(_("The doctor in charge who will have to assess and sign off this result."))
        self._PRW_problem.SetToolTipString(_("The medical problem this test results pertains to."))
        self._TCTRL_narrative.SetToolTipString(_("A clinical assessment of the measurement.\nUsually by a doctor."))
        self._TCTRL_normal_min.SetToolTipString(_("The lower bound of the range of technically normal values."))
        self._TCTRL_normal_max.SetToolTipString(_("The upper bound of the range of technically normal values."))
        self._TCTRL_normal_range.SetToolTipString(_("An alphanumeric range of technically normal values."))
        self._TCTRL_target_min.SetToolTipString(_("The lower bound of the target range for this test in this patient."))
        self._TCTRL_target_max.SetToolTipString(_("The lower bound of the target range for this test in this patient."))
        self._TCTRL_target_range.SetToolTipString(_("An alphanumeric target range for this test in this patient."))
        self._TCTRL_norm_ref_group.SetToolTipString(_("The reference group the normal range for this value pertains to."))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: wxgMeasurementEditAreaPnl.__do_layout
        _gszr_main = wx.FlexGridSizer(15, 2, 1, 3)
        __szr_range_target = wx.BoxSizer(wx.HORIZONTAL)
        __szr_range_normal = wx.BoxSizer(wx.HORIZONTAL)
        __szr_normality = wx.BoxSizer(wx.HORIZONTAL)
        __szr_result = wx.BoxSizer(wx.HORIZONTAL)
        _gszr_main.Add((20, 20), 0, wx.EXPAND, 0)
        __lbl_result_details = wx.StaticText(self, -1, _("Measurement details"))
        __lbl_result_details.SetForegroundColour(wx.Colour(95, 159, 159))
        _gszr_main.Add(__lbl_result_details, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_evaluated = wx.StaticText(self, -1, _("Date"))
        __lbl_evaluated.SetForegroundColour(wx.Colour(204, 50, 50))
        _gszr_main.Add(__lbl_evaluated, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(self._DPRW_evaluated, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_test = wx.StaticText(self, -1, _("Test"))
        __lbl_test.SetForegroundColour(wx.Colour(204, 50, 50))
        _gszr_main.Add(__lbl_test, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(self._PRW_test, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_result = wx.StaticText(self, -1, _("Value"))
        __lbl_result.SetForegroundColour(wx.Colour(204, 50, 50))
        _gszr_main.Add(__lbl_result, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_result.Add(self._TCTRL_result, 2, wx.RIGHT|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5)
        __lbl_unit = wx.StaticText(self, -1, _("Units"))
        __lbl_unit.SetForegroundColour(wx.Colour(204, 50, 50))
        __szr_result.Add(__lbl_unit, 0, wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 3)
        __szr_result.Add(self._PRW_units, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(__szr_result, 1, wx.EXPAND, 0)
        __lbl_abnormality = wx.StaticText(self, -1, _("Indicator"))
        _gszr_main.Add(__lbl_abnormality, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_normality.Add(self._PRW_abnormality_indicator, 1, wx.RIGHT|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5)
        __lbl_note_test_org = wx.StaticText(self, -1, _("Comment:"))
        __szr_normality.Add(__lbl_note_test_org, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 3)
        __szr_normality.Add(self._TCTRL_note_test_org, 3, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(__szr_normality, 1, wx.EXPAND, 0)
        _gszr_main.Add((20, 20), 0, wx.EXPAND, 0)
        __lbl_clinical_assessment = wx.StaticText(self, -1, _("Clinical Assessment"))
        __lbl_clinical_assessment.SetForegroundColour(wx.Colour(95, 159, 159))
        _gszr_main.Add(__lbl_clinical_assessment, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_in_charge = wx.StaticText(self, -1, _("In charge"))
        __lbl_in_charge.SetForegroundColour(wx.Colour(204, 50, 50))
        _gszr_main.Add(__lbl_in_charge, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(self._PRW_intended_reviewer, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_problem = wx.StaticText(self, -1, _("Problem"))
        __lbl_problem.SetForegroundColour(wx.Colour(204, 50, 50))
        _gszr_main.Add(__lbl_problem, 0, wx.ALIGN_CENTER_VERTICAL, 3)
        _gszr_main.Add(self._PRW_problem, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5)
        __lbl_narrative = wx.StaticText(self, -1, _("Note"))
        _gszr_main.Add(__lbl_narrative, 0, wx.ALIGN_CENTER_VERTICAL, 3)
        _gszr_main.Add(self._TCTRL_narrative, 2, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add((20, 20), 0, wx.EXPAND, 0)
        __lbl_reference = wx.StaticText(self, -1, _("Reference information"))
        __lbl_reference.SetForegroundColour(wx.Colour(95, 159, 159))
        _gszr_main.Add(__lbl_reference, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_range_normal = wx.StaticText(self, -1, _("Normal"))
        _gszr_main.Add(__lbl_range_normal, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_range_normal.Add(self._TCTRL_normal_min, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_from_to = wx.StaticText(self, -1, _("--"))
        __szr_range_normal.Add(__lbl_from_to, 0, wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 3)
        __szr_range_normal.Add(self._TCTRL_normal_max, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_range_or_range = wx.StaticText(self, -1, _("or"))
        __szr_range_normal.Add(__lbl_range_or_range, 0, wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        __szr_range_normal.Add(self._TCTRL_normal_range, 2, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5)
        _gszr_main.Add(__szr_range_normal, 1, wx.EXPAND, 0)
        __lbl_range_target = wx.StaticText(self, -1, _("Target"))
        _gszr_main.Add(__lbl_range_target, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_range_target.Add(self._TCTRL_target_min, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_from_to_target = wx.StaticText(self, -1, _("--"))
        __szr_range_target.Add(__lbl_from_to_target, 0, wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 3)
        __szr_range_target.Add(self._TCTRL_target_max, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_range_or_range_target = wx.StaticText(self, -1, _("or"))
        __szr_range_target.Add(__lbl_range_or_range_target, 0, wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        __szr_range_target.Add(self._TCTRL_target_range, 2, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5)
        _gszr_main.Add(__szr_range_target, 1, wx.EXPAND, 0)
        __lbl_ref_group = wx.StaticText(self, -1, _("Group"))
        _gszr_main.Add(__lbl_ref_group, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(self._TCTRL_norm_ref_group, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        self.SetSizer(_gszr_main)
        _gszr_main.Fit(self)
        _gszr_main.AddGrowableCol(1)
        # end wxGlade

# end of class wxgMeasurementEditAreaPnl


