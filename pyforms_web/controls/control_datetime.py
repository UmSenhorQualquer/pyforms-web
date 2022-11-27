import datetime

from pyforms_web.basewidget import custom_json_converter
from pyforms_web.controls.control_base import ControlBase
import simplejson

from django.utils.dateparse import parse_datetime
from django.utils import timezone

class ControlDateTime(ControlBase):


    def init_form(self): return "new ControlDateTime('{0}', {1})".format( self._name, simplejson.dumps(self.serialize(), default=custom_json_converter) )

    @property
    def value(self): return ControlBase.value.fget(self)

    @value.setter
    def value(self, value):

        # covers usage like `DateTimeField(default=timezone.now)`
        value = value() if callable(value) else value

        try:
            if isinstance(value, str) and len(value.strip())==0:
                value = None

            if value is not None and not isinstance(value, datetime.date):
                try:
                    value = parse_datetime(value)
                    value = timezone.localtime(value)
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

        if self.value:
            data.update({'value': self.value.isoformat() })
        return data
