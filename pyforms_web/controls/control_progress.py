from pyforms_web.controls.control_base import ControlBase
import simplejson

class ControlProgress(ControlBase):

    _min = 0
    _max = 100

    def __init__(self, *args, **kwargs):
        self._updateSlider = True
        self._min = kwargs.get('min', 0)
        self._max = kwargs.get('max', 100)
        ControlBase.__init__(self, *args, **kwargs)
                
    def init_form(self): return "new ControlProgress('{0}', {1})".format( self._name, simplejson.dumps(self.serialize()) )




    @property
    def min(self): return self._min
    @min.setter
    def min(self, value): 
        if self._min!=value: self.mark_to_update_client()
        self._min = value

    @property
    def max(self): return self._max
    @max.setter
    def max(self, value): 
        if self._max!=value: self.mark_to_update_client()
        self._max = value
        