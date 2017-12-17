from django.core.exceptions import ObjectDoesNotExist
from pyforms import BaseWidget
from pyforms.Controls import ControlText
from pyforms.Controls import ControlCombo
from pyforms.Controls import ControlList
from pyforms.Controls import ControlCheckBox
from pyforms.Controls import ControlButton
from django.utils import timezone

from pysettings import conf

import uuid, time, os

def sizeof_fmt(num):
	for x in ['bytes','KB','MB','GB']:
		if num < 1000.0: return "%3.1f%s" % (num, x)
		num /= 1000.0
	return "%3.1f%s" % (num, 'TB')


class FilesBrowserApp(BaseWidget):
	
	def __init__(self):
		super(FilesBrowserApp,self).__init__('Files browser')
		
		self._control_id  	= ControlText('Input id')
		self._only_folders 	= ControlCheckBox('Only folders')
		self._directory  	= ControlText('Current directory', '/')
		self._files_table 	= ControlList('Files')
		
		self._formset = [
			'_directory',
			'_files_table',
		]

		self._files_table.item_selection_changed_event = self.__file_selected
		self._files_table.dbl_click 		   = self.__file_dblclick
	
		

	def init_form(self):
		self._files_table.horizontal_headers 	= [
			'','File','Type','Size','Modifed', ''
		]
		self._files_table.select_entire_row 	= True
		self._files_table.readonly 			= True

		request = PyFormsMiddleware.get_request()
		self._control_id.value = request.GET.get('control-id','')
		self._only_folders.value = request.GET.get('filter-folders','false')=='true'
		
		
		self.populate_table()
		return super(FilesBrowserApp, self).init_form()

	def __file_selected(self):
		pass


	def __file_dblclick(self):
		selected_row = self._files_table.value[self._files_table.selected_row_index]
		filetype 	 = selected_row[2]
		if filetype.lower()=='dir':
			if selected_row[1]=='..':
				self._directory.value = os.path.dirname(self._directory.value)
			else:
				self._directory.value = os.path.join(self._directory.value, selected_row[1])
			self.populate_table()

	def populate_table(self):
		request 	= PyFormsMiddleware.get_request()
		self._directory.value = request.GET.get('p',self._directory.value)
		storage 	= conf.MAESTRO_STORAGE_MANAGER.get(request.user)
		path 		= self._directory.value

		files 		= []
		for index, f in enumerate(storage.list(path)):
			if self._only_folders.value and f.type.lower()!='dir': continue

			link = ''
			if f.type.lower()!='dir':
				function = 'javascript:add_file2control("{1}", "{0}");'.format(f.fullpath, self._control_id.value)
				link = """<a target='_blank' href='{0}' ><i class='selected radio icon' ></id></a>""".format( function )

			if self._only_folders.value:
				function = 'javascript:add_file2control("{1}", "{0}");'.format(f.fullpath, self._control_id.value)
				link = """<a target='_blank' href='{0}' ><i class='selected radio icon' ></id></a>""".format( function )

			files.append([
				"<i class='folder icon' ></id>" if f.type.lower()=='dir' else "<i class='file outline icon' ></id>",
				f.filename, 
				f.type, 
				sizeof_fmt( f.size ),
				f.lastmodified,
				link
			])

		self._files_table.value = ([['','..', 'dir']] if path!='/' else []) + sorted(files, key=lambda a: (a[2], a[1]))

