from pyforms_web.controls.control_base import ControlBase
import simplejson

class ControlBoundingSlider(ControlBase):

	def __init__(self, *args, **kwargs):
		self._min 		 = kwargs.get('min', 0)
		self._max 		 = kwargs.get('max', 100)
		self._horizontal = kwargs.get('horizontal', False)
		super(ControlBoundingSlider, self).__init__(*args, **kwargs)
		
		
	def init_form(self):
		return u"new ControlBoundingSlider('{0}', {1})".format( self._name, simplejson.dumps(self.serialize()) )

	@property
	def min(self): return self._min

	@min.setter
	def min(self, value):  
		if self._min!=value: self.mark_to_update_client()
		self._min = value

	@property
	def max(self): return self._max

	@max.setter
	def max(self, value): 
		if self._max!=value: self.mark_to_update_client()
		self._max = value

	def serialize(self):
		data = super(ControlBoundingSlider, self).serialize()
		data.update({ 'max': self.max, 'min': self.min })
		return data

	def deserialize(self, properties):
		super(ControlBoundingSlider, self).deserialize(properties)
		self.max = properties['max']
		self.min = properties['min']