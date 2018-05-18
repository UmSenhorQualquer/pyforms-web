from .control_text import ControlText
import simplejson

class ControlTextArea(ControlText):

	def init_form(self):
		return """new ControlTextArea('{0}', {1})""".format(
			self._name, 
			simplejson.dumps(self.serialize()) 
		)

