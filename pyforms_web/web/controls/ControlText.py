from pyforms_web.web.controls.ControlBase import ControlBase
import simplejson

class ControlText(ControlBase):

	def init_form(self):
		return """new ControlText('{0}', {1})""".format(
			self._name, 
			simplejson.dumps(self.serialize()) 
		)