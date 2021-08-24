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
		self.streaming_func = None
		self.start_streaming = False
		self.abort_streaming = False

	def init_form(self):
		return """new ControlTextArea('{0}', {1})""".format(
			self._name, 
			simplejson.dumps(self.serialize()) 
		)

	def serialize(self):
		res = super().serialize()
		res.update({
			'rows':self.rows,
			'cols':self.cols,
			'start_streaming': self.start_streaming,
			'abort_streaming': self.abort_streaming
		})
		self.start_streaming = False
		self.abort_streaming = False
		return res

	def stream(self, func):
		self.streaming_func = func
		self.start_streaming = True
		self.abort_streaming = True
		self.mark_to_update_client()