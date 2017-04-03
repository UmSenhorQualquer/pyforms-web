from pyforms_web.web.Controls.ControlBase import ControlBase
import simplejson

class ControlFeed(ControlBase):

	def __init__(self, label = "", defaultValue = "", helptext=''):
		self._read_only         = False
		self._selected_index    = -1
		self.item_selection_changed_event = None
		
		super(ControlFeed, self).__init__(label, defaultValue, helptext)
		self._value 	= []
		self._actions 	= None

	def init_form(self): return "new ControlFeed('{0}', {1})".format( self._name, simplejson.dumps(self.serialize()) )

	@property
	def selected_row_index(self): return self._selected_index

	@selected_row_index.setter
	def selected_row_index(self, value):
		self.mark_to_update_client()
		self._selected_index = value

	def insert_feed(self, pk, html):
		self.mark_to_update_client()
		data = self.value
		data.append({
			'pk':pk,
			'html':html
		})
		self.value = data

	@property
	def actions(self): return self._actions
	@actions.setter
	def actions(self, value): self._actions = value
	

	@property
	def value(self): return ControlBase.value.fget(self)

	@value.setter
	def value(self, value):
		self._selected_index = -1
		ControlBase.value.fset(self, value)


	def serialize(self):
		data    = ControlBase.serialize(self)

		if self._actions: data.update({'actions':self._actions})


		data.update({
			'read_only':            1 if self._read_only else 0,
			'selected_index':       self._selected_index
		})

		
		return data

	def deserialize(self, properties):
		ControlBase.deserialize(self,properties)

		self._read_only         = properties['read_only']==1
		self._selected_index    = int(properties['selected_index'])
		self._value 			= []
		