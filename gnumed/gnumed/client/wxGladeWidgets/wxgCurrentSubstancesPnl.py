#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 from "/home/ncq/Projekte/gm-cvs/branches/HEAD/gnumed/gnumed/client/wxg/wxgCurrentSubstancesPnl.wxg"

import wx
import wx.grid

# begin wxGlade: extracode
# end wxGlade



class wxgCurrentSubstancesPnl(wx.ScrolledWindow):
    def __init__(self, *args, **kwds):

        from Gnumed.wxpython import gmMedicationWidgets

        # begin wxGlade: wxgCurrentSubstancesPnl.__init__
        kwds["style"] = wx.NO_BORDER|wx.TAB_TRAVERSAL
        wx.ScrolledWindow.__init__(self, *args, **kwds)
        self._RBTN_episode = wx.RadioButton(self, -1, _("Episode"))
        self._RBTN_brand = wx.RadioButton(self, -1, _("Brand"))
        self._CHBOX_show_inactive = wx.CheckBox(self, -1, _("Inactive"))
        self._CHBOX_show_unapproved = wx.CheckBox(self, -1, _("Unapproved"))
        self._grid_substances = gmMedicationWidgets.cCurrentSubstancesGrid(self, -1, size=(1, 1))
        self._BTN_add = wx.Button(self, wx.ID_ADD, "", style=wx.BU_EXACTFIT)
        self._BTN_edit = wx.Button(self, -1, _("&Edit"), style=wx.BU_EXACTFIT)
        self._BTN_delete = wx.Button(self, wx.ID_DELETE, "", style=wx.BU_EXACTFIT)
        self._BTN_allergy = wx.Button(self, -1, _("Allergy"), style=wx.BU_EXACTFIT)
        self._BTN_info = wx.Button(self, -1, _("Info"), style=wx.BU_EXACTFIT)
        self._BTN_kidneys = wx.Button(self, -1, _("Kidney"), style=wx.BU_EXACTFIT)
        self._BTN_interactions = wx.Button(self, -1, _("&Interactions?"), style=wx.BU_EXACTFIT)
        self._BTN_rx = wx.Button(self, -1, _(u"℞"), style=wx.BU_EXACTFIT)
        self._BTN_adr = wx.Button(self, -1, _("ADR"), style=wx.BU_EXACTFIT)
        self._BTN_print = wx.Button(self, wx.ID_PRINT, "", style=wx.BU_EXACTFIT)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_RADIOBUTTON, self._on_episode_grouping_selected, self._RBTN_episode)
        self.Bind(wx.EVT_RADIOBUTTON, self._on_brand_grouping_selected, self._RBTN_brand)
        self.Bind(wx.EVT_CHECKBOX, self._on_show_inactive_checked, self._CHBOX_show_inactive)
        self.Bind(wx.EVT_CHECKBOX, self._on_show_unapproved_checked, self._CHBOX_show_unapproved)
        self.Bind(wx.EVT_BUTTON, self._on_add_button_pressed, self._BTN_add)
        self.Bind(wx.EVT_BUTTON, self._on_edit_button_pressed, self._BTN_edit)
        self.Bind(wx.EVT_BUTTON, self._on_delete_button_pressed, self._BTN_delete)
        self.Bind(wx.EVT_BUTTON, self._on_allergy_button_pressed, self._BTN_allergy)
        self.Bind(wx.EVT_BUTTON, self._on_info_button_pressed, self._BTN_info)
        self.Bind(wx.EVT_BUTTON, self._on_button_kidneys_pressed, self._BTN_kidneys)
        self.Bind(wx.EVT_BUTTON, self._on_interactions_button_pressed, self._BTN_interactions)
        self.Bind(wx.EVT_BUTTON, self._on_rx_button_pressed, self._BTN_rx)
        self.Bind(wx.EVT_BUTTON, self._on_adr_button_pressed, self._BTN_adr)
        self.Bind(wx.EVT_BUTTON, self._on_print_button_pressed, self._BTN_print)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: wxgCurrentSubstancesPnl.__set_properties
        self.SetScrollRate(10, 10)
        self._RBTN_episode.SetToolTipString(_("Sort entries by \"health issue\" and \"episode\" for which they are taken, then \"substance\", then \"started\"."))
        self._RBTN_episode.SetValue(1)
        self._RBTN_brand.SetToolTipString(_("Sort entries by \"brand\", then \"substance\", then \"started\".\n\nThus each substance will only appear once unless it is really taken in more than one preparation."))
        self._CHBOX_show_inactive.SetToolTipString(_("Whether to show inactive substances, too, or only those which are assumed to currently be active."))
        self._CHBOX_show_inactive.SetValue(1)
        self._CHBOX_show_unapproved.SetToolTipString(_("Whether to show all substances or only those the intake of which is approved of."))
        self._CHBOX_show_unapproved.SetValue(1)
        self._BTN_add.SetToolTipString(_("Add a substance."))
        self._BTN_edit.SetToolTipString(_("Edit the selected substance intake entry."))
        self._BTN_delete.SetToolTipString(_("Remove a substance from the list."))
        self._BTN_allergy.SetToolTipString(_("Discontinue selected entry due to an allergy or intolerance."))
        self._BTN_info.SetToolTipString(_("Show in-depth information on the selected substance if available."))
        self._BTN_kidneys.SetToolTipString(_("Show <www.dosing.de> information on handling of drugs / the selected drug in the presence of renal insufficiency."))
        self._BTN_interactions.SetToolTipString(_("Check for interactions between selected drugs.\n\nIncludes all drugs if none selected."))
        self._BTN_rx.SetToolTipString(_("Write a prescription based on either of\n\n- the selected lines\n- a copy of the most recent prescription"))
        self._BTN_adr.SetToolTipString(_("Report an Adverse Drug Reaction."))
        self._BTN_print.SetToolTipString(_("Print the medication list."))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: wxgCurrentSubstancesPnl.__do_layout
        __szr_main = wx.BoxSizer(wx.VERTICAL)
        __szr_buttons = wx.BoxSizer(wx.HORIZONTAL)
        __szr_grid = wx.BoxSizer(wx.HORIZONTAL)
        __szr_grouping = wx.BoxSizer(wx.HORIZONTAL)
        __lbl_group = wx.StaticText(self, -1, _("Sort by:"))
        __szr_grouping.Add(__lbl_group, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        __szr_grouping.Add(self._RBTN_episode, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        __szr_grouping.Add(self._RBTN_brand, 0, wx.ALIGN_CENTER_VERTICAL, 10)
        __SLINE_grouping = wx.StaticLine(self, -1, style=wx.LI_VERTICAL)
        __szr_grouping.Add(__SLINE_grouping, 0, wx.LEFT|wx.RIGHT|wx.EXPAND, 10)
        __lbl_filter = wx.StaticText(self, -1, _("Include:"))
        __szr_grouping.Add(__lbl_filter, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        __szr_grouping.Add(self._CHBOX_show_inactive, 0, wx.RIGHT|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5)
        __szr_grouping.Add(self._CHBOX_show_unapproved, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5)
        __szr_grouping.Add((20, 20), 1, wx.EXPAND, 0)
        __szr_main.Add(__szr_grouping, 0, wx.EXPAND, 0)
        __szr_grid.Add(self._grid_substances, 1, wx.TOP|wx.EXPAND, 5)
        __szr_main.Add(__szr_grid, 1, wx.EXPAND, 0)
        __szr_buttons.Add((20, 20), 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_buttons.Add(self._BTN_add, 0, wx.RIGHT|wx.EXPAND, 5)
        __szr_buttons.Add(self._BTN_edit, 0, wx.RIGHT|wx.EXPAND, 5)
        __szr_buttons.Add(self._BTN_delete, 0, wx.RIGHT|wx.EXPAND, 5)
        __szr_buttons.Add(self._BTN_allergy, 0, wx.RIGHT|wx.EXPAND, 5)
        __szr_buttons.Add(self._BTN_info, 0, wx.EXPAND, 5)
        __szr_buttons.Add((20, 20), 1, wx.EXPAND, 0)
        __szr_buttons.Add(self._BTN_kidneys, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        __szr_buttons.Add(self._BTN_interactions, 0, wx.ALIGN_CENTER_VERTICAL, 5)
        __szr_buttons.Add((20, 20), 1, wx.EXPAND, 0)
        __szr_buttons.Add(self._BTN_rx, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        __szr_buttons.Add(self._BTN_adr, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        __szr_buttons.Add(self._BTN_print, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_buttons.Add((20, 20), 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_main.Add(__szr_buttons, 0, wx.TOP|wx.EXPAND, 5)
        self.SetSizer(__szr_main)
        __szr_main.Fit(self)
        # end wxGlade

    def _on_add_button_pressed(self, event): # wxGlade: wxgCurrentSubstancesPnl.<event_handler>
        print "Event handler `_on_add_button_pressed' not implemented"
        event.Skip()

    def _on_delete_button_pressed(self, event): # wxGlade: wxgCurrentSubstancesPnl.<event_handler>
        print "Event handler `_on_delete_button_pressed' not implemented"
        event.Skip()

    def _on_print_button_pressed(self, event): # wxGlade: wxgCurrentSubstancesPnl.<event_handler>
        print "Event handler `_on_print_button_pressed' not implemented"
        event.Skip()

    def _on_episode_grouping_selected(self, event): # wxGlade: wxgCurrentSubstancesPnl.<event_handler>
        print "Event handler `_on_episode_grouping_selected' not implemented"
        event.Skip()

    def _on_brand_grouping_selected(self, event): # wxGlade: wxgCurrentSubstancesPnl.<event_handler>
        print "Event handler `_on_brand_grouping_selected' not implemented"
        event.Skip()

    def _on_show_unapproved_checked(self, event): # wxGlade: wxgCurrentSubstancesPnl.<event_handler>
        print "Event handler `_on_show_unapproved_checked' not implemented"
        event.Skip()

    def _on_show_inactive_checked(self, event): # wxGlade: wxgCurrentSubstancesPnl.<event_handler>
        print "Event handler `_on_show_inactive_checked' not implemented"
        event.Skip()

    def _on_interactions_button_pressed(self, event): # wxGlade: wxgCurrentSubstancesPnl.<event_handler>
        print "Event handler `_on_interactions_button_pressed' not implemented"
        event.Skip()

    def _on_edit_button_pressed(self, event): # wxGlade: wxgCurrentSubstancesPnl.<event_handler>
        print "Event handler `_on_edit_button_pressed' not implemented"
        event.Skip()

    def _on_info_button_pressed(self, event): # wxGlade: wxgCurrentSubstancesPnl.<event_handler>
        print "Event handler `_on_info_button_pressed' not implemented"
        event.Skip()

    def _on_allergy_button_pressed(self, event): # wxGlade: wxgCurrentSubstancesPnl.<event_handler>
        print "Event handler `_on_allergy_button_pressed' not implemented"
        event.Skip()

    def _on_button_kidneys_pressed(self, event): # wxGlade: wxgCurrentSubstancesPnl.<event_handler>
        print "Event handler `_on_button_kidneys_pressed' not implemented"
        event.Skip()

    def _on_adr_button_pressed(self, event): # wxGlade: wxgCurrentSubstancesPnl.<event_handler>
        print "Event handler `_on_adr_button_pressed' not implemented"
        event.Skip()

    def _on_rx_button_pressed(self, event): # wxGlade: wxgCurrentSubstancesPnl.<event_handler>
        print "Event handler `_on_rx_button_pressed' not implemented"
        event.Skip()

# end of class wxgCurrentSubstancesPnl


