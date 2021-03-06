"""GNUmed GUI helper classes and functions.

This module provides some convenient wxPython GUI
helper thingies that are widely used throughout
GNUmed.
"""
# ========================================================================
__author__  = "K. Hilbert <Karsten.Hilbert@gmx.net>"
__license__ = "GPL v2 or later (details at http://www.gnu.org)"

import os
import logging
import sys
import io
import time
import datetime as pyDT


import wx


if __name__ == '__main__':
	sys.path.insert(0, '../../')
from Gnumed.pycommon import gmMatchProvider
from Gnumed.pycommon import gmExceptions
from Gnumed.pycommon import gmLog2
from Gnumed.pycommon import gmTools
from Gnumed.pycommon import gmDispatcher
from Gnumed.wxpython import gmPhraseWheel


_log = logging.getLogger('gm.main')
# ========================================================================
class cThreeValuedLogicPhraseWheel(gmPhraseWheel.cPhraseWheel):

	def __init__(self, *args, **kwargs):

		gmPhraseWheel.cPhraseWheel.__init__(self, *args, **kwargs)

		items = [
			{'list_label': _('Yes: + / ! / 1'), 'field_label': _('yes'), 'data': True, 'weight': 0},
			{'list_label': _('No: - / 0'), 'field_label': _('no'), 'data': False, 'weight': 1},
			{'list_label': _('Unknown: ?'), 'field_label': _('unknown'), 'data': None, 'weight': 2},
		]
		mp = gmMatchProvider.cMatchProvider_FixedList(items)
		mp.setThresholds(1, 1, 2)
		mp.word_separators = '[ :/]+'
		mp.word_separators = None
		mp.ignored_chars = r"[.'\\(){}\[\]<>~#*$%^_=&@\t23456]+" + r'"'

		self.matcher = mp
# ========================================================================
from Gnumed.wxGladeWidgets import wxg2ButtonQuestionDlg

class c2ButtonQuestionDlg(wxg2ButtonQuestionDlg.wxg2ButtonQuestionDlg):

	def __init__(self, *args, **kwargs):

		caption = kwargs['caption']
		question = kwargs['question']
		button_defs = kwargs['button_defs'][:2]
		del kwargs['caption']
		del kwargs['question']
		del kwargs['button_defs']

		try:
			show_checkbox = kwargs['show_checkbox']
			del kwargs['show_checkbox']
		except KeyError:
			show_checkbox = False

		try:
			checkbox_msg = kwargs['checkbox_msg']
			del kwargs['checkbox_msg']
		except KeyError:
			checkbox_msg = None

		try:
			checkbox_tooltip = kwargs['checkbox_tooltip']
			del kwargs['checkbox_tooltip']
		except KeyError:
			checkbox_tooltip = None

		wxg2ButtonQuestionDlg.wxg2ButtonQuestionDlg.__init__(self, *args, **kwargs)

		self.SetTitle(title = decorate_window_title(caption))
		self._LBL_question.SetLabel(label = question)

		if not show_checkbox:
			self._CHBOX_dont_ask_again.Hide()
		else:
			if checkbox_msg is not None:
				self._CHBOX_dont_ask_again.SetLabel(checkbox_msg)
			if checkbox_tooltip is not None:
				self._CHBOX_dont_ask_again.SetToolTip(checkbox_tooltip)

		buttons = [self._BTN_1, self._BTN_2]
		for idx in range(len(button_defs)):
			buttons[idx].SetLabel(label = button_defs[idx]['label'])
			buttons[idx].SetToolTip(button_defs[idx]['tooltip'])
			try:
				if button_defs[idx]['default'] is True:
					buttons[idx].SetDefault()
					buttons[idx].SetFocus()
			except KeyError:
				pass

		self.Fit()
	#--------------------------------------------------------
	def checkbox_is_checked(self):
		return self._CHBOX_dont_ask_again.IsChecked()
	#--------------------------------------------------------
	# event handlers
	#--------------------------------------------------------
	def _on_BTN_1_pressed(self, evt):
		if self.IsModal():
			self.EndModal(wx.ID_YES)
		else:
			self.Close()
	#--------------------------------------------------------
	def _on_BTN_2_pressed(self, evt):
		if self.IsModal():
			self.EndModal(wx.ID_NO)
		else:
			self.Close()

# ========================================================================
from Gnumed.wxGladeWidgets import wxg3ButtonQuestionDlg

class c3ButtonQuestionDlg(wxg3ButtonQuestionDlg.wxg3ButtonQuestionDlg):

	def __init__(self, *args, **kwargs):
		"""Initialize.

	button_defs = [
		# tooltip and default are optional
		{'label': _(''), 'tooltip': _(''), 'default': True/False},
		{'label': _(''), 'tooltip': _(''), 'default': True/False},
		{'label': _(''), 'tooltip': _(''), 'default': True/False}
	]
		"""
		caption = kwargs['caption']
		question = kwargs['question']
		button_defs = kwargs['button_defs'][:3]
		del kwargs['caption']
		del kwargs['question']
		del kwargs['button_defs']

		try:
			show_checkbox = kwargs['show_checkbox']
			del kwargs['show_checkbox']
		except KeyError:
			show_checkbox = False

		try:
			checkbox_msg = kwargs['checkbox_msg']
			del kwargs['checkbox_msg']
		except KeyError:
			checkbox_msg = None

		try:
			checkbox_tooltip = kwargs['checkbox_tooltip']
			del kwargs['checkbox_tooltip']
		except KeyError:
			checkbox_tooltip = None

		wxg3ButtonQuestionDlg.wxg3ButtonQuestionDlg.__init__(self, *args, **kwargs)

		self.SetTitle(title = decorate_window_title(caption))
		self._LBL_question.SetLabel(label = question)

		if not show_checkbox:
			self._CHBOX_dont_ask_again.Hide()
		else:
			if checkbox_msg is not None:
				self._CHBOX_dont_ask_again.SetLabel(checkbox_msg)
			if checkbox_tooltip is not None:
				self._CHBOX_dont_ask_again.SetToolTip(checkbox_tooltip)

		buttons = [self._BTN_1, self._BTN_2, self._BTN_3]
		for idx in range(len(button_defs)):
			buttons[idx].SetLabel(label = button_defs[idx]['label'])
			try:
				buttons[idx].SetToolTip(button_defs[idx]['tooltip'])
			except KeyError:
				pass
			try:
				if button_defs[idx]['default'] is True:
					buttons[idx].SetDefault()
					buttons[idx].SetFocus()
			except KeyError:
				pass

		self.Fit()
	#--------------------------------------------------------
	def checkbox_is_checked(self):
		return self._CHBOX_dont_ask_again.IsChecked()

	#--------------------------------------------------------
	# event handlers
	#--------------------------------------------------------
	def _on_BTN_1_pressed(self, evt):
		if self.IsModal():
			self.EndModal(wx.ID_YES)
		else:
			self.Close()

	#--------------------------------------------------------
	def _on_BTN_2_pressed(self, evt):
		if self.IsModal():
			self.EndModal(wx.ID_NO)
		else:
			self.Close()

# ========================================================================
from Gnumed.wxGladeWidgets import wxgMultilineTextEntryDlg

class cMultilineTextEntryDlg(wxgMultilineTextEntryDlg.wxgMultilineTextEntryDlg):
	"""Editor for a bit of text."""

	def __init__(self, *args, **kwargs):

		try:
			title = kwargs['title']
			del kwargs['title']
		except KeyError:
			title = None

		try:
			msg = kwargs['msg']
			del kwargs['msg']
		except KeyError:
			msg = None

		try:
			data = kwargs['data']
			del kwargs['data']
		except KeyError:
			data = None

		try:
			self.original_text = kwargs['text']
			del kwargs['text']
		except KeyError:
			self.original_text = None

		wxgMultilineTextEntryDlg.wxgMultilineTextEntryDlg.__init__(self, *args, **kwargs)

		if title is not None:
			self.SetTitle(decorate_window_title(title))

		if self.original_text is not None:
			self._TCTRL_text.SetValue(self.original_text)
			self._BTN_restore.Enable(True)

		if msg is None:
			self._LBL_msg.Hide()
		else:
			self._LBL_msg.SetLabel(msg)
			self.Layout()
			self.Refresh()

		if data is None:
			self._TCTRL_data.Hide()
		else:
			self._TCTRL_data.SetValue(data)
			self.Layout()
			self.Refresh()

		self._TCTRL_text.SetFocus()
	#--------------------------------------------------------
	# properties
	#--------------------------------------------------------
	def _get_value(self):
		return self._TCTRL_text.GetValue()

	value = property(_get_value, lambda x:x)
	#--------------------------------------------------------
	def _get_is_user_formatted(self):
		return self._CHBOX_is_already_formatted.IsChecked()

	is_user_formatted = property(_get_is_user_formatted, lambda x:x)
	#--------------------------------------------------------
	def _set_enable_user_formatting(self, value):
		self._CHBOX_is_already_formatted.Enable(value)

	enable_user_formatting = property(lambda x:x, _set_enable_user_formatting)
	#--------------------------------------------------------
	# event handlers
	#--------------------------------------------------------
	def _on_save_button_pressed(self, evt):

		if self.IsModal():
			self.EndModal(wx.ID_SAVE)
		else:
			self.Close()
	#--------------------------------------------------------
	def _on_clear_button_pressed(self, evt):
		self._TCTRL_text.SetValue('')
	#--------------------------------------------------------
	def _on_restore_button_pressed(self, evt):
		if self.original_text is not None:
			self._TCTRL_text.SetValue(self.original_text)

# ========================================================================
def clipboard2text():

	if wx.TheClipboard.IsOpened():
		return False

	if not wx.TheClipboard.Open():
		return False

	data_obj = wx.TextDataObject()
	got_it = wx.TheClipboard.GetData(data_obj)
	if got_it:
		txt = data_obj.Text
		wx.TheClipboard.Close()
		return txt

	wx.TheClipboard.Close()
	return None

#-------------------------------------------------------------------------
def clipboard2file(check_for_filename=False):

	if wx.TheClipboard.IsOpened():
		return False

	if not wx.TheClipboard.Open():
		return False

	data_obj = wx.TextDataObject()
	got_it = wx.TheClipboard.GetData(data_obj)
	if got_it:
		clipboard_text_content = data_obj.Text
		wx.TheClipboard.Close()
		if check_for_filename:
			try:
				io.open(clipboard_text_content).close()
				return clipboard_text_content
			except IOError:
				_log.exception('clipboard does not seem to hold filename: %s', clipboard_text_content)
		fname = gmTools.get_unique_filename(prefix = 'gm-clipboard-', suffix = '.txt')
		target_file = io.open(fname, mode = 'wt', encoding = 'utf8')
		target_file.write(clipboard_text_content)
		target_file.close()
		return fname

	data_obj = wx.BitmapDataObject()
	got_it = wx.TheClipboard.GetData(data_obj)
	if got_it:
		fname = gmTools.get_unique_filename(prefix = 'gm-clipboard-', suffix = '.png')
		bmp = data_obj.Bitmap.SaveFile(fname, wx.BITMAP_TYPE_PNG)
		wx.TheClipboard.Close()
		return fname

	wx.TheClipboard.Close()
	return None

#-------------------------------------------------------------------------
def text2clipboard(text=None, announce_result=False):
	if wx.TheClipboard.IsOpened():
		return False
	if not wx.TheClipboard.Open():
		return False
	data_obj = wx.TextDataObject()
	data_obj.SetText(text)
	wx.TheClipboard.SetData(data_obj)
	wx.TheClipboard.Close()
	if announce_result:
		gmDispatcher.send(signal = 'statustext', msg = _('The text has been copied into the clipboard.'), beep = False)
	return True

#-------------------------------------------------------------------------
def file2clipboard(filename=None, announce_result=False):
	f = io.open(filename, mode = 'rt', encoding = 'utf8')
	result = text2clipboard(text = f.read(), announce_result = False)
	f.close()
	if announce_result:
		gm_show_info (
			title = _('file2clipboard'),
			info = _('The file [%s] has been copied into the clipboard.') % filename
		)
	return result

# ========================================================================
class cFileDropTarget(wx.FileDropTarget):
	"""Generic file drop target class.

	Protocol:
		Widgets being declared file drop targets
		must provide the method:

			def _drop_target_consume_filenames(self, filenames)

		or declare a callback during __init__() of this class.
	"""
	#-----------------------------------------------
	def __init__(self, target=None, on_drop_callback=None):
		if target is not None:
			on_drop_callback = getattr(target, '_drop_target_consume_filenames')
		if not callable(on_drop_callback):
			_log.error('[%s] not callable, cannot set as drop target callback', on_drop_callback)
			raise AttributeError('[%s] not callable, cannot set as drop target callback', on_drop_callback)

		self._on_drop_callback = on_drop_callback
		wx.FileDropTarget.__init__(self)
		_log.debug('setting up [%s] as file drop target', self._on_drop_callback)

	#-----------------------------------------------
	def OnDropFiles(self, x, y, filenames):
		self._on_drop_callback(filenames)

# ========================================================================
def file2scaled_image(filename=None, height=100):
	img_data = None
	bitmap = None
	rescaled_height = height
	try:
		img_data = wx.Image(filename, wx.BITMAP_TYPE_ANY)
		current_width = img_data.GetWidth()
		current_height = img_data.GetHeight()
#		if current_width == 0:
#			current_width = 1
#		if current_height == 0:
#			current_height = 1
		rescaled_width = (float(current_width) / current_height) * rescaled_height
		img_data.Rescale(rescaled_width, rescaled_height, quality = wx.IMAGE_QUALITY_HIGH)		# w, h
		bitmap = wx.Bitmap(img_data)
		del img_data
	except Exception:
		_log.exception('cannot load image from [%s]', filename)
		del img_data
		del bitmap
		return None
	return bitmap

# ========================================================================
def save_screenshot_to_file(filename=None, widget=None, settle_time=None):
	"""Take screenshot of widget.

	<settle_time> in milliseconds
	"""
	assert (isinstance(widget, wx.Window)), '<widget> must be (sub)class of wx.Window'

	if filename is None:
		filename = gmTools.get_unique_filename (
			prefix = 'gm-screenshot-%s-' % pyDT.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'),
			suffix = '.png'
			# for testing:
			#,tmp_dir = os.path.join(gmTools.gmPaths().home_dir, 'gnumed')
		)
	else:
		filename = gmTools.fname_sanitize(filename)

	_log.debug('filename: %s', filename)
	_log.debug('widget: %s', widget)
	_log.debug('display size: %s', wx.DisplaySize())

	# let it settle a bit for, say, tooltips
	if settle_time is not None:
		for wait_slice in range(int(settle_time // 100)):
			wx.SafeYield()
			time.sleep(0.1)

	widget_rect_on_screen = widget.GetScreenRect()
	client_area_origin_on_screen = widget.ClientToScreen((0, 0))
	widget_rect_local = widget.GetRect()
	widget_rect_client_area = widget.GetClientRect()
	client_area_origin_local = widget.GetClientAreaOrigin()

	_log.debug('widget.GetScreenRect(): %s', widget_rect_on_screen)
	_log.debug('widget.ClientToScreen(0, 0): %s', client_area_origin_on_screen)
	_log.debug('widget.GetRect(): %s', widget_rect_local)
	_log.debug('widget.GetClientRect(): %s', widget_rect_client_area)
	_log.debug('widget.GetClientAreaOrigin(): %s', client_area_origin_local)

	width2snap = widget_rect_local.width
	height2snap = widget_rect_local.height
	border_x = client_area_origin_on_screen.x - widget_rect_local.x
	x2snap_from = 0 - border_x
	title_and_menu_height = client_area_origin_on_screen.y - widget_rect_on_screen.y
	y2snap_from = 0 - title_and_menu_height

	# those are the correct dimensions but we don't get to
	# *see* the window decorations on a WindowDC or ClientDC :-(
	# (and a screendc doesn't work either)
	_log.debug('left (x) border: %s', border_x)
	_log.debug('top (y) border: %s', title_and_menu_height)
	_log.debug('x2snap_from: %s', x2snap_from)
	_log.debug('y2snap_from: %s', y2snap_from)
	_log.debug('width2snap: %s', width2snap)
	_log.debug('height2snap: %s', height2snap)

	# WindowDC includes decorations, supposedly, but Windows only
	window_dc = wx.WindowDC(widget)
	wxbmp = __snapshot_to_bitmap (
		source_dc = window_dc,
		x2snap_from = x2snap_from,
		y2snap_from = y2snap_from,
		width2snap = width2snap,
		height2snap = height2snap
	)
	window_dc.Destroy()
	del window_dc
	wxbmp.SaveFile(filename, wx.BITMAP_TYPE_PNG)
	del wxbmp

	x2snap_on_screen = widget_rect_on_screen.x
	y2snap_on_screen = widget_rect_on_screen.y			# adjust for menu/title ?
	sane_x2snap_on_screen = max(0, x2snap_on_screen)
	sane_y2snap_on_screen = max(0, y2snap_on_screen)

	_log.debug('x2snap_on_screen: %s', x2snap_on_screen)
	_log.debug('y2snap_on_screen: %s', y2snap_on_screen)
	_log.debug('sane x2snap_on_screen: %s', sane_x2snap_on_screen)
	_log.debug('sane x2snap_on_screen: %s', sane_y2snap_on_screen)

	screen_dc = wx.ScreenDC()
	# not implemented:
	#wxbmp = screen_dc.GetAsBitmap()		# can use subrect=...
	wxbmp = __snapshot_to_bitmap (
		source_dc = screen_dc,
		x2snap_from = sane_x2snap_on_screen,
		y2snap_from = sane_y2snap_on_screen,
		width2snap = width2snap,
		height2snap = height2snap
	)
	screen_dc.Destroy()
	del screen_dc
	wxbmp.SaveFile(filename + '.screendc.png', wx.BITMAP_TYPE_PNG)
	del wxbmp

	# ClientDC does not include decorations, only client area
	#client_dc = wx.ClientDC(widget)
	#wxbmp = __snapshot_to_bitmap (
	#	source_dc = client_dc,
	#	x2snap_from = x2snap_from,
	#	y2snap_from = y2snap_from,
	#	width2snap = width2snap,
	#	height2snap = height2snap
	#)
	#client_dc.Destroy()
	#del client_dc
	#wxbmp.SaveFile(filename + '.clientdc.png', wx.BITMAP_TYPE_PNG)
	#del wxbmp

	# adjust for window decoration on Linux
	#if sys.platform == 'linux':
	# If the widget has a menu bar, remove that from the title bar height.
	#if hasattr(widget, 'GetMenuBar'):
	#	if widget.GetMenuBar():
	#		title_bar_height /= 2
	#		print('title bar height:', title_bar_height)
	#width2snap += (border_width * 2)
	#height2snap += title_bar_height + border_width

	gmDispatcher.send(signal = 'statustext', msg = _('Saved screenshot to file [%s].') % filename)
	return filename

#-------------------------------------------------------------------------
def __snapshot_to_bitmap(source_dc=None, x2snap_from=0, y2snap_from=0, width2snap=1, height2snap=1):
	_log.debug('taking screenshot from %sx%s for %sx%s on [%s]', x2snap_from, y2snap_from, width2snap, height2snap, source_dc)
	target_dc = wx.MemoryDC()
	_log.debug('target DC: %s', target_dc)
	wxbmp = wx.Bitmap(width2snap, height2snap)
	target_dc.SelectObject(wxbmp)
	target_dc.Clear()						# wipe anything that might have been there in memory ?	taken from wxWidgets source
	target_dc.Blit (						# copy into this memory DC ...
		0, 0,								# ... to here in the memory DC (= target) ...
		width2snap, height2snap,			# ... that much ...
		source_dc,							# ... from the source DC ...
		x2snap_from, y2snap_from			# ... starting here
	)
	target_dc.SelectObject(wx.NullBitmap)	# disassociate wxbmp so it can safely be handled further
	target_dc.Destroy()						# destroy C++ object
	del target_dc
	return wxbmp

# ========================================================================
__curr_pat = None

def __on_post_patient_selection(**kwds):
	global __curr_pat
	__curr_pat = kwds['current_patient']

gmDispatcher.connect(signal = 'post_patient_selection', receiver = __on_post_patient_selection)

#---------------------------------------------------------------------------
def __generate_pat_str():
	if __curr_pat is None:
		return None
	data = {
		'last': __curr_pat['lastnames'].upper(),
		'first': __curr_pat['firstnames'],
		'sex': __curr_pat.gender_symbol
	}
	return ('%(last)s %(first)s (%(sex)s)' % data).strip()

#---------------------------------------------------------------------------
def decorate_window_title(title):
	if not title.startswith(gmTools._GM_TITLE_PREFIX):
		title = '%s: %s' % (
			gmTools._GM_TITLE_PREFIX,
			title.strip()
		)
	pat = __generate_pat_str()
	if (pat is not None) and (pat not in title):
		title = '%s | %s' % (title, pat)
	# FIXME: add current provider
	return title

#---------------------------------------------------------------------------
def undecorate_window_title(title):
	pat = __generate_pat_str()
	if (pat is not None) and (pat in title):
		title = title.replace(pat, '')
	title = title.replace('|', '')
	title = gmTools.strip_prefix (
		title,
		gmTools._GM_TITLE_PREFIX + ':',
		remove_repeats = True,
		remove_whitespace = True
	)
	return title.strip()

# ========================================================================
def gm_show_error(aMessage=None, aTitle = None, error=None, title=None):

	if error is None:
		error = aMessage
	if error is None:
		error = _('programmer forgot to specify error message')
	error += _("\n\nPlease consult the error log for all the gory details !")
	if title is None:
		title = aTitle
	if title is None:
		title = _('generic error message')
	dlg = wx.MessageDialog (
		parent = None,
		message = error,
		caption = decorate_window_title(title),
		style = wx.OK | wx.ICON_ERROR | wx.STAY_ON_TOP
	)
	dlg.ShowModal()
	dlg.DestroyLater()
	return True

#-------------------------------------------------------------------------
def gm_show_info(aMessage=None, aTitle=None, info=None, title=None):

	if info is None:
		info = aMessage
	if info is None:
		info = _('programmer forgot to specify info message')
	if title is None:
		title = aTitle
	if title is None:
		title = _('generic info message')
	dlg = wx.MessageDialog (
		parent = None,
		message = info,
		caption = decorate_window_title(title),
		style = wx.OK | wx.ICON_INFORMATION | wx.STAY_ON_TOP
	)
	dlg.ShowModal()
	dlg.DestroyLater()
	return True

#-------------------------------------------------------------------------
def gm_show_warning(aMessage=None, aTitle=None):
	if aMessage is None:
		aMessage = _('programmer forgot to specify warning')
	if aTitle is None:
		aTitle = _('generic warning message')

	dlg = wx.MessageDialog (
		parent = None,
		message = aMessage,
		caption = decorate_window_title(aTitle),
		style = wx.OK | wx.ICON_EXCLAMATION | wx.STAY_ON_TOP
	)
	dlg.ShowModal()
	dlg.DestroyLater()
	return True

#-------------------------------------------------------------------------
def gm_show_question(aMessage='programmer forgot to specify question', aTitle='generic user question dialog', cancel_button=False, question=None, title=None):
	if cancel_button:
		style = wx.YES_NO | wx.CANCEL | wx.ICON_QUESTION | wx.STAY_ON_TOP
	else:
		style = wx.YES_NO | wx.ICON_QUESTION | wx.STAY_ON_TOP
	if question is None:
		question = aMessage
	if title is None:
		title = aTitle
	title = decorate_window_title(title)
	dlg = wx.MessageDialog(None, question, title, style)
	btn_pressed = dlg.ShowModal()
	dlg.DestroyLater()
	if btn_pressed == wx.ID_YES:
		return True

	elif btn_pressed == wx.ID_NO:
		return False

	else:
		return None

#======================================================================
if __name__ == '__main__':

	if len(sys.argv) < 2:
		sys.exit()

	if sys.argv[1] != 'test':
		sys.exit()

	from Gnumed.pycommon import gmI18N
	gmI18N.activate_locale()
	gmI18N.install_domain(domain='gnumed')

	#------------------------------------------------------------------
	def test_scale_img():
		app = wx.App()
		img = file2scaled_image(filename = sys.argv[2])
		print(img)
		print(img.Height)
		print(img.Width)
	#------------------------------------------------------------------
	def test_sql_logic_prw():
		app = wx.PyWidgetTester(size = (200, 50))
		prw = cThreeValuedLogicPhraseWheel(app.frame, -1)
		app.frame.Show(True)
		app.MainLoop()

		return True
	#------------------------------------------------------------------
	def test_clipboard():
		app = wx.PyWidgetTester(size = (200, 50))
		result = clipboard2file()
		if result is False:
			print("problem opening clipboard")
			return
		if result is None:
			print("no data in clipboard")
			return
		print("file:", result)
	#------------------------------------------------------------------
	#test_scale_img()
	#test_sql_logic_prw()
	test_clipboard()

#======================================================================
