import datetime

from pyforms_web.basewidget import custom_json_converter
from pyforms_web.controls.control_base import ControlBase
import simplejson

class ControlLineChart(ControlBase):

    def __init__(self, *args, **kwargs):
        self._legend = []
        self.selected_data = None
        self.selected_serie = None
        self.height = kwargs.get('height', None)
        self.width = kwargs.get('width', None)
        self.legend_location = kwargs.get('legend_location', 'e')
        self.legend_placement = kwargs.get('legend_placement', 'outside')
        self.x_axis_format = kwargs.get('x_axis_format', None)
        self.x_axis_type = kwargs.get('x_axis_type', 'datetime')
        self.smooth = kwargs.get('smooth', True)
        self.show_marker = kwargs.get('show_marker', True)

        self._xaxis_range = kwargs.get('xaxis_range', None)

        super().__init__(*args, **kwargs)

        self.data_selected_event = kwargs.get('data_selected_event', self.data_selected_event)

    def init_form(self): return "new ControlLineChart('{0}', {1})".format( self._name, simplejson.dumps(self.serialize(), default=custom_json_converter) )

    def remote_data_selected_event(self):
        self.data_selected_event(self.selected_serie, self.selected_data)

    def data_selected_event(self, series_index, data):
        pass

    @property
    def xaxis_range(self): return self._xaxis_range

    @xaxis_range.setter
    def xaxis_range(self, value): self._xaxis_range = value

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
            'width': self.width,
            'x_axis_format': self.x_axis_format,
            'x_axis_type': self.x_axis_type,
            'smooth': self.smooth,
            'show_marker': self.show_marker,
            'xaxis_range': self.xaxis_range,
        })

        return data

    def deserialize(self, properties):
        pass