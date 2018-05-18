from pyforms_web.controls.control_base import ControlBase
import simplejson

class ControlInteger(ControlBase):

    def init_form(self):

        return """new ControlInteger('{0}', {1})""".format(
            self._name, 
            simplejson.dumps(self.serialize()) 
        )

    @property
    def value(self): return ControlBase.value.fget(self)

    @value.setter
    def value(self, value):
        try:
            if value is not None:
                try:
                    value = int(value)
                except:
                    raise Exception('The value is not a number')

            ControlBase.value.fset(self, value)
            self.error = False
        except Exception as e:
            self.error = True
            self.mark_to_update_client()
            raise e
        

    def clean_field(self):
        if isinstance(value, str): 
            raise Exception('The field {0} should be of type integer')