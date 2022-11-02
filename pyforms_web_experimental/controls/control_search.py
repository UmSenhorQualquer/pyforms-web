from pyforms_web.controls.control_base import ControlBase
import simplejson

class ControlSearch(ControlBase):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def init_form(self):
		return """new ControlSearch('{0}', {1})""".format(
			self._name,
			simplejson.dumps(self.serialize())
		)
