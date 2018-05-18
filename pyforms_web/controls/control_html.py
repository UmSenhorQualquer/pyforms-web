from pyforms_web.controls.control_base import ControlBase
import simplejson

class ControlHtml(ControlBase):

	def init_form(self):
		return """new ControlHtml('{0}', {1})""".format(
			self._name, 
			simplejson.dumps(self.serialize()) 
		)

	def deserialize(self, properties):
		self._label   = properties.get('label','')
		self._help    = properties.get('help','')
		self._visible = properties.get('visible',True)