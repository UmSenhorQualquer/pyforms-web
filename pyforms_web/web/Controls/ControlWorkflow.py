import datetime
from pyforms_web.web.Controls.ControlBase import ControlBase

class ControlWorkflow(ControlBase):

	def initControl(self): return "new ControlWorkflow('{0}', {1})".format( self._name, str(self.serialize()) )

	@property
	def selected_operator(self):
		if not hasattr(self, '_selected_operator'): return None
		return self._selected_operator
	@selected_operator.setter
	def selected_operator(self, value):
		if not hasattr(self, '_selected_operator'): return
		self._selected_operator = value

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

	def deleteSelected(self): self._delete_selected = True



	def serialize(self):
		res = super(ControlWorkflow, self).serialize()

		if self.selected_operator: res.update({'selected_operator': self.selected_operator})
		if hasattr(self, '_delete_selected'):
			res.update({'deleteSelected': self._delete_selected})
			del self._delete_selected
		
		res.update({'operator_selected_evt': 1 if hasattr(self, 'operator_selected_evt') else 0})
		res.update({'operator_unselected_evt': 1 if hasattr(self, 'operator_unselected_evt') else 0})
		return res

	def deserialize(self, properties):
		super(ControlWorkflow, self).deserialize(properties)
		if 'selected_operator' in properties: self._selected_operator = properties['selected_operator']


	