from pyforms_web.web.Controls.ControlBase import ControlBase
import simplejson

class ControlCheckBox(ControlBase):

	def init_form(self): return "new ControlCheckBox('{0}', {1})".format( self._name, simplejson.dumps(self.serialize()) )

	def serialize(self):
		return { 
			'name':     str(self.__class__.__name__), 
			'value':    self.value,
			'label':    str(self._label if self._label else ''),
			'help':     str(self._help if self._help else ''),
			'visible':  int(self._visible)
		}

	def deserialize(self, properties):
		self.value    = properties.get('value',None)=='True' or properties.get('value',None)=='true' or properties.get('value',None)==True
		self._label   = properties.get('label','')
		self._help    = properties.get('help','')
		self._visible = properties.get('visible',True)