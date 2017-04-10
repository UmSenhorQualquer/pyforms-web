from pyforms_web.web.Controls.ControlBase import ControlBase
import simplejson

class ControlLabel(ControlBase):
	def __init__(self, label="", defaultValue="", helptext=''):
		self._css = ''
		super(ControlLabel, self).__init__(label, defaultValue, helptext)

	def init_form(self):
		return """new ControlLabel('{0}', {1})""".format(
			self._name,
			simplejson.dumps(self.serialize())
		)
