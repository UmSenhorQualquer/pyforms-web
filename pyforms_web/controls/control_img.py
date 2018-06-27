from pyforms_web.controls.control_base import ControlBase
import simplejson

class ControlImg(ControlBase):

    def init_form(self):
        return """new ControlImg('{0}', {1})""".format(
            self._name, 
            simplejson.dumps(self.serialize()) 
        )


    def serialize(self):
        res = super(ControlImg, self).serialize()
        if self.value is None: 
            res.update({'value':''})
        else:
            res.update({'value':str(self.value)})
        return res