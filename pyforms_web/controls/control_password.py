from pyforms_web.controls.control_base import ControlBase
import simplejson

class ControlPassword(ControlBase):

	def init_form(self):
		return """new ControlPassword('{0}', {1})""".format(
			self._name, 
			simplejson.dumps(self.serialize()) 
		)