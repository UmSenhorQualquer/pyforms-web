import datetime
from pyforms_web.controls.control_base import ControlBase
import simplejson

class ControlBarsChart(ControlBase):

    def __init__(self, *args, **kwargs):
        self._legend = []
        self.selected_data = None
        self.selected_serie = None
        
        super().__init__(*args, **kwargs)

        self.data_selected_event = kwargs.get('data_selected_event', self.data_selected_event)

    def init_form(self): return "new ControlBarsChart('{0}', {1})".format( self._name, simplejson.dumps(self.serialize()) )

    def remote_data_selected_event(self):
        self.data_selected_event(self.selected_serie, self.selected_data)

    def data_selected_event(self, series_index, data):
        pass

    """
    @property
    def value(self):
        rows = []
        for title, serie in self._value.items():
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
    def value(self, value):
        ControlBase.value.fset(self, value)
    """

    def serialize(self):
        data = ControlBase.serialize(self)
        
        legend, series = [], []
        value = self._value if isinstance(self._value, dict) else {}

        for title, serie in value.items():
            legend.append(title)
            series.append(serie)


        data.update({ 
            'legend': legend, 
            'value':  series 
        })

        return data


    def deserialize(self, properties):
        self.selected_serie  = properties.get('selected_series', None)
        self.selected_data   = properties.get('selected_data', None)
        
        ControlBase.deserialize(self, properties)
        self.legend = properties[u'legend']
        self.value  = properties[u'value']

        