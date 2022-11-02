from pyforms_web.controls.control_base import ControlBase
import simplejson

class ControlCodeMirror(ControlBase):

    def __init__(self, *args, **kwargs):
        """
        :param function on_enter_event: Event called when the Enter key is pressed.
        """
        super().__init__(*args, **kwargs)
        self.height = kwargs.get('height', None)
        self.width = kwargs.get('width', None)

    def init_form(self):
        return """new ControlCodeMirror('{0}', {1})""".format(
            self._name, 
            simplejson.dumps(self.serialize()) 
        )

    def serialize(self):
        data = super().serialize()
        data.update({
            'height':  self.height,
            'width': self.width
        })
        return data