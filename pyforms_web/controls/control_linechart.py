import datetime
from pyforms_web.controls.control_base import ControlBase
import simplejson

class ControlLineChart(ControlBase):

    def __init__(self, *args, **kwargs):
        self._legend = []
        self.selected_data = None
        self.selected_serie = None
        self.height = kwargs.get('height', 400)
        self.width = kwargs.get('width', None)
        self.legend_location = kwargs.get('legend_location', 'e')
        self.legend_placement = kwargs.get('legend_placement', 'outside')
        
        super().__init__(*args, **kwargs)

        self.data_selected_event = kwargs.get('data_selected_event', self.data_selected_event)

    def init_form(self): return "new ControlLineChart('{0}', {1})".format( self._name, simplejson.dumps(self.serialize()) )

    def remote_data_selected_event(self):
        self.data_selected_event(self.selected_serie, self.selected_data)

    def data_selected_event(self, series_index, data):
        pass

    def serialize(self):
        data = ControlBase.serialize(self)
        
        legend, series = [], []
        value = self._value if isinstance(self._value, dict) else {}

        for title, serie in value.items():
            legend.append(title)
            series.append(serie)

        data.update({ 
            'legend': legend,
            'legend_location': self.legend_location,
            'legend_placement': self.legend_placement,
            'value':  series,
            'height': self.height,
            'width': self.width
        })

        return data

    """
    def deserialize(self, properties):
        self.selected_serie  = properties.get('selected_series', None)
        self.selected_data   = properties.get('selected_data', None)
        
        ControlBase.deserialize(self, properties)
        self.legend = properties[u'legend']
        self.value  = properties[u'value']
    """

        