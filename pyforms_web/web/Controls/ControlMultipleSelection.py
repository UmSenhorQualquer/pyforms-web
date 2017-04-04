from pyforms_web.web.Controls.ControlBase import ControlBase
import simplejson

class ControlMultipleSelection(ControlBase):

	def __init__(self, label = "",  defaultValue = [],helptext=''):
		super(ControlMultipleSelection, self).__init__(label, defaultValue, helptext)
		self._items={}

	def init_form(self): return "new ControlMultipleSelection('{0}', {1})".format( self._name, simplejson.dumps(self.serialize()) )

	def add_item(self, label, value = None):
		if self._items==None: self._items={}
		
		if value==None:
			self._items[label] = label
		else:
			self._items[label] = value
	   
		self.mark_to_update_client()



	def serialize(self):
		data = ControlBase.serialize(self)
		items = []
		for key, value in self._items.items():
			value = int(value) if isinstance(value, int) else value
			items.append({'label': str(key), 'value': value}) 

		value = int(self._value) if isinstance(self._value, int) else self._value
			
		data.update({ 'items': items, 'value': value})
		return data
		
	def deserialize(self, properties):
		ControlBase.deserialize(self,properties)
		self._items = {}

		for item in properties['items']:
			self.add_item(item['label'], item['value'])

		self.value = properties['value']
