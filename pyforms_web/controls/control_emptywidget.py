from pyforms_web.controls.control_base import ControlBase
from pyforms_web.basewidget import BaseWidget
import base64, dill
import simplejson
from pyforms_web.web.middleware import PyFormsMiddleware

class ControlEmptyWidget(ControlBase):

    def __init__(self, *args, **kwargs):
        super(ControlEmptyWidget,self).__init__(*args, **kwargs)
        self._parent = kwargs.get('parent', None)
        self._name = kwargs.get('name', None)

    def init_form(self):
        return """new ControlEmptyWidget('{0}', {1})""".format(
            self._name, 
            simplejson.dumps(self.serialize())
        )

    def serialize(self):
        data = ControlBase.serialize(self)
        if isinstance(self.value, BaseWidget):
            data.update({'value':self.value.uid})
            self.value.parent = self.parent.uid 
        else:
            data.update({'value':None})

        return data

    def deserialize(self, properties):
        #self._label   = properties.get('label','')
        #self._help    = properties.get('help','')
        #self._visible = properties.get('visible',True)

        if isinstance(self.value, BaseWidget):
            self.value = PyFormsMiddleware.get_instance(self.value.uid)
            if self.value is not None: self.value.parent = self.parent
        else:
            self.value = None
        


    def mark_to_update_client(self):
         self._update_client = True
         request = PyFormsMiddleware.get_request()
         if self.parent is not None and request is not None and hasattr(request,'updated_apps'):
            request.updated_apps.add_top(self.parent)

    @property
    def value(self): return ControlBase.value.fget(self)

    @value.setter
    def value(self, value):
        ControlBase.value.fset(self, value)
        if value: 
            value.LAYOUT_POSITION = self.place_id
            