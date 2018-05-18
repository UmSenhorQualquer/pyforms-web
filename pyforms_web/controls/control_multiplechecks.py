from pyforms_web.controls.control_base import ControlBase
import simplejson, collections

class ControlMultipleChecks(ControlBase):

	def __init__(self, *args, **kwargs):
		if kwargs.get('default', None) is None: kwargs['default'] = []
		super(ControlMultipleChecks, self).__init__(*args, **kwargs)
		self.mode   		= kwargs.get('mode', 'selection')
		self._update_items	= True
		self._items			= collections.OrderedDict()


	def init_form(self): return "new ControlMultipleChecks('{0}', {1})".format( self._name, simplejson.dumps(self.serialize()) )

	def add_item(self, label, value = None):
		if self._items==None: self._items={}
		
		if value==None:
			self._items[label] = label
		else:
			self._items[label] = value
	   
		self._update_items = True
		self.mark_to_update_client()


	def clear_items(self):
		self._items = {}
		self._value = None
		self.mark_to_update_client()


	def serialize(self):
		data = ControlBase.serialize(self)
		items = []
		for key, value in self._items.items():
			items.append({'text': str(key), 'value': value, 'name': str(key)})
		
		#value = str(self._value) if self._value is not None else None
		if isinstance(self._value, list) and len(self._value)>0:
			value = list(sorted(self._value))
		else:
			value = None


		data.update({ 'items': items, 'value': value, 'mode': self.mode, 'update_items': self._update_items })
		
		self._update_items = False
		return data
		
	

	def deserialize(self, properties):
		properties.update({'value':properties.get('value', [])})
		
		ControlBase.deserialize(self, properties)
		
	