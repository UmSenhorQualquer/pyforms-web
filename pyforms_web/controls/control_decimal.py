from pyforms_web.controls.control_base import ControlBase
import simplejson, decimal

class ControlDecimal(ControlBase):

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
		str_val = properties.get('value', None)
		self.value = decimal.Decimal(str_val) if str_val else None
