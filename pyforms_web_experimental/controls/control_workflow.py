import datetime
from pyforms_web.controls.control_base import ControlBase
import simplejson

class ControlWorkflow(ControlBase):

	def init_form(self): return "new ControlWorkflow('{0}', {1})".format( self._name, simplejson.dumps(self.serialize()) )

	@property
	def selected_operator(self):
		if not hasattr(self, '_selected_operator'): return None
		return self._selected_operator
	@selected_operator.setter
	def selected_operator(self, value):
		if not hasattr(self, '_selected_operator'): return
		if self._selected_operator!=value: self.mark_to_update_client()
		
		self._selected_operator = value

	@property
	def selected_link(self):
		if not hasattr(self, '_selected_link'): return None
		return self._selected_link
	@selected_link.setter
	def selected_link(self, value):
		if not hasattr(self, '_selected_link'): return
		if self._selected_link!=value: self.mark_to_update_client()
		
		self._selected_link = value



	@property
	def operator_selected_evt(self):
		return self._operator_selected_evt

	@operator_selected_evt.setter
	def operator_selected_evt(self, value):
		self._operator_selected_evt = value

	@property
	def operator_unselected_evt(self):
		return self._operator_unselected_evt

	@operator_unselected_evt.setter
	def operator_unselected_evt(self, value):
		self._operator_unselected_evt = value



	@property
	def link_selected_evt(self): return self._link_selected_evt
	@link_selected_evt.setter
	def link_selected_evt(self, value): self._link_selected_evt = value

	@property
	def link_unselected_evt(self): return self._link_unselected_evt
	@link_unselected_evt.setter
	def link_unselected_evt(self, value): self._link_unselected_evt = value




	def deleteSelected(self): self._delete_selected = True



	def serialize(self):
		res = super(ControlWorkflow, self).serialize()

		if self.selected_operator: 	res.update({'selected_operator': self.selected_operator})
		if self.selected_link: 		res.update({'selected_link': self.selected_link})
		if hasattr(self, '_delete_selected'):
			res.update({'deleteSelected': self._delete_selected})
			del self._delete_selected
		
		res.update({'operator_selected_evt': 1 if hasattr(self, 'operator_selected_evt') else 0})
		res.update({'operator_unselected_evt': 1 if hasattr(self, 'operator_unselected_evt') else 0})
		
		res.update({'link_selected_evt': 1 if hasattr(self, 'link_selected_evt') else 0})
		res.update({'link_unselected_evt': 1 if hasattr(self, 'link_unselected_evt') else 0})
		
		return res

	def deserialize(self, properties):
		super(ControlWorkflow, self).deserialize(properties)
		if 'selected_operator' in properties: 	self._selected_operator = properties['selected_operator']
		if 'selected_link' in properties: 		self._selected_link = properties['selected_link']


	