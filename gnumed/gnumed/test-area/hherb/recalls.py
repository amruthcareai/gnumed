#!/usr/bin/env python
# generated by wxGlade 0.2.1cvs on Sat Jan 11 15:27:15 2003

from wxPython.wx import *
from wxPython.grid import *

class RecallPanel(wxPanel):
    def __init__(self, *args, **kwds):
        # begin wxGlade: RecallPanel.__init__
        kwds["style"] = wxTAB_TRAVERSAL
        wxPanel.__init__(self, *args, **kwds)
        self.lbl_name = wxStaticText(self, -1, _("Name"))
        self.lbl_recall_reason = wxStaticText(self, -1, _("reason for recall"))
        self.lbl_due = wxStaticText(self, -1, _("due"))
        self.lbl_importance = wxStaticText(self, -1, _("importance"))
        self.lbl_requested_by = wxStaticText(self, -1, _("req. by"))
        self.lbl_action = wxStaticText(self, -1, _("action"))
        self.tc_name = wxTextCtrl(self, -1, "")
        self.tc_reason = wxTextCtrl(self, -1, "")
        self.tc_due = wxTextCtrl(self, -1, "")
        self.ch_flag = wxChoice(self, -1, choices=[_("routine")])
        self.cmb_reqby = wxComboBox(self, -1, choices=[_("doctor")], style=wxCB_DROPDOWN)
        self.cmb_action = wxComboBox(self, -1, choices=[_("ring")], style=wxCB_DROPDOWN)
        self.btn_addrecall = wxButton(self, -1, _("&Add"))
        self.grid_recalls = wxGrid(self, -1)
        self.cb_events = wxCheckBox(self, -1, _("events"))
        self.cb_finalized = wxCheckBox(self, -1, _("finalized"))
        self.cmb_selectdisplay = wxComboBox(self, -1, choices=[_("all")], style=wxCB_DROPDOWN)
        self.btn_update = wxButton(self, -1, _("&Update"))

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: RecallPanel.__set_properties
        self.tc_name.SetSize((120, 25))
        self.tc_name.SetToolTipString(_("Enter any numbers of first name and surname separated by a space and hit return, or just enter any number of letters from the surname and hit return"))
        self.ch_flag.SetSelection(0)
        self.cmb_reqby.SetSelection(0)
        self.cmb_action.SetSelection(0)
        self.grid_recalls.CreateGrid(20, 10)
        self.grid_recalls.SetColLabelValue(0, _("Name"))
        self.grid_recalls.SetColLabelValue(1, _("reason"))
        self.grid_recalls.SetColLabelValue(2, _("due"))
        self.grid_recalls.SetColLabelValue(3, _("flag"))
        self.grid_recalls.SetColLabelValue(4, _("req. by"))
        self.grid_recalls.SetColLabelValue(5, _("action"))
        self.grid_recalls.SetColLabelValue(6, _("managed"))
        self.grid_recalls.SetColLabelValue(7, _("by"))
        self.grid_recalls.SetColLabelValue(8, _("how"))
        self.grid_recalls.SetColLabelValue(9, _("completed"))
        self.cb_events.SetValue(1)
        self.cmb_selectdisplay.SetSelection(0)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: RecallPanel.__do_layout
        szr_top = wxBoxSizer(wxVERTICAL)
        szr_optionsrow = wxBoxSizer(wxHORIZONTAL)
        fgszr_editrow = wxFlexGridSizer(2, 7, 0, 8)
        fgszr_editrow.Add(self.lbl_name, 0, 0, 0)
        fgszr_editrow.Add(self.lbl_recall_reason, 0, wxEXPAND, 0)
        fgszr_editrow.Add(self.lbl_due, 0, 0, 0)
        fgszr_editrow.Add(self.lbl_importance, 0, 0, 0)
        fgszr_editrow.Add(self.lbl_requested_by, 0, 0, 0)
        fgszr_editrow.Add(self.lbl_action, 0, 0, 0)
        fgszr_editrow.Add(20, 20, 0, 0, 0)
        fgszr_editrow.Add(self.tc_name, 0, wxEXPAND, 0)
        fgszr_editrow.Add(self.tc_reason, 0, wxEXPAND, 0)
        fgszr_editrow.Add(self.tc_due, 0, wxEXPAND, 0)
        fgszr_editrow.Add(self.ch_flag, 0, 0, 0)
        fgszr_editrow.Add(self.cmb_reqby, 0, 0, 0)
        fgszr_editrow.Add(self.cmb_action, 0, 0, 0)
        fgszr_editrow.Add(self.btn_addrecall, 0, 0, 0)
        fgszr_editrow.AddGrowableCol(1)
        szr_top.Add(fgszr_editrow, 0, wxALL|wxEXPAND, 10)
        szr_top.Add(self.grid_recalls, 1, wxEXPAND, 0)
        szr_optionsrow.Add(self.cb_events, 0, 0, 0)
        szr_optionsrow.Add(self.cb_finalized, 0, 0, 0)
        szr_optionsrow.Add(20, 20, 1, wxLEFT, 0)
        szr_optionsrow.Add(self.cmb_selectdisplay, 0, 0, 0)
        szr_optionsrow.Add(self.btn_update, 0, 0, 0)
        szr_top.Add(szr_optionsrow, 0, wxEXPAND, 0)
        self.SetAutoLayout(1)
        self.SetSizer(szr_top)
        szr_top.Fit(self)
        szr_top.SetSizeHints(self)
        self.Layout()
        # end wxGlade

# end of class RecallPanel


class MainFrame(wxFrame):
    def __init__(self, *args, **kwds):

        # begin wxGlade: MainFrame.__init__
        kwds["style"] = wxDEFAULT_FRAME_STYLE
        wxFrame.__init__(self, *args, **kwds)
        self.notebook_recalls = wxNotebook(self, -1, style=0)
        self.nbp_due = wxPanel(self.notebook_recalls, -1)
        self.frmRecallApp_statusbar = self.CreateStatusBar(2)
        
        # Menu Bar
        self.frmRecallApp_menubar = wxMenuBar()
        self.SetMenuBar(self.frmRecallApp_menubar)
        self.menuFile = wxMenu()
        self.menuFile.Append(wxNewId(), _("&Close"), "")
        self.frmRecallApp_menubar.Append(self.menuFile, _("&File"))
        # Menu Bar end
        self.nbp_overview = RecallPanel(self.notebook_recalls, -1)
        self.lc_due = wxListCtrl(self.nbp_due, -1)
        self.nbp_overdue = wxPanel(self.notebook_recalls, -1)
        self.nbp_completed = wxPanel(self.notebook_recalls, -1)
        self.nbp_log = wxPanel(self.notebook_recalls, -1)
        self.nbp_templates = wxPanel(self.notebook_recalls, -1)
        self.nbp_macros = wxPanel(self.notebook_recalls, -1)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MainFrame.__set_properties
        self.SetTitle(_("GnuMed: recall system"))
        self.frmRecallApp_statusbar.SetStatusWidths([-1, 60])
        # statusbar fields
        frmRecallApp_statusbar_fields = [_("Not logged in"), _("00:00")]
        for i in range(len(frmRecallApp_statusbar_fields)):
            self.frmRecallApp_statusbar.SetStatusText(frmRecallApp_statusbar_fields[i], i)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MainFrame.__do_layout
        szr_main = wxBoxSizer(wxVERTICAL)
        sizer_main = wxBoxSizer(wxHORIZONTAL)
        sizer_main.Add(self.lc_due, 1, wxEXPAND, 0)
        self.nbp_due.SetAutoLayout(1)
        self.nbp_due.SetSizer(sizer_main)
        sizer_main.Fit(self.nbp_due)
        sizer_main.SetSizeHints(self.nbp_due)
        self.notebook_recalls.AddPage(self.nbp_overview, _("Overview"))
        self.notebook_recalls.AddPage(self.nbp_due, _("Due"))
        self.notebook_recalls.AddPage(self.nbp_overdue, _("Overdue"))
        self.notebook_recalls.AddPage(self.nbp_completed, _("Completed"))
        self.notebook_recalls.AddPage(self.nbp_log, _("Log"))
        self.notebook_recalls.AddPage(self.nbp_templates, _("Templates"))
        self.notebook_recalls.AddPage(self.nbp_macros, _("Macros"))
        szr_main.Add(wxNotebookSizer(self.notebook_recalls), 1, wxEXPAND, 0)
        self.SetAutoLayout(1)
        self.SetSizer(szr_main)
        szr_main.Fit(self)
        szr_main.SetSizeHints(self)
        self.Layout()
        # end wxGlade


# end of class MainFrame


class RecallApp(wxApp):
    def OnInit(self):
        wxInitAllImageHandlers()
        frame_1 = MainFrame(None, -1, "")
        self.SetTopWindow(frame_1)
        frame_1.Show(1)
        return 1

# end of class RecallApp

if __name__ == "__main__":
    import gettext
    gettext.install("recalls") # replace with the appropriate catalog name

    recalls = RecallApp()
    recalls.MainLoop()
