from pyforms_web.web.Controls.ControlBase import ControlBase
import simplejson

class ControlInteger(ControlBase):

	def init_form(self):

		return """new ControlInteger('{0}', {1})""".format(
			self._name, 
			simplejson.dumps(self.serialize()) 
		)

	@property
	def value(self): return ControlBase.value.fget(self)

	@value.setter
	def value(self, value):
		try:
			if isinstance(value, str):
				value = int(value) if len(value)>0 else None
			ControlBase.value.fset(self, value)
			self.error = False
			
		except Exception as e:
			self.error = True
			self.mark_to_update_client()
			raise e
		

	def clean_field(self):
		if isinstance(value, str): 
			raise Exception('The field {0} should be of type integer')