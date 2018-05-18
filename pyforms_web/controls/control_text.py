from pyforms_web.controls.control_base import ControlBase
import simplejson

class ControlText(ControlBase):

    def init_form(self):
        return """new ControlText('{0}', {1})""".format(
            self._name, 
            simplejson.dumps(self.serialize()) 
        )


    def serialize(self):
        res = super(ControlText, self).serialize()
        if self.value is None: 
            res.update({'value':''})
        else:
            res.update({'value':str(self.value)})
        return res

    def deserialize(self, properties):
        super(ControlText, self).deserialize(properties)
        val = properties.get('value',None)
        if val=='': self._value = None