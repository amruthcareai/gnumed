#!/usr/bin/env python
# -*- coding: utf8 -*-
# generated by wxGlade 0.6.3 from "/home/ncq/Projekte/gm-cvs/branches/HEAD/gnumed/gnumed/client/wxg/wxgCurrentMedicationEAPnl.wxg"

import wx

# begin wxGlade: extracode
# end wxGlade



class wxgCurrentMedicationEAPnl(wx.ScrolledWindow):
    def __init__(self, *args, **kwds):

        from Gnumed.wxpython import gmPhraseWheel
        from Gnumed.wxpython import gmEMRStructWidgets
        from Gnumed.wxpython import gmMedicationWidgets

        # begin wxGlade: wxgCurrentMedicationEAPnl.__init__
        kwds["style"] = wx.NO_BORDER|wx.TAB_TRAVERSAL
        wx.ScrolledWindow.__init__(self, *args, **kwds)
        self._LBL_allergies = wx.StaticText(self, -1, "")
        self._PRW_substance = gmMedicationWidgets.cSubstancePhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._BTN_database_substance = wx.Button(self, -1, _("+"), style=wx.BU_EXACTFIT)
        self._PRW_strength = gmPhraseWheel.cPhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._PRW_preparation = gmMedicationWidgets.cSubstancePreparationPhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._CHBOX_approved = wx.CheckBox(self, -1, _("Approved of"))
        self._PRW_brand = gmMedicationWidgets.cBrandedDrugPhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._BTN_database_brand = wx.Button(self, -1, _("+"), style=wx.BU_EXACTFIT)
        self._TCTRL_brand_ingredients = wx.TextCtrl(self, -1, "", style=wx.NO_BORDER)
        self._DP_started = wx.DatePickerCtrl(self, -1, style=wx.DP_DROPDOWN|wx.DP_SHOWCENTURY)
        self._PRW_schedule = gmMedicationWidgets.cSubstanceSchedulePhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._PRW_duration = gmPhraseWheel.cPhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._CHBOX_long_term = wx.CheckBox(self, -1, _("Long-term"))
        self._PRW_aim = gmPhraseWheel.cPhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._PRW_episode = gmEMRStructWidgets.cEpisodeSelectionPhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._PRW_notes = gmPhraseWheel.cPhraseWheel(self, -1, "", style=wx.NO_BORDER)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self._on_get_substance_button_pressed, self._BTN_database_substance)
        self.Bind(wx.EVT_BUTTON, self._on_get_brand_button_pressed, self._BTN_database_brand)
        self.Bind(wx.EVT_CHECKBOX, self._on_chbox_long_term_checked, self._CHBOX_long_term)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: wxgCurrentMedicationEAPnl.__set_properties
        self.SetScrollRate(10, 10)
        self._BTN_database_substance.SetToolTipString(_("Get substances from an external drug database.\n\nNote that if you select more than one substance only the first one will be available for further editing right away."))
        self._PRW_strength.SetToolTipString(_("The amount of substance per dose."))
        self._PRW_preparation.SetToolTipString(_("The preparation the substance comes in."))
        self._CHBOX_approved.SetToolTipString(_("Whether this substance is taken by advice."))
        self._CHBOX_approved.SetValue(1)
        self._PRW_brand.SetToolTipString(_("The brand name of the drug the patient is taking."))
        self._BTN_database_brand.SetToolTipString(_("Get brand(s) from an external drug database.\n\nNote that if you select more than one only the first will be available for further editing right away."))
        self._TCTRL_brand_ingredients.SetToolTipString(_("The active ingredients of this brand."))
        self._TCTRL_brand_ingredients.Enable(False)
        self._DP_started.SetToolTipString(_("When was this substance started to be consumed."))
        self._PRW_schedule.SetToolTipString(_("The schedule for taking this substance."))
        self._PRW_duration.SetToolTipString(_("How long is this substance supposed to be taken."))
        self._CHBOX_long_term.SetToolTipString(_("Whether this substance is to be taken for the rest of the patient's life."))
        self._PRW_aim.SetToolTipString(_("The aim of consuming this substance."))
        self._PRW_episode.SetToolTipString(_("The episode this substance is taken under."))
        self._PRW_notes.SetToolTipString(_("Any clinical notes, comments, or instructions on this substance intake."))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: wxgCurrentMedicationEAPnl.__do_layout
        __szr_main = wx.BoxSizer(wx.VERTICAL)
        _gszr_main = wx.FlexGridSizer(10, 2, 1, 3)
        __szr_duration = wx.BoxSizer(wx.HORIZONTAL)
        __szr_brand = wx.BoxSizer(wx.HORIZONTAL)
        __szr_specs = wx.BoxSizer(wx.HORIZONTAL)
        __szr_substance = wx.BoxSizer(wx.HORIZONTAL)
        __szr_main.Add(self._LBL_allergies, 0, wx.BOTTOM|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5)
        __lbl_substance = wx.StaticText(self, -1, _("Substance"))
        _gszr_main.Add(__lbl_substance, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_substance.Add(self._PRW_substance, 1, wx.RIGHT|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5)
        __szr_substance.Add(self._BTN_database_substance, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(__szr_substance, 1, wx.EXPAND, 0)
        __lbl_specs = wx.StaticText(self, -1, _("Strength"))
        _gszr_main.Add(__lbl_specs, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_specs.Add(self._PRW_strength, 1, wx.RIGHT|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 10)
        __lbl_prep = wx.StaticText(self, -1, _("Preparation"))
        __szr_specs.Add(__lbl_prep, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        __szr_specs.Add(self._PRW_preparation, 1, wx.RIGHT|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 10)
        __szr_specs.Add(self._CHBOX_approved, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(__szr_specs, 1, wx.EXPAND, 0)
        __lbl_brand = wx.StaticText(self, -1, _("Brand"))
        _gszr_main.Add(__lbl_brand, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_brand.Add(self._PRW_brand, 1, wx.RIGHT|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5)
        __szr_brand.Add(self._BTN_database_brand, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(__szr_brand, 1, wx.EXPAND, 0)
        _gszr_main.Add((20, 20), 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(self._TCTRL_brand_ingredients, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_started = wx.StaticText(self, -1, _("Started"))
        _gszr_main.Add(__lbl_started, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(self._DP_started, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 10)
        __lbl_schedule = wx.StaticText(self, -1, _("Schedule"))
        _gszr_main.Add(__lbl_schedule, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(self._PRW_schedule, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_duration = wx.StaticText(self, -1, _("Duration"))
        _gszr_main.Add(__lbl_duration, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_duration.Add(self._PRW_duration, 1, wx.RIGHT|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 10)
        __szr_duration.Add(self._CHBOX_long_term, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 2)
        _gszr_main.Add(__szr_duration, 1, wx.EXPAND, 0)
        __lbl_aim = wx.StaticText(self, -1, _("Aim"))
        _gszr_main.Add(__lbl_aim, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(self._PRW_aim, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_episode = wx.StaticText(self, -1, _("Episode"))
        _gszr_main.Add(__lbl_episode, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(self._PRW_episode, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_notes = wx.StaticText(self, -1, _("Advice"))
        _gszr_main.Add(__lbl_notes, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(self._PRW_notes, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.AddGrowableCol(1)
        __szr_main.Add(_gszr_main, 1, wx.EXPAND, 0)
        self.SetSizer(__szr_main)
        __szr_main.Fit(self)
        # end wxGlade

    def _on_chbox_long_term_checked(self, event): # wxGlade: wxgCurrentMedicationEAPnl.<event_handler>
        print "Event handler `_on_chbox_long_term_checked' not implemented"
        event.Skip()

    def _on_get_brand_button_pressed(self, event): # wxGlade: wxgCurrentMedicationEAPnl.<event_handler>
        print "Event handler `_on_get_brand_button_pressed' not implemented"
        event.Skip()

    def _on_get_substance_button_pressed(self, event): # wxGlade: wxgCurrentMedicationEAPnl.<event_handler>
        print "Event handler `_on_get_substance_button_pressed' not implemented"
        event.Skip()

# end of class wxgCurrentMedicationEAPnl


