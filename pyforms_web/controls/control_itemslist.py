from pyforms_web.controls.control_base import ControlBase
import simplejson

class ControlItemsList(ControlBase):

	def __init__(self, *args, **kwargs):
		self._read_only         = False
		self._selected_index    = -1
		self.item_selection_changed_event = None
		self.select_btn_label 	= 'More <i class="right chevron icon"></i>'
		super(ControlItemsList, self).__init__(*args, **kwargs)


	def init_form(self): return "new ControlItemsList('{0}', {1})".format( self._name, simplejson.dumps(self.serialize()) )

	def dbl_click(self): pass



	@property
	def readonly(self): return self._read_only

	@readonly.setter
	def readonly(self, value):
		self.mark_to_update_client()
		self._read_only = value

	@property
	def selected_row_index(self): return self._selected_index

	@selected_row_index.setter
	def selected_row_index(self, value):
		self.mark_to_update_client()
		self._selected_index = value

	@property
	def value(self): return ControlBase.value.fget(self)

	@value.setter
	def value(self, value):
		self._selected_index = -1
		ControlBase.value.fset(self, value)

	def serialize(self):
		data    = ControlBase.serialize(self)

		data.update({
			'read_only':            1 if self._read_only else 0,
			'selected_index':       self._selected_index
		})

		if self.item_selection_changed_event:
			data.update({
				'select_btn_label':self.select_btn_label,
			})
		return data

	def deserialize(self, properties):
		ControlBase.deserialize(self,properties)

		self._read_only         = properties['read_only']==1
		self._selected_index    = int(properties['selected_index'])
		