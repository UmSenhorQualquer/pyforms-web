from pyforms_web.web.controls.ControlBase import ControlBase
import simplejson

class ControlFloat(ControlBase):

	def init_form(self):
		return """new ControlFloat('{0}', {1})""".format(
			self._name, 
			simplejson.dumps(self.serialize()) 
		)

	@property
	def value(self): return ControlBase.value.fget(self)

	@value.setter
	def value(self, value): ControlBase.value.fset(self, value)