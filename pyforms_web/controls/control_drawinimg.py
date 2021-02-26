from pyforms_web.controls.control_base import ControlBase
import simplejson

class ControlDrawInImg(ControlBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._circles = kwargs.get('circles', [])

    def init_form(self):
        return """new ControlDrawInImg('{0}', {1})""".format(
            self._name, 
            simplejson.dumps(self.serialize()) 
        )

    def add_circle(self, x, y, radius):
        self._circles.append( (x, y, radius) )
        self.mark_to_update_client()

    def serialize(self):
        res = super().serialize()
        if self.value is None: 
            res.update({'value':''})
        else:
            res.update({'value':str(self.value)})

        res.update({
            'circles': self._circles
        })
        return res