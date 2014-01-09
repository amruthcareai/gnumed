"""GNUmed form/letter handling widgets."""

#================================================================
__author__ = "Karsten Hilbert <Karsten.Hilbert@gmx.net>"
__license__ = "GPL v2 or later"


import os.path
import sys
import logging
import shutil


import wx


if __name__ == '__main__':
	sys.path.insert(0, '../../')
from Gnumed.pycommon import gmI18N
from Gnumed.pycommon import gmTools
from Gnumed.pycommon import gmDispatcher
from Gnumed.pycommon import gmPrinting
from Gnumed.pycommon import gmDateTime
from Gnumed.pycommon import gmShellAPI
from Gnumed.pycommon import gmMimeLib

from Gnumed.business import gmForms
from Gnumed.business import gmPerson

from Gnumed.wxpython import gmGuiHelpers
from Gnumed.wxpython import gmListWidgets
from Gnumed.wxpython import gmMacro
from Gnumed.wxpython import gmEditArea
from Gnumed.wxpython.gmDocumentWidgets import save_files_as_new_document


_log = logging.getLogger('gm.ui')

_ID_FORM_DISPOSAL_PRINT_NOW, \
_ID_FORM_DISPOSAL_MAIL_NOW, \
_ID_FORM_DISPOSAL_FAX_NOW, \
_ID_FORM_DISPOSAL_EXPORT_NOW, \
_ID_FORM_DISPOSAL_ARCHIVE_NOW, \
_ID_FORM_DISPOSAL_SAVE_NOW = range(6)

#============================================================
# generic form generation and handling convenience functions
#------------------------------------------------------------
def print_doc_from_template(parent=None, jobtype=None, episode=None):

	form = generate_form_from_template (
		parent = parent,
		excluded_template_types = [
			u'gnuplot script',
			u'visual progress note',
			u'invoice'
		],
		edit = True
	)
	if form is None:
		return False

	if form in [True, False]:	# returned by special OOo/LO handling
		return form

	return act_on_generated_forms (
		parent = parent,
		forms = [form],
		jobtype = jobtype,
		episode_name = u'administrative',
		review_copy_as_normal = True
	)

#------------------------------------------------------------
# eventually this should become superfluous when there's a
# standard engine wrapper around OOo
def print_doc_from_ooo_template(template=None):

	# export template to file
	filename = template.export_to_file()
	if filename is None:
		gmGuiHelpers.gm_show_error (
			_(	'Error exporting form template\n'
				'\n'
				' "%s" (%s)'
			) % (template['name_long'], template['external_version']),
			_('Letter template export')
		)
		return False

	try:
		doc = gmForms.cOOoLetter(template_file = filename, instance_type = template['instance_type'])
	except ImportError:
		gmGuiHelpers.gm_show_error (
			_('Cannot connect to OpenOffice.\n\n'
			  'The UNO bridge module for Python\n'
			  'is not installed.'
			),
			_('Letter writer')
		)
		return False

	if not doc.open_in_ooo():
		gmGuiHelpers.gm_show_error (
			_('Cannot connect to OpenOffice.\n'
			  '\n'
			  'You may want to increase the option\n'
			  '\n'
			  ' <%s>'
			) % _('OOo startup time'),
			_('Letter writer')
		)
		try: os.remove(filename)
		except: pass
		return False

	doc.show(False)
	ph_handler = gmMacro.gmPlaceholderHandler()
	doc.replace_placeholders(handler = ph_handler)

	filename = filename.replace('.ott', '.odt').replace('-FormTemplate-', '-FormInstance-')
	doc.save_in_ooo(filename = filename)

	doc.show(True)

	return True

#------------------------------------------------------------
def generate_form_from_template(parent=None, template_types=None, edit=None, template=None, excluded_template_types=None):
	"""If <edit> is None it will honor the template setting."""

	if parent is None:
		parent = wx.GetApp().GetTopWindow()

	# 1) get template to use
	if template is None:
		template = manage_form_templates (
			parent = parent,
			active_only = True,
			template_types = template_types,
			excluded_types = excluded_template_types
		)
		if template is None:
			gmDispatcher.send(signal = 'statustext', msg = _('No document template selected.'), beep = False)
			return None

	if template['engine'] == u'O':
		return print_doc_from_ooo_template(template = template)

	wx.BeginBusyCursor()

	# 2) process template
	try:
		form = template.instantiate()
	except KeyError:
		_log.exception('cannot instantiate document template [%s]', template)
		gmGuiHelpers.gm_show_error (
			aMessage = _('Invalid document template [%s - %s (%s)]') % (name, ver, template['engine']),
			aTitle = _('Generating document from template')
		)
		wx.EndBusyCursor()
		return None
	ph = gmMacro.gmPlaceholderHandler()
	#ph.debug = True
	form.substitute_placeholders(data_source = ph)
	if edit is None:
		if form.template['edit_after_substitution']:
			edit = True
		else:
			edit = False
	if edit:
		wx.EndBusyCursor()
		form.edit()
		wx.BeginBusyCursor()

	# 3) generate output
	pdf_name = form.generate_output()
	wx.EndBusyCursor()
	if pdf_name is not None:
		return form

	gmGuiHelpers.gm_show_error (
		aMessage = _('Error generating document printout.'),
		aTitle = _('Generating document printout')
	)
	return None

#------------------------------------------------------------
def act_on_generated_forms(parent=None, forms=None, jobtype=None, episode_name=None, progress_note=None, review_copy_as_normal=False):
	"""This function assumes that .generate_output() has already been called on each form.

	It operates on the active patient.
	"""

	if len(forms) == 0:
		return True

	no_of_printables = 0
	for form in forms:
		no_of_printables += len(form.final_output_filenames)

	if no_of_printables == 0:
		return True

	soap_lines = []

	#-----------------------------
	def save_soap(soap=None):
		if soap.strip() == u'':
			return
		pat = gmPerson.gmCurrentPatient()
		emr = pat.get_emr()
		epi = emr.add_episode(episode_name = episode_name, is_open = False)
		emr.add_clin_narrative (
			soap_cat = None,
			note = soap,
			episode = epi
		)
	#-----------------------------
	def archive_forms(episode_name=None):
		if episode_name is None:
			epi = None				# will ask for episode further down
		else:
			pat = gmPerson.gmCurrentPatient()
			emr = pat.get_emr()
			epi = emr.add_episode(episode_name = episode_name, is_open = False)

		for form in forms:
			files2import = []
			files2import.extend(form.final_output_filenames)
			files2import.extend(form.re_editable_filenames)
			if len(files2import) == 0:
				continue
			save_files_as_new_document (
				parent = parent,
				filenames = files2import,
				document_type = form.template['instance_type'],
				unlock_patient = False,
				episode = epi,
				review_as_normal = review_copy_as_normal,
				reference = None
			)

		return True
	#-----------------------------
	def save_forms():
		# anything to do ?
		files2save = []
		form_names = []
		for form in forms:
			files2save.extend(form.final_output_filenames)
			form_names.append(u'%s (%s)' % (form.template['name_long'], form.template['external_version']))
		if len(files2save) == 0:
			return True
		# get path
		path = os.path.expanduser(os.path.join('~', 'gnumed'))
		dlg = wx.DirDialog (
			parent = parent,
			message = _('Select directory in which to create patient directory ...'),
			defaultPath = path,
			style = wx.DD_DEFAULT_STYLE
		)
		result = dlg.ShowModal()
		path = dlg.GetPath()
		dlg.Destroy()
		if result != wx.ID_OK:
			return
		# save forms
		pat = gmPerson.gmCurrentPatient()
		path = os.path.join(path, pat.dirname)
		gmTools.mkdir(path)
		_log.debug('form saving path: %s', path)
		for form in forms:
			for filename in form.final_output_filenames:
				shutil.copy2(filename, path)
		soap_lines.append(_('Saved to disk: %s') % u', '.join(form_names))
		return True
	#-----------------------------
	def print_forms():
		# anything to do ?
		files2print = []
		form_names = []
		for form in forms:
			files2print.extend(form.final_output_filenames)
			form_names.append(u'%s (%s)' % (form.template['name_long'], form.template['external_version']))
		if len(files2print) == 0:
			return True
		# print
		printed = gmPrinting.print_files(filenames = files2print, jobtype = jobtype)
		if not printed:
			gmGuiHelpers.gm_show_error (
				aMessage = _('Error printing documents.'),
				aTitle = _('Printing [%s]') % jobtype
			)
			return False
		soap_lines.append(_('Printed: %s') % u', '.join(form_names))
		return True
	#-----------------------------
	def mail_forms():
		# anything to do ?
		files2mail = []
		form_names = []
		for form in forms:
			files2mail.extend(form.final_output_filenames)
			form_names.append(u'%s (%s)' % (form.template['name_long'], form.template['external_version']))
		if len(files2mail) == 0:
			return True
		found, external_cmd = gmShellAPI.detect_external_binary('gm-mail_doc')
		if not found:
			return False
		# send mail
		cmd = u'%s %s' % (external_cmd, u' '.join(files2mail))
		if os.name == 'nt':
			blocking = True
		else:
			blocking = False
		success = gmShellAPI.run_command_in_shell (
			command = cmd,
			blocking = blocking
		)
		if not success:
			gmGuiHelpers.gm_show_error (
				aMessage = _('Error mailing documents.'),
				aTitle = _('Mailing documents')
			)
			return False
		soap_lines.append(_('Mailed: %s') % u', '.join(form_names))
		return True
	#-----------------------------
	def fax_forms(fax_number=None):
		# anything to do ?
		files2fax = []
		form_names = []
		for form in forms:
			files2fax.extend(form.final_output_filenames)
			form_names.append(u'%s (%s)' % (form.template['name_long'], form.template['external_version']))
		if len(files2fax) == 0:
			return True
		found, external_cmd = gmShellAPI.detect_external_binary('gm-fax_doc')
		if not found:
			return False
		# send fax
		cmd = u'%s "%s" %s' % (external_cmd, fax_number, u' '.join(files2fax))
		if os.name == 'nt':
			blocking = True
		else:
			blocking = False
		success = gmShellAPI.run_command_in_shell (
			command = cmd,
			blocking = blocking
		)
		if not success:
			gmGuiHelpers.gm_show_error (
				aMessage = _('Error faxing documents to\n\n  %s') % fax_number,
				aTitle = _('Faxing documents')
			)
			return False
		soap_lines.append(_('Faxed to %s: %s') % (fax_number, u', '.join(form_names)))
		return True
	#-----------------------------
	def export_forms():
		pat = gmPerson.gmCurrentPatient()
		return pat.export_area.add_forms(forms = forms)
	#-----------------------------

	if parent is None:
		parent = wx.GetApp().GetTopWindow()

	if jobtype is None:
		jobtype = 'generic_document'

	dlg = cFormDisposalDlg(parent, -1)
	dlg.forms = forms
	dlg.progress_note = progress_note
	dlg.episode_name = episode_name
	action_code = dlg.ShowModal()

	if action_code == wx.ID_CANCEL:
		dlg.Destroy()
		return True

	forms = dlg._LCTRL_forms.get_item_data()
	if len(forms) == 0:
		dlg.Destroy()
		return True

	progress_note = dlg.progress_note
	episode_name = dlg._PRW_episode.GetValue().strip()
	do_save = dlg._CHBOX_save.GetValue()
	do_print = dlg._CHBOX_print.GetValue()
	do_mail = dlg._CHBOX_mail.GetValue()
	fax_number = dlg._PRW_fax.GetValue().strip()
	dlg.Destroy()

	if action_code == wx.ID_OK:
		if episode_name != u'':
			result = archive_forms(episode_name = episode_name)
		if do_save:
			result = save_forms()
		if do_print:
			result = print_forms()
		if do_mail:
			result = mail_forms()
		if fax_number != u'':
			result = fax_forms(fax_number = fax_number)
		if progress_note != u'':
			soap_lines.insert(0, progress_note)
		if len(soap_lines) > 0:
			save_soap(soap = u'\n'.join(soap_lines))
		return result

	success = False
	keep_a_copy = False
	if action_code == _ID_FORM_DISPOSAL_PRINT_NOW:
		if episode_name != u'':
			keep_a_copy = True
		success = print_forms()

	elif action_code == _ID_FORM_DISPOSAL_ARCHIVE_NOW:
		if episode_name == u'':
			episode_name = None
		keep_a_copy = True
		success = True

	elif action_code == _ID_FORM_DISPOSAL_SAVE_NOW:
		if episode_name != u'':
			keep_a_copy = True
		success = save_forms()

	elif action_code == _ID_FORM_DISPOSAL_MAIL_NOW:
		if episode_name != u'':
			keep_a_copy = True
		success = mail_forms()

	elif action_code == _ID_FORM_DISPOSAL_FAX_NOW:
		if episode_name != u'':
			keep_a_copy = True
		success = fax_forms(fax_number = fax_number)

	elif action_code == _ID_FORM_DISPOSAL_EXPORT_NOW:
		success = export_forms()

	if not success:
		return False

	if progress_note != u'':
		soap_lines.insert(0, progress_note)
	if len(soap_lines) > 0:
		save_soap(soap = u'\n'.join(soap_lines))

	if keep_a_copy:
		archive_forms(episode_name = episode_name)

	return True

#============================================================
from Gnumed.wxGladeWidgets import wxgFormDisposalDlg

class cFormDisposalDlg(wxgFormDisposalDlg.wxgFormDisposalDlg):

	def __init__(self, *args, **kwargs):

		wxgFormDisposalDlg.wxgFormDisposalDlg.__init__(self, *args, **kwargs)

		self.__init_ui()

	#--------------------------------------------------------
	# properties
	#--------------------------------------------------------
	def _set_msg(self, msg):
		self._LBL_msg.SetLabel(msg)
		self._LBL_msg.Refresh()

	message = property(lambda x:x, _set_msg)

	#--------------------------------------------------------
	def _set_forms(self, forms):
		items = [ f.template['name_long'] for f in forms ]
		self._LCTRL_forms.set_string_items(items)
		self._LCTRL_forms.set_data(forms)

	forms = property(lambda x:x, _set_forms)

	#--------------------------------------------------------
	def _get_note(self):
		return self._TCTRL_soap.GetValue().strip()

	def _set_note(self, note):
		if note is None:
			note = u''
		self._TCTRL_soap.SetValue(note)

	progress_note = property(_get_note, _set_note)

	#--------------------------------------------------------
	def _get_episode_name(self):
		return self._PRW_episode.GetValue().strip()

	def _set_episode_name(self, episode_name):
		if episode_name is None:
			episode_name = u''
		self._PRW_episode.SetValue(episode_name)

	episode_name = property(_get_episode_name, _set_episode_name)

	#--------------------------------------------------------
	# internal helpers
	#--------------------------------------------------------
	def __init_ui(self):
		self._LCTRL_forms.set_columns([_('Form')])

		self.__mail_script_exists, path = gmShellAPI.detect_external_binary(binary = r'gm-mail_doc')
		if not self.__mail_script_exists:
			self._LBL_mail.Disable()
			self._CHBOX_mail.SetLabel(_('<gm-mail_doc(.bat) not found>'))
			self._CHBOX_mail.SetValue(False)
			self._CHBOX_mail.Disable()
			self._BTN_mail.Disable()

		self.__fax_script_exists, path = gmShellAPI.detect_external_binary(binary = r'gm-fax_doc')
		if not self.__fax_script_exists:
			self._LBL_fax.Disable()
			self._PRW_fax.SetText(_('<gm-fax_doc(.bat) not found>'), data = None)
			self._PRW_fax.display_as_disabled(True)
			self._PRW_fax.Disable()
			self._BTN_fax.Disable()

		self._CHBOX_export.SetValue(False)

	#--------------------------------------------------------
	# event handlers
	#--------------------------------------------------------
	def _on_print_button_pressed(self, event):
		self.EndModal(_ID_FORM_DISPOSAL_PRINT_NOW)
	#--------------------------------------------------------
	def _on_mail_button_pressed(self, event):
		event.Skip()
		if not self.__mail_script_exists:
			return
		self.EndModal(_ID_FORM_DISPOSAL_MAIL_NOW)
	#--------------------------------------------------------
	def _on_fax_button_pressed(self, event):
		event.Skip()
		if not self.__fax_script_exists:
			return
		self.EndModal(_ID_FORM_DISPOSAL_FAX_NOW)
	#--------------------------------------------------------
	def _on_export_button_pressed(self, event):
		self.EndModal(_ID_FORM_DISPOSAL_EXPORT_NOW)
	#--------------------------------------------------------
	def _on_archive_button_pressed(self, event):
		self.EndModal(_ID_FORM_DISPOSAL_ARCHIVE_NOW)
	#--------------------------------------------------------
	def _on_save_button_pressed(self, event):
		self.EndModal(_ID_FORM_DISPOSAL_SAVE_NOW)
	#--------------------------------------------------------
	def _on_show_forms_button_pressed(self, event):
		event.Skip()
		forms2show = self._LCTRL_forms.get_selected_item_data()
		if len(forms2show) == 0:
			return
		for form in forms2show:
			for filename in form.final_output_filenames:
				gmMimeLib.call_viewer_on_file(filename, block = True)
	#--------------------------------------------------------
	def _on_delete_forms_button_pressed(self, event):
		print "Event handler '_on_delete_forms_button_pressed' not implemented!"
		event.Skip()
	#--------------------------------------------------------
	def _on_ok_button_pressed(self, event):
		self.EndModal(wx.ID_OK)

#============================================================
# form template management
#------------------------------------------------------------
def edit_template(parent=None, template=None, single_entry=False):
	ea = cFormTemplateEAPnl(parent = parent, id = -1)
	ea.data = template
	ea.mode = gmTools.coalesce(template, 'new', 'edit')
	dlg = gmEditArea.cGenericEditAreaDlg2(parent = parent, id = -1, edit_area = ea, single_entry = single_entry)
	dlg.SetTitle(gmTools.coalesce(template, _('Adding new form template'), _('Editing form template')))
	if dlg.ShowModal() == wx.ID_OK:
		dlg.Destroy()
		return True
	dlg.Destroy()
	return False

#------------------------------------------------------------
def manage_form_templates(parent=None, template_types=None, active_only=False, excluded_types=None, msg=None):

	if parent is None:
		parent = wx.GetApp().GetTopWindow()

	#-------------------------
	def edit(template=None):
		return edit_template(parent = parent, template = template)
	#-------------------------
	def delete(template):
		delete = gmGuiHelpers.gm_show_question (
			aTitle = _('Deleting form template.'),
			aMessage = _(
				'Are you sure you want to delete\n'
				'the following form template ?\n\n'
				' "%s (%s)"\n\n'
				'You can only delete templates which\n'
				'have not yet been used to generate\n'
				'any forms from.'
			) % (template['name_long'], template['external_version'])
		)
		if delete:
			# FIXME: make this a priviledged operation ?
			gmForms.delete_form_template(template = template)
			return True
		return False
	#-------------------------
	def refresh(lctrl):
		templates = gmForms.get_form_templates(active_only = active_only, template_types = template_types, excluded_types = excluded_types)
		lctrl.set_string_items(items = [ [t['name_long'], t['external_version'], gmForms.form_engine_names[t['engine']]] for t in templates ])
		lctrl.set_data(data = templates)
	#-------------------------
	template = gmListWidgets.get_choices_from_list (
		parent = parent,
		msg = msg,
		caption = _('Select letter or form template.'),
		columns = [_('Template'), _('Version'), _('Type')],
		edit_callback = edit,
		new_callback = edit,
		delete_callback = delete,
		refresh_callback = refresh,
		single_selection = True
	)

	return template

#------------------------------------------------------------
from Gnumed.wxGladeWidgets import wxgFormTemplateEditAreaPnl

class cFormTemplateEAPnl(wxgFormTemplateEditAreaPnl.wxgFormTemplateEditAreaPnl, gmEditArea.cGenericEditAreaMixin):

	def __init__(self, *args, **kwargs):

		try:
			data = kwargs['template']
			del kwargs['template']
		except KeyError:
			data = None

		wxgFormTemplateEditAreaPnl.wxgFormTemplateEditAreaPnl.__init__(self, *args, **kwargs)
		gmEditArea.cGenericEditAreaMixin.__init__(self)

		self.full_filename = None

		self.mode = 'new'
		self.data = data
		if data is not None:
			self.mode = 'edit'

		self.__init_ui()
	#----------------------------------------------------------------
	def __init_ui(self):
		self._PRW_name_long.matcher = gmForms.cFormTemplateNameLong_MatchProvider()
		self._PRW_name_short.matcher = gmForms.cFormTemplateNameShort_MatchProvider()
		self._PRW_template_type.matcher = gmForms.cFormTemplateType_MatchProvider()
	#----------------------------------------------------------------
	# generic Edit Area mixin API
	#----------------------------------------------------------------
	def _valid_for_save(self):

		validity = True

		# self._TCTRL_filename
		self.display_tctrl_as_valid(tctrl = self._TCTRL_filename, valid = True)
		fname = self._TCTRL_filename.GetValue().strip()
		# 1) new template: file must exist
		if self.data is None:
			try:
				open(fname, 'r').close()
			except:
				validity = False
				self.display_tctrl_as_valid(tctrl = self._TCTRL_filename, valid = False)
				self.status_message = _('You must select a template file before saving.')
				self._TCTRL_filename.SetFocus()
		# 2) existing template
		# - empty = no change
		# - does not exist: name change in DB field
		# - does exist: reload from filesystem

		# self._PRW_instance_type
		if self._PRW_instance_type.GetValue().strip() == u'':
			validity = False
			self._PRW_instance_type.display_as_valid(False)
			self.status_message = _('You must enter a type for documents created with this template.')
			self._PRW_instance_type.SetFocus()
		else:
			self._PRW_instance_type.display_as_valid(True)

		# self._PRW_template_type
		if self._PRW_template_type.GetData() is None:
			validity = False
			self._PRW_template_type.display_as_valid(False)
			self.status_message = _('You must enter a type for this template.')
			self._PRW_template_type.SetFocus()
		else:
			self._PRW_template_type.display_as_valid(True)

		# self._TCTRL_external_version
		if self._TCTRL_external_version.GetValue().strip() == u'':
			validity = False
			self.display_tctrl_as_valid(tctrl = self._TCTRL_external_version, valid = False)
			self.status_message = _('You must enter a version for this template.')
			self._TCTRL_external_version.SetFocus()
		else:
			self.display_tctrl_as_valid(tctrl = self._TCTRL_external_version, valid = True)

		# self._PRW_name_short
		if self._PRW_name_short.GetValue().strip() == u'':
			validity = False
			self._PRW_name_short.display_as_valid(False)
			self.status_message = _('Missing short name for template.')
			self._PRW_name_short.SetFocus()
		else:
			self._PRW_name_short.display_as_valid(True)

		# self._PRW_name_long
		if self._PRW_name_long.GetValue().strip() == u'':
			validity = False
			self._PRW_name_long.display_as_valid(False)
			self.status_message = _('Missing long name for template.')
			self._PRW_name_long.SetFocus()
		else:
			self._PRW_name_long.display_as_valid(True)

		return validity
	#----------------------------------------------------------------
	def _save_as_new(self):
		data = gmForms.create_form_template (
			template_type = self._PRW_template_type.GetData(),
			name_short = self._PRW_name_short.GetValue().strip(),
			name_long = self._PRW_name_long.GetValue().strip()
		)
		data['external_version'] = self._TCTRL_external_version.GetValue()
		data['instance_type'] = self._PRW_instance_type.GetValue().strip()
		data['filename'] = os.path.split(self._TCTRL_filename.GetValue().strip())[1]
		data['in_use'] = self._CHBOX_active.GetValue()
		data['edit_after_substitution'] = self._CHBOX_editable.GetValue()
		data['engine'] = gmForms.form_engine_abbrevs[self._CH_engine.GetSelection()]
		data.save()

		data.update_template_from_file(filename = self._TCTRL_filename.GetValue().strip())

		self.data = data
		return True
	#----------------------------------------------------------------
	def _save_as_update(self):
		self.data['pk_template_type'] = self._PRW_template_type.GetData()
		self.data['name_short'] = self._PRW_name_short.GetValue().strip()
		self.data['name_long'] = self._PRW_name_long.GetValue().strip()
		self.data['external_version'] = self._TCTRL_external_version.GetValue()
		tmp = self._PRW_instance_type.GetValue().strip()
		if tmp not in [self.data['instance_type'], self.data['l10n_instance_type']]:
			self.data['instance_type'] = tmp
		tmp = os.path.split(self._TCTRL_filename.GetValue().strip())[1]
		if tmp != u'':
			self.data['filename'] = tmp
		self.data['in_use'] = self._CHBOX_active.GetValue()
		self.data['edit_after_substitution'] = self._CHBOX_editable.GetValue()
		self.data['engine'] = gmForms.form_engine_abbrevs[self._CH_engine.GetSelection()]
		self.data.save()

		fname = self._TCTRL_filename.GetValue().strip()
		try:
			open(fname, 'r').close()
			self.data.update_template_from_file(filename = fname)
		except:
			pass # filename column already updated

		return True
	#----------------------------------------------------------------
	def _refresh_as_new(self):
		self._PRW_name_long.SetText(u'')
		self._PRW_name_short.SetText(u'')
		self._TCTRL_external_version.SetValue(u'')
		self._PRW_template_type.SetText(u'')
		self._PRW_instance_type.SetText(u'')
		self._TCTRL_filename.SetValue(u'')
		self._CH_engine.SetSelection(0)
		self._CHBOX_active.SetValue(True)
		self._CHBOX_editable.SetValue(True)
		self._LBL_status.SetLabel(u'')
		self._BTN_export.Enable(False)

		self._PRW_name_long.SetFocus()
	#----------------------------------------------------------------
	def _refresh_as_new_from_existing(self):
		self._refresh_as_new()
	#----------------------------------------------------------------
	def _refresh_from_existing(self):
		self._PRW_name_long.SetText(self.data['name_long'])
		self._PRW_name_short.SetText(self.data['name_short'])
		self._TCTRL_external_version.SetValue(self.data['external_version'])
		self._PRW_template_type.SetText(self.data['l10n_template_type'], data = self.data['pk_template_type'])
		self._PRW_instance_type.SetText(self.data['l10n_instance_type'], data = self.data['instance_type'])
		self._TCTRL_filename.SetValue(self.data['filename'])
		self._CH_engine.SetSelection(gmForms.form_engine_abbrevs.index(self.data['engine']))
		self._CHBOX_active.SetValue(self.data['in_use'])
		self._CHBOX_editable.SetValue(self.data['edit_after_substitution'])
		self._LBL_status.SetLabel(_('last modified %s by %s') % (
			gmDateTime.pydt_strftime(self.data['last_modified'], '%Y %B %d'),
			self.data['modified_by']
		))

		self._TCTRL_filename.Enable(True)
		self._BTN_load.Enable(True)
		self._BTN_export.Enable(True)

		self._BTN_load.SetFocus()
	#----------------------------------------------------------------
	# event handlers
	#----------------------------------------------------------------
	def _on_load_button_pressed(self, event):
		engine_abbrev = gmForms.form_engine_abbrevs[self._CH_engine.GetSelection()]

		wildcards = []
		try:
			wildcards.append(u'%s (%s)|%s' % (
				gmForms.form_engine_names[engine_abbrev],
				gmForms.form_engine_template_wildcards[engine_abbrev],
				gmForms.form_engine_template_wildcards[engine_abbrev]
			))
		except KeyError:
			pass
		wildcards.append(u"%s (*)|*" % _('all files'))
		wildcards.append(u"%s (*.*)|*.*" % _('all files (Windows)'))

		dlg = wx.FileDialog (
			parent = self,
			message = _('Choose a form template file'),
			defaultDir = os.path.expanduser(os.path.join('~', 'gnumed')),
			defaultFile = '',
			wildcard = '|'.join(wildcards),
			style = wx.OPEN | wx.HIDE_READONLY | wx.FILE_MUST_EXIST
		)
		result = dlg.ShowModal()
		if result != wx.ID_CANCEL:
			self._TCTRL_filename.SetValue(dlg.GetPath())
		dlg.Destroy()

		event.Skip()
	#----------------------------------------------------------------
	def _on_export_button_pressed(self, event):
		if self.data is None:
			return

		engine_abbrev = gmForms.form_engine_abbrevs[self._CH_engine.GetSelection()]

		wildcards = []
		try:
			wildcards.append(u'%s (%s)|%s' % (
				gmForms.form_engine_names[engine_abbrev],
				gmForms.form_engine_template_wildcards[engine_abbrev],
				gmForms.form_engine_template_wildcards[engine_abbrev]
			))
		except KeyError:
			pass
		wildcards.append(u"%s (*)|*" % _('all files'))
		wildcards.append(u"%s (*.*)|*.*" % _('all files (Windows)'))

		dlg = wx.FileDialog (
			parent = self,
			message = _('Enter a filename to save the template to'),
			defaultDir = os.path.expanduser(os.path.join('~', 'gnumed')),
			defaultFile = '',
			wildcard = '|'.join(wildcards),
			style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT | wx.HIDE_READONLY
		)
		result = dlg.ShowModal()
		if result != wx.ID_CANCEL:
			fname = dlg.GetPath()
			self.data.export_to_file(filename = fname)
		dlg.Destroy()

		event.Skip()

#============================================================
# main
#------------------------------------------------------------
if __name__ == '__main__':

	gmI18N.activate_locale()
	gmI18N.install_domain(domain = 'gnumed')

	#----------------------------------------
	def test_cFormTemplateEAPnl():
		app = wx.PyWidgetTester(size = (400, 300))
		pnl = cFormTemplateEAPnl(app.frame, -1, template = gmForms.cFormTemplate(aPK_obj=4))
		app.frame.Show(True)
		app.MainLoop()
		return
	#----------------------------------------
	if (len(sys.argv) > 1) and (sys.argv[1] == 'test'):
		test_cFormTemplateEAPnl()

#============================================================
