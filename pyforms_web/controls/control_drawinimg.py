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

    def add_circle(self, x, y, radius, text=None):
        self._circles.append( [x, y, radius, text] )
        self.mark_to_update_client()

    def update_circle(self, index, x=None, y=None, radius=None, text=None):
        if x is not None:       self._circles[index][0] = x
        if y is not None:       self._circles[index][1] = y
        if radius is not None:  self._circles[index][2] = radius
        if text is not None:    self._circles[index][3] = text
        self.mark_to_update_client()

    def clear(self):
        self._circles = []
        self.mark_to_update_client()

    @property
    def circles(self):
        return self._circles

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

    def deserialize(self, properties):
        super().deserialize(properties)

        self._circles = properties.get('circles', [])