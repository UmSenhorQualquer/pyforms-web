import datetime
from pyforms_web.web.Controls.ControlBase import ControlBase

class ControlWorkflow(ControlBase):

	def initControl(self): return "new ControlWorkflow('{0}', {1})".format( self._name, str(self.serialize()) )


	@property
	def operator_selected_evt(self):
		return self._operator_selected_evt

	@operator_selected_evt.setter
	def operator_selected_evt(self, value):
		self._operator_selected_evt = value


	def serialize(self):
		res = super(ControlWorkflow, self).serialize()

		res.update({'operator_selected_evt': 1 if hasattr(self, 'operator_selected_evt') else 0})
		return res

	def deserialize(self, properties):
		super(ControlWorkflow, self).deserialize(properties)
		if 'selected_operator' in properties:
			self._selected_operator = properties['selected_operator']


	