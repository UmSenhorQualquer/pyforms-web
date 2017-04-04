import datetime
from pyforms_web.web.Controls.ControlBase import ControlBase
import simplejson

class ControlDate(ControlBase):

	PYTHON_FORMAT = "%Y-%m-%d"
	JS_FORMAT = "Y-m-d"

	def init_form(self): return "new ControlDate('{0}', {1})".format( self._name, simplejson.dumps(self.serialize()) )

	@property
	def value(self): 
		if isinstance(self._value, (str,str) ):
			return self._value
		elif self._value==None:
			return ''
		else:
			return self._value.strftime("%Y-%m-%d")
			

	@value.setter
	def value(self, value):		
		oldvalue = self._value
		self._value = value
		if oldvalue!=value: 
			self.mark_to_update_client()
			self.changed_event()


	def serialize(self):
		data = ControlBase.serialize(self)
		data.update({'format':self.JS_FORMAT})
		return data
