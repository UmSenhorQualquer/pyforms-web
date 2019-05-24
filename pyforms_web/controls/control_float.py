from pyforms_web.controls.control_base import ControlBase
import simplejson
from decimal import Decimal

class ControlFloat(ControlBase):

	def init_form(self):
		return """new ControlFloat('{0}', {1})""".format(
			self._name, 
			simplejson.dumps(self.serialize()) 
		)


	def deserialize(self, properties):
		"""
        Serialize the control data.

        :param dict properties: Serialized data to load.
        """
		super().deserialize(properties)

		self.value = float(
			properties.get('value', None)
		)