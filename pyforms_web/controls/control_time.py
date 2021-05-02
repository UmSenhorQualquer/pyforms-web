import datetime
from datetime import date, time
from pyforms_web.controls.control_base import ControlBase
import simplejson
from django.db.models.fields import NOT_PROVIDED

from django.utils.dateparse import parse_datetime
from django.utils import timezone

class ControlTime(ControlBase):

    def init_form(self): return "new ControlTime('{0}', {1})".format( self._name, simplejson.dumps(self.serialize()) )

    @property
    def value(self):
        return ControlBase.value.fget(self)

    @value.setter
    def value(self, value):
        if value and isinstance(value, str):
            value = int(value)
        if value and isinstance(value, time):
            value = value.hour*60+value.minute
        ControlBase.value.fset(self, value)


    def serialize(self):
        data = ControlBase.serialize(self)

        if self.value:
            if isinstance(self.value, time):
                data.update({'value': self.value.hour*60+self.value.minute})
        return data