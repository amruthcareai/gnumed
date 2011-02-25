#!/usr/bin/env python
# -*- coding: utf8 -*-
# generated by wxGlade 0.6.3 from "/home/ncq/Projekte/gm-git/gnumed/gnumed/client/wxg/wxgTagImageEAPnl.wxg"

import wx

# begin wxGlade: extracode
# end wxGlade



class wxgTagImageEAPnl(wx.ScrolledWindow):
    def __init__(self, *args, **kwds):
        # begin wxGlade: wxgTagImageEAPnl.__init__
        kwds["style"] = wx.NO_BORDER|wx.TAB_TRAVERSAL
        wx.ScrolledWindow.__init__(self, *args, **kwds)
        self._TCTRL_description = wx.TextCtrl(self, -1, "", style=wx.NO_BORDER)
        self._TCTRL_filename = wx.TextCtrl(self, -1, "", style=wx.NO_BORDER)
        self._BMP_image = wx.lib.statbmp.GenStaticBitmap(self, -1, wx.NullBitmap, style=wx.SIMPLE_BORDER)
        self._BTN_pick_image = wx.Button(self, -1, _("&Pick"), style=wx.BU_EXACTFIT)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self._on_pick_image_button_pressed, self._BTN_pick_image)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: wxgTagImageEAPnl.__set_properties
        self.SetScrollRate(10, 10)
        self._TCTRL_description.SetToolTipString(_("A name for the tag.\n\nNote that there cannot be two tags with the same name."))
        self._TCTRL_filename.SetToolTipString(_("An example file name for this image. Mainly used for deriving a suitable file extension."))
        self._BMP_image.SetMinSize((100, 100))
        self._BMP_image.SetToolTipString(_("The image to use for the tag.\n\nDo not use a big image because the tag will be downscaled anyway."))
        self._BTN_pick_image.SetToolTipString(_("Pick the file from which to load the tag image."))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: wxgTagImageEAPnl.__do_layout
        _gszr_main = wx.FlexGridSizer(3, 2, 1, 3)
        __szr_image = wx.BoxSizer(wx.HORIZONTAL)
        __lbl_name = wx.StaticText(self, -1, _("Tag name"))
        __lbl_name.SetForegroundColour(wx.Colour(255, 0, 0))
        _gszr_main.Add(__lbl_name, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(self._TCTRL_description, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_fname = wx.StaticText(self, -1, _("File name"))
        _gszr_main.Add(__lbl_fname, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(self._TCTRL_filename, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_image = wx.StaticText(self, -1, _("Image"))
        __lbl_image.SetForegroundColour(wx.Colour(255, 0, 0))
        _gszr_main.Add(__lbl_image, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_image.Add(self._BMP_image, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 3)
        __szr_image.Add(self._BTN_pick_image, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(__szr_image, 1, wx.EXPAND, 0)
        self.SetSizer(_gszr_main)
        _gszr_main.Fit(self)
        _gszr_main.AddGrowableCol(1)
        # end wxGlade

    def _on_pick_image_button_pressed(self, event): # wxGlade: wxgTagImageEAPnl.<event_handler>
        print "Event handler `_on_pick_image_button_pressed' not implemented!"
        event.Skip()

# end of class wxgTagImageEAPnl

