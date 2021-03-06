# -*- coding: UTF-8 -*-
#
# generated by wxGlade
#

import wx

# begin wxGlade: dependencies
import gettext
# end wxGlade

# begin wxGlade: extracode
from Gnumed.wxpython.gmSubstanceMgmtWidgets import cDrugProductPhraseWheel
from Gnumed.wxpython.gmPhraseWheel import cPhraseWheel
from Gnumed.wxpython.gmATCWidgets import cATCPhraseWheel
# end wxGlade


class wxgVaccineEAPnl(wx.ScrolledWindow):
	def __init__(self, *args, **kwds):
		# begin wxGlade: wxgVaccineEAPnl.__init__
		kwds["style"] = kwds.get("style", 0) | wx.BORDER_NONE | wx.TAB_TRAVERSAL
		wx.ScrolledWindow.__init__(self, *args, **kwds)
		self._PRW_drug_product = cDrugProductPhraseWheel(self, wx.ID_ANY, "")
		self._CHBOX_fake = wx.CheckBox(self, wx.ID_ANY, _("Fake"))
		self._PRW_route = cPhraseWheel(self, wx.ID_ANY, "")
		self._CHBOX_live = wx.CheckBox(self, wx.ID_ANY, _("Live"), style=wx.CHK_2STATE)
		self._TCTRL_indications = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_MULTILINE | wx.TE_READONLY)
		self._PRW_atc = cATCPhraseWheel(self, wx.ID_ANY, "")
		self._PRW_age_min = cPhraseWheel(self, wx.ID_ANY, "")
		self._PRW_age_max = cPhraseWheel(self, wx.ID_ANY, "")
		self._TCTRL_comment = wx.TextCtrl(self, wx.ID_ANY, "")

		self.__set_properties()
		self.__do_layout()
		# end wxGlade

	def __set_properties(self):
		# begin wxGlade: wxgVaccineEAPnl.__set_properties
		self.SetScrollRate(10, 10)
		self._CHBOX_fake.SetToolTip(_("Whether this is an actual product or a generic, fake vaccine."))
		self._PRW_route.SetToolTip(_("The route by which this vaccine is to be administered.\n\nTypically one of i.m., s.c., or orally."))
		self._PRW_route.Enable(False)
		self._PRW_route.Hide()
		self._CHBOX_live.SetToolTip(_("Check if this is a live attenuated vaccine."))
		self._TCTRL_indications.Enable(False)
		self._PRW_atc.SetToolTip(_("The ATC for this vaccine."))
		self._PRW_age_min.SetToolTip(_("The minimum age at which this vaccine should be given."))
		self._PRW_age_max.SetToolTip(_("The maximum age at which this vaccine should be given."))
		self._TCTRL_comment.SetToolTip(_("Any comment you may wish to relate to this vaccine."))
		# end wxGlade

	def __do_layout(self):
		# begin wxGlade: wxgVaccineEAPnl.__do_layout
		_gszr_main = wx.FlexGridSizer(6, 2, 1, 3)
		__szr_age_range = wx.BoxSizer(wx.HORIZONTAL)
		__szr_route_details = wx.BoxSizer(wx.HORIZONTAL)
		__szr_product_details = wx.BoxSizer(wx.HORIZONTAL)
		__lbl_name = wx.StaticText(self, wx.ID_ANY, _("Name"))
		__lbl_name.SetForegroundColour(wx.Colour(255, 0, 0))
		_gszr_main.Add(__lbl_name, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		__szr_product_details.Add(self._PRW_drug_product, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.RIGHT, 5)
		__szr_product_details.Add(self._CHBOX_fake, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		_gszr_main.Add(__szr_product_details, 1, wx.EXPAND, 0)
		__lbl_route = wx.StaticText(self, wx.ID_ANY, _("Route"))
		__lbl_route.SetForegroundColour(wx.Colour(255, 0, 0))
		__lbl_route.Enable(False)
		__lbl_route.Hide()
		_gszr_main.Add(__lbl_route, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		__szr_route_details.Add(self._PRW_route, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.RIGHT, 5)
		__szr_route_details.Add(self._CHBOX_live, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
		_gszr_main.Add(__szr_route_details, 1, wx.EXPAND, 0)
		__lbl_indications = wx.StaticText(self, wx.ID_ANY, _("Protects\nfrom"))
		__lbl_indications.SetForegroundColour(wx.Colour(255, 0, 0))
		_gszr_main.Add(__lbl_indications, 0, 0, 0)
		_gszr_main.Add(self._TCTRL_indications, 1, wx.EXPAND, 0)
		__lbl_atc = wx.StaticText(self, wx.ID_ANY, _("ATC"))
		_gszr_main.Add(__lbl_atc, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		_gszr_main.Add(self._PRW_atc, 1, wx.EXPAND, 0)
		__lbl_age_range = wx.StaticText(self, wx.ID_ANY, _("Age range"))
		_gszr_main.Add(__lbl_age_range, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		__szr_age_range.Add(self._PRW_age_min, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
		__lbl_from_to = wx.StaticText(self, wx.ID_ANY, _(u"\u2192"))
		__szr_age_range.Add(__lbl_from_to, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 10)
		__szr_age_range.Add(self._PRW_age_max, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
		_gszr_main.Add(__szr_age_range, 1, wx.EXPAND, 0)
		__lbl_comment = wx.StaticText(self, wx.ID_ANY, _("Comment"))
		_gszr_main.Add(__lbl_comment, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		_gszr_main.Add(self._TCTRL_comment, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
		self.SetSizer(_gszr_main)
		_gszr_main.Fit(self)
		_gszr_main.AddGrowableRow(2)
		_gszr_main.AddGrowableCol(1)
		self.Layout()
		# end wxGlade

# end of class wxgVaccineEAPnl
