from datetime import date
from pyforms_web.controls.control_base import ControlBase
import simplejson

class ControlCalendar(ControlBase):
    
    def __init__(self, *args, **kwargs):
        super(ControlCalendar, self).__init__(*args, **kwargs)

        today = date.today()
        self.month = today.month 
        self.year  = today.year
        
    def init_form(self): return "new ControlCalendar('{0}', {1})".format( self._name, simplejson.dumps(self.serialize()) )
    
    def serialize(self):
        data = super(ControlCalendar, self).serialize()
        data.update({ 'month': self.month, 'year': self.year })
        return data

    @property
    def month(self): return self._month
    @month.setter 
    def month(self, value):
        self.mark_to_update_client()
        self._month = value
    
    @property
    def year(self): return self._year
    @year.setter 
    def year(self, value):
        self.mark_to_update_client()
        self._year = value

