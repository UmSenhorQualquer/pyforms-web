from pyforms_web.basewidget import custom_json_converter
from pyforms_web.controls.control_base import ControlBase
import simplejson

class ControlHtml(ControlBase):

	def init_form(self):
		return """new ControlHtml('{0}', {1})""".format(
			self._name, 
			simplejson.dumps(self.serialize(), default=custom_json_converter)
		)

	def deserialize(self, properties):
		self._label   = properties.get('label','')
		self._help    = properties.get('help','')
		self._visible = properties.get('visible',True)