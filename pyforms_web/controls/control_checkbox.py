from pyforms_web.controls.control_base import ControlBase
import simplejson

class ControlCheckBox(ControlBase):

    def __init__(self, *args, **kwargs):
        if 'default' not in kwargs: kwargs['default']=False
        self.checkbox_type = kwargs.get('checkbox_type', 'toggle')

        super().__init__(*args, **kwargs)
    

    def init_form(self):
        return "new ControlCheckBox('{0}', {1})".format( self._name, simplejson.dumps(self.serialize()) )

    def serialize(self):
        res = super().serialize()
        res['checkbox_type'] = self.checkbox_type
        return res
