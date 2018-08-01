from pyforms_web.controls.control_base import ControlBase
import simplejson

class ControlCheckBox(ControlBase):

    def __init__(self, *args, **kwargs):
        if 'default' not in kwargs: kwargs['default']=False
        super().__init__(*args, **kwargs)
    

    def init_form(self): return "new ControlCheckBox('{0}', {1})".format( self._name, simplejson.dumps(self.serialize()) )

