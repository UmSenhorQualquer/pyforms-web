from pyforms_web.controls.control_base import ControlBase
import simplejson

class ControlSimpleLabel(ControlBase):
	def __init__(self, *args, **kwargs):
		self._css = ''
		super().__init__(*args, **kwargs)

	def init_form(self):
		return """new ControlSimpleLabel('{0}', {1})""".format(
			self._name,
			simplejson.dumps(self.serialize())
		)

	def deserialize(self, properties): pass

	def serialize(self):
		res = super().serialize()
		if self.value:
			res.update({'value': "<br />".join(self.value.split("\n"))})
		return res