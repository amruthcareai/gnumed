#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.7.0
#

import wx
import wx.grid

# begin wxGlade: dependencies
import gettext
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class wxgMeasurementsAsTablePnl(wx.Panel):
	def __init__(self, *args, **kwds):

		from Gnumed.wxpython.gmMeasurementWidgets import cMeasurementsGrid

		# begin wxGlade: wxgMeasurementsAsTablePnl.__init__
		kwds["style"] = wx.BORDER_NONE | wx.TAB_TRAVERSAL
		wx.Panel.__init__(self, *args, **kwds)
		self._GRID_results_all = cMeasurementsGrid(self, wx.ID_ANY, size=(1, 1))
		self._BTN_manage_types = wx.Button(self, wx.ID_ANY, _("Manage types"), style=wx.BU_EXACTFIT)
		self._BTN_add = wx.Button(self, wx.ID_ADD, "", style=wx.BU_EXACTFIT)
		self._BTN_select = wx.Button(self, wx.ID_ANY, _("&Select:"), style=wx.BU_EXACTFIT)
		self._RBTN_my_unsigned = wx.RadioButton(self, wx.ID_ANY, _("your unsigned (&Y)"))
		self._RBTN_all_unsigned = wx.RadioButton(self, wx.ID_ANY, _("all unsigned (&A)"))
		self._BTN_review = wx.Button(self, wx.ID_ANY, _("&Actions ... "), style=wx.BU_EXACTFIT)

		self.__set_properties()
		self.__do_layout()

		self.Bind(wx.EVT_BUTTON, self._on_manage_types_button_pressed, self._BTN_manage_types)
		self.Bind(wx.EVT_BUTTON, self._on_add_button_pressed, self._BTN_add)
		self.Bind(wx.EVT_BUTTON, self._on_select_button_pressed, self._BTN_select)
		self.Bind(wx.EVT_BUTTON, self._on_review_button_pressed, self._BTN_review)
		# end wxGlade

	def __set_properties(self):
		# begin wxGlade: wxgMeasurementsAsTablePnl.__set_properties
		self._BTN_manage_types.SetToolTipString(_("Manage test types."))
		self._BTN_add.SetToolTipString(_("Add measurments."))
		self._BTN_select.SetToolTipString(_("Select results according to your choice on the right.\n\nThis will override any previous selection.\n\nNote that you can also select cells, rows, or columns manually within the table."))
		self._RBTN_my_unsigned.SetToolTipString(_("Apply selection to those unsigned results for which you are to take responsibility."))
		self._RBTN_all_unsigned.SetToolTipString(_("Apply selection to all unsigned results."))
		self._BTN_review.SetToolTipString(_("Invoke actions on the selected measurements."))
		# end wxGlade

	def __do_layout(self):
		# begin wxGlade: wxgMeasurementsAsTablePnl.__do_layout
		__szr_main = wx.BoxSizer(wx.VERTICAL)
		__szr_bottom = wx.BoxSizer(wx.HORIZONTAL)
		__szr_main.Add(self._GRID_results_all, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 5)
		__hline_buttons = wx.StaticLine(self, wx.ID_ANY)
		__szr_main.Add(__hline_buttons, 0, wx.ALL | wx.EXPAND, 5)
		__szr_bottom.Add(self._BTN_manage_types, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		__szr_bottom.Add((20, 20), 2, wx.ALIGN_CENTER_VERTICAL, 0)
		__vline_buttons = wx.StaticLine(self, wx.ID_ANY, style=wx.LI_VERTICAL)
		__szr_bottom.Add(__vline_buttons, 0, wx.EXPAND | wx.RIGHT, 3)
		__lbl_results = wx.StaticText(self, wx.ID_ANY, _("Results:"))
		__szr_bottom.Add(__lbl_results, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 3)
		__szr_bottom.Add(self._BTN_add, 0, wx.ALIGN_CENTER_VERTICAL, 3)
		__szr_bottom.Add((20, 20), 1, wx.ALIGN_CENTER_VERTICAL, 0)
		__szr_bottom.Add(self._BTN_select, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
		__szr_bottom.Add(self._RBTN_my_unsigned, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 3)
		__szr_bottom.Add(self._RBTN_all_unsigned, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 3)
		__szr_bottom.Add(self._BTN_review, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		__szr_bottom.Add((20, 20), 1, wx.ALIGN_CENTER_VERTICAL, 0)
		__szr_main.Add(__szr_bottom, 0, wx.BOTTOM | wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
		self.SetSizer(__szr_main)
		__szr_main.Fit(self)
		self.Layout()
		# end wxGlade

	def _on_manage_types_button_pressed(self, event):  # wxGlade: wxgMeasurementsAsTablePnl.<event_handler>
		print "Event handler '_on_manage_types_button_pressed' not implemented!"
		event.Skip()

	def _on_add_button_pressed(self, event):  # wxGlade: wxgMeasurementsAsTablePnl.<event_handler>
		print "Event handler '_on_add_button_pressed' not implemented!"
		event.Skip()

	def _on_select_button_pressed(self, event):  # wxGlade: wxgMeasurementsAsTablePnl.<event_handler>
		print "Event handler '_on_select_button_pressed' not implemented!"
		event.Skip()

	def _on_review_button_pressed(self, event):  # wxGlade: wxgMeasurementsAsTablePnl.<event_handler>
		print "Event handler '_on_review_button_pressed' not implemented!"
		event.Skip()

# end of class wxgMeasurementsAsTablePnl
