#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import wx.grid

# begin wxGlade: extracode
# end wxGlade



class wxgCurrentSubstancesPnl(wx.ScrolledWindow):
    def __init__(self, *args, **kwds):

        from Gnumed.wxpython import gmMedicationWidgets

        # begin wxGlade: wxgCurrentSubstancesPnl.__init__
        kwds["style"] = wx.BORDER_NONE | wx.TAB_TRAVERSAL
        wx.ScrolledWindow.__init__(self, *args, **kwds)
        self._HLINE_lab = wx.StaticLine(self, wx.ID_ANY)
        self._CHCE_grouping = wx.Choice(self, wx.ID_ANY, choices=[_("einlangerstring einlangerstring")])
        self._CHBOX_show_inactive = wx.CheckBox(self, wx.ID_ANY, _("Inactive"))
        self._CHBOX_show_unapproved = wx.CheckBox(self, wx.ID_ANY, _("Unapproved"))
        self._grid_substances = gmMedicationWidgets.cCurrentSubstancesGrid(self, wx.ID_ANY, size=(1, 1))
        self._BTN_add = wx.Button(self, wx.ID_ADD, "", style=wx.BU_EXACTFIT)
        self._BTN_edit = wx.Button(self, wx.ID_ANY, _("&Edit"), style=wx.BU_EXACTFIT)
        self._BTN_delete = wx.Button(self, wx.ID_DELETE, "", style=wx.BU_EXACTFIT)
        self._BTN_allergy = wx.Button(self, wx.ID_ANY, _("Allergy"), style=wx.BU_EXACTFIT)
        self._BTN_info = wx.Button(self, wx.ID_ANY, _("Info"), style=wx.BU_EXACTFIT)
        self._BTN_heart = wx.Button(self, wx.ID_ANY, _(u"\u2665"), style=wx.BU_EXACTFIT)
        self._BTN_kidneys = wx.Button(self, wx.ID_ANY, _("Kidney"), style=wx.BU_EXACTFIT)
        self._LBL_gfr = wx.StaticText(self, wx.ID_ANY, _("GFR: ?"))
        self._BTN_interactions = wx.Button(self, wx.ID_ANY, _("&Interactions?"), style=wx.BU_EXACTFIT)
        self._BTN_rx = wx.Button(self, wx.ID_ANY, _(u"\u211e"), style=wx.BU_EXACTFIT)
        self._BTN_adr = wx.Button(self, wx.ID_ANY, _("ADR"), style=wx.BU_EXACTFIT)
        self._BTN_print = wx.Button(self, wx.ID_PRINT, "", style=wx.BU_EXACTFIT)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_CHOICE, self._on_grouping_selected, self._CHCE_grouping)
        self.Bind(wx.EVT_CHECKBOX, self._on_show_inactive_checked, self._CHBOX_show_inactive)
        self.Bind(wx.EVT_CHECKBOX, self._on_show_unapproved_checked, self._CHBOX_show_unapproved)
        self.Bind(wx.EVT_BUTTON, self._on_add_button_pressed, self._BTN_add)
        self.Bind(wx.EVT_BUTTON, self._on_edit_button_pressed, self._BTN_edit)
        self.Bind(wx.EVT_BUTTON, self._on_delete_button_pressed, self._BTN_delete)
        self.Bind(wx.EVT_BUTTON, self._on_allergy_button_pressed, self._BTN_allergy)
        self.Bind(wx.EVT_BUTTON, self._on_info_button_pressed, self._BTN_info)
        self.Bind(wx.EVT_BUTTON, self._on_button_heart_pressed, self._BTN_heart)
        self.Bind(wx.EVT_BUTTON, self._on_button_kidneys_pressed, self._BTN_kidneys)
        self.Bind(wx.EVT_BUTTON, self._on_interactions_button_pressed, self._BTN_interactions)
        self.Bind(wx.EVT_BUTTON, self._on_rx_button_pressed, self._BTN_rx)
        self.Bind(wx.EVT_BUTTON, self._on_adr_button_pressed, self._BTN_adr)
        self.Bind(wx.EVT_BUTTON, self._on_print_button_pressed, self._BTN_print)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: wxgCurrentSubstancesPnl.__set_properties
        self.SetScrollRate(10, 10)
        self._HLINE_lab.Hide()
        self._CHCE_grouping.SetSelection(0)
        self._CHBOX_show_inactive.SetToolTipString(_("Whether to show inactive substances, too, or only those which are assumed to currently be active."))
        self._CHBOX_show_inactive.SetValue(1)
        self._CHBOX_show_unapproved.SetToolTipString(_("Whether to show all substances or only those the intake of which is approved of."))
        self._CHBOX_show_unapproved.SetValue(1)
        self._BTN_add.SetToolTipString(_("Add a substance."))
        self._BTN_edit.SetToolTipString(_("Edit the selected substance intake entry."))
        self._BTN_delete.SetToolTipString(_("Remove a substance from the list."))
        self._BTN_allergy.SetToolTipString(_("Discontinue selected entry due to an allergy or intolerance."))
        self._BTN_info.SetToolTipString(_("Show in-depth information on the selected substance if available."))
        self._BTN_heart.SetFont(wx.Font(13, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self._BTN_heart.SetToolTipString(_("Information on handling drugs in the presence of long Qt syndrome (%s)."))
        self._BTN_kidneys.SetToolTipString(_("Information on handling of drugs / the selected drug in the presence of renal insufficiency (%s)."))
        self._BTN_interactions.SetToolTipString(_("Check for interactions between selected drugs.\n\nIncludes all drugs if none selected."))
        self._BTN_rx.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
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
        self._GSZR_lab = wx.GridSizer(0, 5, 2, 3)
        self._GSZR_lab.Add((0, 0), 0, 0, 0)
        self._GSZR_lab.Add((0, 0), 0, 0, 0)
        self._GSZR_lab.Add((0, 0), 0, 0, 0)
        __szr_main.Add(self._GSZR_lab, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 3)
        __szr_main.Add(self._HLINE_lab, 0, wx.ALIGN_CENTER_VERTICAL | wx.BOTTOM | wx.EXPAND | wx.TOP, 2)
        __lbl_group = wx.StaticText(self, wx.ID_ANY, _("Sort by:"))
        __szr_grouping.Add(__lbl_group, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        __szr_grouping.Add(self._CHCE_grouping, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
        __SLINE_grouping = wx.StaticLine(self, wx.ID_ANY, style=wx.LI_VERTICAL)
        __szr_grouping.Add(__SLINE_grouping, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        __lbl_filter = wx.StaticText(self, wx.ID_ANY, _("Include:"))
        __szr_grouping.Add(__lbl_filter, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        __szr_grouping.Add(self._CHBOX_show_inactive, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.RIGHT, 5)
        __szr_grouping.Add(self._CHBOX_show_unapproved, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 5)
        __szr_grouping.Add((20, 20), 1, wx.EXPAND, 0)
        __szr_main.Add(__szr_grouping, 0, wx.EXPAND, 0)
        __szr_grid.Add(self._grid_substances, 1, wx.EXPAND | wx.TOP, 5)
        __szr_main.Add(__szr_grid, 1, wx.EXPAND, 0)
        __szr_buttons.Add((20, 20), 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
        __szr_buttons.Add(self._BTN_add, 0, wx.EXPAND | wx.RIGHT, 5)
        __szr_buttons.Add(self._BTN_edit, 0, wx.EXPAND | wx.RIGHT, 5)
        __szr_buttons.Add(self._BTN_delete, 0, wx.EXPAND | wx.RIGHT, 5)
        __szr_buttons.Add(self._BTN_allergy, 0, wx.EXPAND | wx.RIGHT, 5)
        __szr_buttons.Add(self._BTN_info, 0, wx.EXPAND, 5)
        __szr_buttons.Add((20, 20), 1, wx.EXPAND, 0)
        __szr_buttons.Add(self._BTN_heart, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        __szr_buttons.Add(self._BTN_kidneys, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        __szr_buttons.Add(self._LBL_gfr, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        __szr_buttons.Add(self._BTN_interactions, 0, wx.ALIGN_CENTER_VERTICAL, 5)
        __szr_buttons.Add((20, 20), 1, wx.EXPAND, 0)
        __szr_buttons.Add(self._BTN_rx, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        __szr_buttons.Add(self._BTN_adr, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        __szr_buttons.Add(self._BTN_print, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_buttons.Add((20, 20), 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
        __szr_main.Add(__szr_buttons, 0, wx.EXPAND | wx.TOP, 5)
        self.SetSizer(__szr_main)
        __szr_main.Fit(self)
        self.Layout()
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

    def _on_product_grouping_selected(self, event): # wxGlade: wxgCurrentSubstancesPnl.<event_handler>
        print "Event handler `_on_product_grouping_selected' not implemented"
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

    def _on_issue_grouping_selected(self, event):  # wxGlade: wxgCurrentSubstancesPnl.<event_handler>
        print "Event handler `_on_issue_grouping_selected' not implemented"
        event.Skip()

    def _on_button_heart_pressed(self, event):  # wxGlade: wxgCurrentSubstancesPnl.<event_handler>
        print "Event handler `_on_button_heart_pressed' not implemented"
        event.Skip()

    def _on_grouping_selected(self, event):  # wxGlade: wxgCurrentSubstancesPnl.<event_handler>
        print "Event handler '_on_grouping_selected' not implemented!"
        event.Skip()
# end of class wxgCurrentSubstancesPnl


