from .control_text import ControlText
import simplejson

class ControlTextArea(ControlText):

	def __init__(self, *args, **kwargs):
		"""
        :param function on_enter_event: Event called when the Enter key is pressed.
        """
		super().__init__(*args, **kwargs)
		self.rows = kwargs.get('rows', 8)
		self.cols = kwargs.get('cols', None)

	def init_form(self):
		return """new ControlTextArea('{0}', {1})""".format(
			self._name, 
			simplejson.dumps(self.serialize()) 
		)

	def serialize(self):
		res = super().serialize()
		res.update({'rows':self.rows, 'cols':self.cols})
		return res