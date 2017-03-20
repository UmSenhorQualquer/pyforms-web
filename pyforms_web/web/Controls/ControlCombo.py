from pyforms_web.web.Controls.ControlBase import ControlBase
import simplejson, collections

class ControlCombo(ControlBase):


	def __init__(self, label = "", defaultValue = "", helptext=''):
		super(ControlCombo, self).__init__(label, defaultValue,helptext)
		self._items = collections.OrderedDict()

	def init_form(self): return "new ControlCombo('{0}', {1})".format( self._name, simplejson.dumps(self.serialize()) )

	def currentIndexChanged(self, index):
		if not self._addingItem:
			if len(item)>=1: 
				OTControlBase.value.fset(self, self._items[str(item)])
			
	def add_item(self, label, value = None):
		if self._items==None: self._items=collections.OrderedDict()
		self._addingItem = True
		
		firstValue = False
		if len(self._items)==0: firstValue = True

		if value==None:
			self._items[label] = label
		else:
			self._items[label] = value
		self._addingItem = False

		if firstValue: self.value = self._items[label]

		self.mark_to_update_client()

	def __add__(self, val):
		if isinstance( val, tuple ):
			self.add_item(val[0], val[1])
		else:
			self.add_item(val)
		
		return self


	def clearItems(self):
		self._items = collections.OrderedDict()
		self._value = None

		self.mark_to_update_client()

	@property
	def items(self): return self._items.values()

	@property
	def values(self): return self._items.items()

	@property
	def value(self): return self._value

	@value.setter
	def value(self, value):
		for key, val in self._items.items():
			self.mark_to_update_client()
			if str(value) == str(val):
				if str(self._value)!=str(value): self.changed_event()
				self._value = val

	@property
	def text(self): return ""

	@text.setter
	def text(self, value):
		for key, val in self._items.items():
			self.mark_to_update_client()
			if value == key:
				self.value = val
				break
	

	def serialize(self):
		data = ControlBase.serialize(self)
		items = []
		for key, value in self._items.items():
			items.append({'label': key, 'value': value }) 
		data.update({ 'items': items, 'value': self._value })
		return data
		

