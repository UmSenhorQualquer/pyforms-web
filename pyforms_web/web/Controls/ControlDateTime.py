import datetime
from pyforms_web.web.controls.ControlBase import ControlBase
import simplejson

from dateutil.parser import parse as date_parser

class ControlDateTime(ControlBase):

    PYTHON_FORMAT = "%Y-%m-%d %H:%M"
    JS_FORMAT = "Y-m-d"

    def init_form(self): return "new ControlDateTime('{0}', {1})".format( self._name, simplejson.dumps(self.serialize()) )

    @property
    def value(self): return ControlBase.value.fget(self)

    @value.setter
    def value(self, value):
        try:
            if isinstance(value, str) and len(value.strip())==0:
                value = None

            if value is not None and not isinstance(value, datetime.date):
                try:
                    value = date_parser(value)
                except:
                    raise Exception('The value is not a valid date time')

            ControlBase.value.fset(self, value)
            self.error = False
        except Exception as e:
            self.error = True
            self.mark_to_update_client()
            raise e

    def serialize(self):
        data = ControlBase.serialize(self)
        data.update({'format':self.JS_FORMAT})
        if self.value:
            data.update({'value': self.value.strftime(self.PYTHON_FORMAT) })
        return data
