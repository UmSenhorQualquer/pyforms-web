from pyforms_web.controls.control_base import ControlBase
import simplejson

class ControlSlider(ControlBase):

    def __init__(self, *args, **kwargs):
        self._updateSlider = True
        self._min   = kwargs.get('min', 0)
        self._max   = kwargs.get('max', 100)
        if kwargs.get('default', None)==None:
            kwargs['default']=0
        super(ControlSlider,self).__init__(*args, **kwargs)
        
    def init_form(self): return "new ControlSlider('{0}', {1})".format( self._name, simplejson.dumps(self.serialize()) )


    @property
    def min(self): return self._min

    @min.setter
    def min(self, value):
        if self._min!=value:
            self.mark_to_update_client()
            self._min = value

    @property
    def max(self):  return  self._max

    @max.setter
    def max(self, value):
        if self._max!=value:
            self.mark_to_update_client()
            self._max = value

    def deserialize(self, properties):
        self.value    = int(properties.get('value',None))
        self._label   = properties.get('label','')
        self._help    = properties.get('help','')
        self._visible = properties.get('visible',True)

    def serialize(self):
        data = super(ControlSlider,self).serialize()
        data.update({ 'max': self.max, 'min': self.min, 'value': self._value })
        return data