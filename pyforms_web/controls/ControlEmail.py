from pyforms_web.controls.ControlText import ControlText
import simplejson

class ControlEmail(ControlText):

	def init_form(self):
		return """new ControlEmail('{0}', {1})""".format(
			self._name, 
			simplejson.dumps(self.serialize()) 
		)