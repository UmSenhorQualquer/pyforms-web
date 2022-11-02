from pyforms_web.controls.control_base import ControlBase
import simplejson


class ControlFile(ControlBase):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.search_path = kwargs.get('path', '/')

	def init_form(self):
		return "new ControlFile('{0}', {1})".format( self._name, simplejson.dumps(self.serialize()))

	def open_file_browser(self):
		from pyforms_web.widgets.django.filesbrowser import FilesBrowserApp
		self._win = FilesBrowserApp(file_selected_event=self.__update_filepath, path=self.search_path)

	def __update_filepath(self, filename):
		self.value = filename
		self._win.close()
