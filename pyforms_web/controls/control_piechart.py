import datetime
from pyforms_web.controls.control_base import ControlBase
import simplejson

class ControlPieChart(ControlBase):

    def __init__(self, *args, **kwargs):
        super(ControlPieChart, self).__init__(*args, **kwargs)

        self.legend_location = kwargs.get('legend_location', 'e')
        self.legend_placement = kwargs.get('legend_placement', 'outside')

    def init_form(self): return "new ControlPieChart('{0}', {1})".format( self._name, simplejson.dumps(self.serialize()) )

    def deserialize(self, properties):
        ControlBase.deserialize(self, properties)
        self.legend = properties[u'legend']
        self.value  = properties[u'value']

    def serialize(self):
        data = ControlBase.serialize(self)

        data.update({
            'legend_location': self.legend_location,
            'legend_placement': self.legend_placement,
        })

        return data
        