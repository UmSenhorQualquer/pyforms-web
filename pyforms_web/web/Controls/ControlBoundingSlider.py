from pyforms_web.web.Controls.ControlBase import ControlBase

class ControlBoundingSlider(ControlBase):

	def __init__(self, label = "", defaultValue=(0,100) , min = 0, max = 100, horizontal=False, helpText=''):
		self._min = min
		self._max = max
		self._horizontal = horizontal
		super(ControlBoundingSlider, self).__init__(label, defaultValue, helpText)
		
		
	def init_form(self):
		return "new ControlBoundingSlider('{0}', {1})".format( self._name, str(self.serialize()) )

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