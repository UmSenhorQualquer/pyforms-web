import datetime
from pyforms_web.web.Controls.ControlBase import ControlBase
import simplejson

class ControlDateTime(ControlBase):

	PYTHON_FORMAT = "%Y-%m-%d %H:%M"
	JS_FORMAT = "Y-m-d"

	def init_form(self): return "new ControlDateTime('{0}', {1})".format( self._name, simplejson.dumps(self.serialize()) )

	@property
	def value(self): 
		if isinstance(self._value, (str,unicode)):
			return self._value
		elif self._value==None:
			return ''
		else:
			return self._value.strftime(self.PYTHON_FORMAT)
			

	@value.setter
	def value(self, value):
		ControlBase.value.fset(self, value)


	def serialize(self):
		data = ControlBase.serialize(self)
		data.update({'format':self.JS_FORMAT})
		return data
