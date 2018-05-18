from pyforms_web.controls.control_base import ControlBase
import simplejson

class ControlBreadcrumb(ControlBase):

    def __init__(self, *args, **kwargs):
        super(ControlBreadcrumb, self).__init__(*args, **kwargs)
        self.action_param = None

    def init_form(self): 
        return "new ControlBreadcrumb('{0}', {1})".format( 
            self._name, simplejson.dumps(self.serialize()) 
        )

    def pressed(self): 
        """
        This event is called when the button is pressed.
        The correspondent js event is defined in the framework.js file
        """
        if self.action_param is not None:
            self.value[self.action_param][1]()


    def serialize(self):
        data  = super(ControlBreadcrumb,self).serialize()
        value = []
        for i, (label, action) in enumerate(self.value):

            v = {'label': label}
            
            if callable(action): 
                v['action_param'] = i
            else:
                v['link'] = action

            value.append(v)

        data.update({'value':value, 'action_param': None})
        return data

    def deserialize(self, properties):
        self.action_param = properties.get('action_param', None)

        
    