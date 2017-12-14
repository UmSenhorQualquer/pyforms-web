from pyforms_web.web.Controls.ControlBase import ControlBase
import simplejson

class ControlSlider(ControlBase):

	_min = 0
	_max = 100

	def __init__(self, *args, **kwargs):
		self._min 		 = kwargs.get('min', 0)
		self._max 		 = kwargs.get('max', 100)
		self._updateSlider = True
		self._value = 0
		
		ControlBase.__init__(self, *args, **kwargs)
		
	def init_form(self): return "new ControlSlider('{0}', {1})".format( self._name, simplejson.dumps(self.serialize()) )



	def changed(self): pass
	

	@property
	def min(self): return self._min

	@min.setter
	def min(self, value):
		if self._min!=value: self.mark_to_update_client()
		self._min = value

	@property
	def max(self):  return  self._max

	@max.setter
	def max(self, value):
		if self._max!=value: self.mark_to_update_client()
		self._max = value

	@property
	def value(self): return int(self._value)

	@value.setter
	def value(self, value):
		oldvalue = self._value
		self._value = int(value)
		if oldvalue!=value: 
			self.mark_to_update_client()
			self.changed_event()


	def serialize(self):
		data = ControlBase.serialize(self)
		data.update({ 'max': self.max, 'min': self.min })
		return data
		
	def deserialize(self, properties):
		ControlBase.deserialize(self,properties)
		self.max = properties[u'max']
		self.min = properties[u'min']
		