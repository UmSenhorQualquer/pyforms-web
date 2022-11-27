import datetime
from pyforms_web.controls.control_base import ControlBase
import simplejson

class ControlVisVis(ControlBase):

    def __init__(self, *args, **kwargs):
        self._legend = []
        self.selected_data = None
        self.selected_serie = None
        
        if 'default' not in kwargs.keys():
            kwargs['default']=[]
        
        super().__init__(*args, **kwargs)

        self.data_selected_event = kwargs.get('data_selected_event', self.data_selected_event)

    def init_form(self): return "new ControlVisVis('{0}', {1})".format( self._name, simplejson.dumps(self.serialize()) )

    def remote_data_selected_event(self):
        self.data_selected_event(self.selected_serie, self.selected_data)

    def data_selected_event(self, series_index, data):
        pass


    @property
    def legend(self):return self._legend
    @legend.setter
    def legend(self, value):
        if self._legend!=value: self.mark_to_update_client()
        self._legend = value


    @property
    def value(self):
        rows = []
        for row in self._value:
            new_row = []
            for value in row:
                if value is None: break
                if isinstance(value[0], datetime.datetime): value[0] = str(value[0])
                if isinstance(value[0], datetime.date): value[0] = str(value[0])
                if isinstance(value[0], str): value[0] = str(value[0])
                if isinstance(value[1], str): value[1] = str(value[1])
                new_row.append(value)
            rows.append(new_row)
        return rows

    @value.setter
    def value(self, value): ControlBase.value.fset(self, value)


    def serialize(self):
        data  = ControlBase.serialize(self)
        data.update({ 
            'legend':   self.legend, 
            'value':    self._value 
        })
        return data


    def deserialize(self, properties):
        self.selected_serie  = properties.get('selected_series', None)
        self.selected_data   = properties.get('selected_data', None)
        
        ControlBase.deserialize(self, properties)
        self.legend = properties[u'legend']
        self.value  = properties[u'value']

        