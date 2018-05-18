from pyforms_web.controls.control_base import ControlBase
import simplejson, collections

class ControlMultipleSelection(ControlBase):

	def __init__(self, *args, **kwargs):
		if kwargs.get('default', None) is None: kwargs['default'] = []
		super(ControlMultipleSelection, self).__init__(*args, **kwargs)
		self.mode   		= kwargs.get('mode', 'selection')
		self._update_items	= True
		self._items			= collections.OrderedDict()


	def init_form(self): return "new ControlMultipleSelection('{0}', {1})".format( self._name, simplejson.dumps(self.serialize()) )

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
			items.append({'text': str(key), 'value': str(value), 'name': str(key)})
		
		#value = str(self._value) if self._value is not None else None
		if isinstance(self._value, list) and len(self._value)>0:
			value = list(map(str,sorted(self._value)))
		else:
			value = None


		data.update({ 'items': items, 'value': value, 'mode': self.mode, 'update_items': self._update_items })
		
		self._update_items = False
		return data
		
	

	def deserialize(self, properties):
		value = properties.get('value', [])
		values = []
		for v in value:
			if len(v.strip())>0:
				values.append(v)
		properties.update({'value':values})
		
		ControlBase.deserialize(self, properties)
		
	