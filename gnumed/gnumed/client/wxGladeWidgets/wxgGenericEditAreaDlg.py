#!/usr/bin/env python
# -*- coding: utf8 -*-
# generated by wxGlade 0.6.3 on Sat Aug  1 12:10:35 2009

import wx

# begin wxGlade: extracode
# end wxGlade



class wxgGenericEditAreaDlg(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: wxgGenericEditAreaDlg.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX|wx.THICK_FRAME
        wx.Dialog.__init__(self, *args, **kwds)
        self._PNL_ea = wx.Panel(self, -1, style=wx.NO_BORDER|wx.TAB_TRAVERSAL)
        self._BTN_save = wx.Button(self, wx.ID_SAVE, "")
        self._BTN_clear = wx.Button(self, wx.ID_CLEAR, "")
        self._BTN_cancel = wx.Button(self, wx.ID_CANCEL, "")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self._on_save_button_pressed, self._BTN_save)
        self.Bind(wx.EVT_BUTTON, self._on_clear_button_pressed, self._BTN_clear)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: wxgGenericEditAreaDlg.__set_properties
        self.SetTitle(_("GNUmed  generic EditArea dialog"))
        self.SetSize((450, 280))
        self.SetSetMinSize((450,280))
        self._BTN_save.SetToolTipString(_("Save the entered data into the database."))
        self._BTN_clear.SetToolTipString(_("Clear all fields or reset to database values."))
        self._BTN_cancel.SetToolTipString(_("Cancel editing the data and discard changes."))
        self._BTN_cancel.SetDefault()
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: wxgGenericEditAreaDlg.__do_layout
        _szr_main = wx.BoxSizer(wx.VERTICAL)
        __szr_buttons = wx.BoxSizer(wx.HORIZONTAL)
        __szr_pnl_ea = wx.BoxSizer(wx.HORIZONTAL)
        __szr_pnl_ea.Add(self._PNL_ea, 1, wx.EXPAND, 0)
        _szr_main.Add(__szr_pnl_ea, 1, wx.ALL|wx.EXPAND, 5)
        __szr_buttons.Add(self._BTN_save, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_buttons.Add(self._BTN_clear, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_buttons.Add((20, 20), 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_buttons.Add(self._BTN_cancel, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        _szr_main.Add(__szr_buttons, 0, wx.ALL|wx.EXPAND, 5)
        self.SetSizer(_szr_main)
        self.Layout()
        self.Centre()
        # end wxGlade

    def _on_save_button_pressed(self, event): # wxGlade: wxgGenericEditAreaDlg.<event_handler>
        print "Event handler `_on_save_button_pressed' not implemented!"
        event.Skip()

    def _on_clear_button_pressed(self, event): # wxGlade: wxgGenericEditAreaDlg.<event_handler>
        print "Event handler `_on_clear_button_pressed' not implemented!"
        event.Skip()

# end of class wxgGenericEditAreaDlg


if __name__ == "__main__":
    import gettext
    gettext.install("app") # replace with the appropriate catalog name

    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    dialog_1 = wxgGenericEditAreaDlg(None, -1, "")
    app.SetTopWindow(dialog_1)
    dialog_1.Show()
    app.MainLoop()
