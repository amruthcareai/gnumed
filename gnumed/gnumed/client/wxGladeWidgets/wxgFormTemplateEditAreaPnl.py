#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.5 on Mon Aug 20 14:02:38 2007 from /home/ncq/Projekte/gm-cvs/branches/HEAD/gnumed/gnumed/client/wxg/wxgFormTemplateEditAreaPnl.wxg

import wx

class wxgFormTemplateEditAreaPnl(wx.ScrolledWindow):
    def __init__(self, *args, **kwds):

        from Gnumed.wxpython import gmPhraseWheel, gmDocumentWidgets

        # begin wxGlade: wxgFormTemplateEditAreaPnl.__init__
        kwds["style"] = wx.NO_BORDER | wx.TAB_TRAVERSAL
        wx.ScrolledWindow.__init__(self, *args, **kwds)
        self._PRW_name_long = gmPhraseWheel.cPhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._PRW_name_short = gmPhraseWheel.cPhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._TCTRL_external_version = wx.TextCtrl(self, -1, "", style=wx.NO_BORDER)
        self._PRW_template_type = gmPhraseWheel.cPhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._PRW_instance_type = gmDocumentWidgets.cDocumentTypeSelectionPhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._TCTRL_filename = wx.TextCtrl(self, -1, "")
        self._BTN_load = wx.Button(self, -1, _("&Template"), style=wx.BU_EXACTFIT)
        self._BTN_export = wx.Button(self, -1, _("Export"), style=wx.BU_EXACTFIT)
        self._CH_engine = wx.Choice(self, -1, choices=[_("OpenOffice"), _("LaTeX"), _("Image editor"), _("Gnuplot"), _("PDF form editor"), _("AbiWord")])
        self._CHBOX_active = wx.CheckBox(self, -1, _("active"))
        self._TCTRL_date_modified = wx.TextCtrl(self, -1, "", style=wx.NO_BORDER)
        self._TCTRL_modified_by = wx.TextCtrl(self, -1, "", style=wx.NO_BORDER)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self._on_load_button_pressed, self._BTN_load)
        self.Bind(wx.EVT_BUTTON, self._on_export_button_pressed, self._BTN_export)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: wxgFormTemplateEditAreaPnl.__set_properties
        self.SetScrollRate(10, 10)
        self._PRW_name_long.SetToolTipString(_("A long, descriptive name for this form template."))
        self._PRW_name_short.SetToolTipString(_("A short, catchy name for this template."))
        self._TCTRL_external_version.SetToolTipString(_("External version information such as the exact version/release/revision of a paper form onto which to print data with the help of this template."))
        self._PRW_template_type.SetToolTipString(_("The type of this template. The intended use case for this template."))
        self._PRW_instance_type.SetToolTipString(_("The document type under which to store forms generated from this template."))
        self._TCTRL_filename.SetToolTipString(_("Examplary filename. Mainly used for deriving a suitable file extension since that matters to some form engines. Most of the time this should already be set correctly when the template data is imported initially."))
        self._TCTRL_filename.Enable(False)
        self._BTN_load.SetToolTipString(_("Load template data from a file."))
        self._BTN_export.SetToolTipString(_("Export the form template into a file."))
        self._BTN_export.Enable(False)
        self._CH_engine.SetToolTipString(_("The form engine this template must be processed with."))
        self._CH_engine.SetSelection(0)
        self._CHBOX_active.SetToolTipString(_("Mark this checkbox if you want this template to be active in GNUmed."))
        self._CHBOX_active.SetValue(1)
        self._TCTRL_date_modified.Enable(False)
        self._TCTRL_modified_by.Enable(False)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: wxgFormTemplateEditAreaPnl.__do_layout
        __gzsr_main = wx.FlexGridSizer(7, 2, 2, 5)
        __szr_status = wx.BoxSizer(wx.HORIZONTAL)
        __szr_options = wx.BoxSizer(wx.HORIZONTAL)
        __szr_filename = wx.BoxSizer(wx.HORIZONTAL)
        __szr_line2 = wx.BoxSizer(wx.HORIZONTAL)
        __lbl_name_long = wx.StaticText(self, -1, _("Name"))
        __gzsr_main.Add(__lbl_name_long, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __gzsr_main.Add(self._PRW_name_long, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_name_short = wx.StaticText(self, -1, _("Alias"))
        __gzsr_main.Add(__lbl_name_short, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_line2.Add(self._PRW_name_short, 2, wx.RIGHT | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 5)
        __lbl_external_version = wx.StaticText(self, -1, _("Version:"))
        __szr_line2.Add(__lbl_external_version, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 3)
        __szr_line2.Add(self._TCTRL_external_version, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
        __gzsr_main.Add(__szr_line2, 1, wx.EXPAND, 0)
        __lbl_template_type = wx.StaticText(self, -1, _("Template type"))
        __gzsr_main.Add(__lbl_template_type, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __gzsr_main.Add(self._PRW_template_type, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_instance_type = wx.StaticText(self, -1, _("Document type"))
        __gzsr_main.Add(__lbl_instance_type, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __gzsr_main.Add(self._PRW_instance_type, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_filename = wx.StaticText(self, -1, _("Filename"))
        __gzsr_main.Add(__lbl_filename, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_filename.Add(self._TCTRL_filename, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_filename.Add(self._BTN_load, 0, wx.LEFT | wx.RIGHT | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 3)
        __szr_filename.Add(self._BTN_export, 0, wx.LEFT | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 3)
        __gzsr_main.Add(__szr_filename, 1, wx.EXPAND, 0)
        __lbl_options = wx.StaticText(self, -1, _("Options"))
        __gzsr_main.Add(__lbl_options, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_engine = wx.StaticText(self, -1, _("Processed by:"))
        __szr_options.Add(__lbl_engine, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)
        __szr_options.Add(self._CH_engine, 0, wx.RIGHT | wx.TOP | wx.BOTTOM | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 3)
        __szr_options.Add(self._CHBOX_active, 0, wx.LEFT | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 3)
        __gzsr_main.Add(__szr_options, 1, wx.EXPAND, 0)
        __lbl_status = wx.StaticText(self, -1, _("Status"))
        __gzsr_main.Add(__lbl_status, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_modified_when = wx.StaticText(self, -1, _("Last modified:"))
        __szr_status.Add(__lbl_modified_when, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 3)
        __szr_status.Add(self._TCTRL_date_modified, 0, wx.RIGHT | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 5)
        __lbl_modified_by = wx.StaticText(self, -1, _("by:"))
        __szr_status.Add(__lbl_modified_by, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 3)
        __szr_status.Add(self._TCTRL_modified_by, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 5)
        __gzsr_main.Add(__szr_status, 1, wx.EXPAND, 0)
        self.SetSizer(__gzsr_main)
        __gzsr_main.Fit(self)
        __gzsr_main.AddGrowableCol(1)
        # end wxGlade

    def _on_load_button_pressed(self, event): # wxGlade: wxgFormTemplateEditAreaPnl.<event_handler>
        print "Event handler `_on_load_button_pressed' not implemented"
        event.Skip()

    def _on_export_button_pressed(self, event): # wxGlade: wxgFormTemplateEditAreaPnl.<event_handler>
        print "Event handler `_on_export_button_pressed' not implemented"
        event.Skip()

# end of class wxgFormTemplateEditAreaPnl


