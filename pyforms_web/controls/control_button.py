from pyforms_web.controls.control_base import ControlBase
import simplejson

class ControlButton(ControlBase):

    def __init__(self, *args, **kwargs):
        if 'css' not in kwargs: kwargs['css']='blue'
        self._labeled = kwargs.get('labeled', False)
        super(ControlButton, self).__init__(*args, **kwargs)
        
    def init_form(self): return "new ControlButton('{0}', {1})".format( self._name, simplejson.dumps(self.serialize()) )

    def pressed(self): 
        """
        This event is called when the button is pressed.
        The correspondent js event is defined in the framework.js file
        """
        if not isinstance(self._value, str) and self._value: self._value()

    def serialize(self):
        res = super(ControlButton, self).serialize()
        res.update({
            'value': self.value if (isinstance(self.value, str) and len(self.value)>0) else None,
            'labeled': self._labeled
        })
        return res

    def deserialize(self, properties):
        self._label   = properties.get('label','')
        self._help    = properties.get('help','')
        if properties.get('value',None):
            self.value = properties.get('value',None)
        self._visible = properties.get('visible',True)


   