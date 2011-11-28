#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 from "/home/ncq/Projekte/gm-git/gnumed/gnumed/client/wxg/wxgActiveEncounterPnl.wxg"

import wx

# begin wxGlade: extracode
# end wxGlade



class wxgActiveEncounterPnl(wx.Panel):
    def __init__(self, *args, **kwds):
        # begin wxGlade: wxgActiveEncounterPnl.__init__
        kwds["style"] = wx.NO_BORDER|wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self._TCTRL_encounter = wx.TextCtrl(self, -1, "", style=wx.TE_READONLY|wx.NO_BORDER)
        self._BTN_new = wx.Button(self, -1, _("&N"), style=wx.BU_EXACTFIT)
        self._BTN_list = wx.Button(self, -1, _("&L"), style=wx.BU_EXACTFIT)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self._on_new_button_pressed, self._BTN_new)
        self.Bind(wx.EVT_BUTTON, self._on_list_button_pressed, self._BTN_list)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: wxgActiveEncounterPnl.__set_properties
        self._TCTRL_encounter.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_BACKGROUND))
        self._TCTRL_encounter.SetToolTipString(_("The encounter."))
        self._BTN_new.SetToolTipString(_("Start a new encounter for the active patient."))
        self._BTN_list.SetToolTipString(_("List all encounters."))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: wxgActiveEncounterPnl.__do_layout
        __szr_main = wx.BoxSizer(wx.HORIZONTAL)
        __szr_main.Add(self._TCTRL_encounter, 2, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 3)
        __szr_main.Add(self._BTN_new, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 3)
        __szr_main.Add(self._BTN_list, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.SetSizer(__szr_main)
        __szr_main.Fit(self)
        # end wxGlade

    def _on_new_button_pressed(self, event): # wxGlade: wxgActiveEncounterPnl.<event_handler>
        print "Event handler `_on_new_button_pressed' not implemented!"
        event.Skip()

    def _on_list_button_pressed(self, event): # wxGlade: wxgActiveEncounterPnl.<event_handler>
        print "Event handler `_on_list_button_pressed' not implemented!"
        event.Skip()

# end of class wxgActiveEncounterPnl


