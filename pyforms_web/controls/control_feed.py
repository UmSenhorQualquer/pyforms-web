from pyforms_web.controls.control_base import ControlBase
import simplejson

class ControlFeed(ControlBase):

	def __init__(self, *args, **kwargs):
		self._read_only         = False
		self.has_more		    = False
		self._selected_index    = -1
		self.item_selection_changed_event = None
		self.mode = kwargs.get('mode','feed')
		
		super(ControlFeed, self).__init__(*args, **kwargs)
		self._value = []
		self.action_param = None
		self._clear   = False
		

	def init_form(self): return "new ControlFeed('{0}', {1})".format( self._name, simplejson.dumps(self.serialize()) )

	def clear(self):
		self._clear = True
		self._value = []
		self.mark_to_update_client()

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
	def value(self): return ControlBase.value.fget(self)

	@value.setter
	def value(self, value):
		self._selected_index = -1
		ControlBase.value.fset(self, value)


	def serialize(self):
		res = ControlBase.serialize(self)
		res.update({'clear':self._clear, 'has_more': self.has_more, 'mode': self.mode})
		self._clear = False
		self.value = []
		return res
	

	def deserialize(self, properties):
		ControlBase.deserialize(self,properties)
		self._value			= []
		self.action_param 	= properties.get('action_param', None)
		