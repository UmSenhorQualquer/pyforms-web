from pyforms_web.web.Controls.ControlBase import ControlBase
import simplejson

class ControlItemList(ControlBase):
    def __init__(self, label="", defaultValue="", helptext=''):
        self._hname = ''
        self._specs = []
        self._options = []
        super(ControlItemList, self).__init__(label, defaultValue, helptext)

    def init_form(self):
        return """new ControlItemList('{0}', {1})""".format(
            self._name,
            simplejson.dumps(self.serialize())
        )

    @property
    def hname(self):
        return str(self._hname)

    @hname.setter
    def hname(self, value):
        self._hname = value

    @property
    def specs(self):
        return map(str, self._specs)

    @specs.setter
    def specs(self, value):
        self._specs = value

    @property
    def options(self):
        return map(str, self._options)

    @options.setter
    def options(self, value):
        self._options = value

    def serialize(self):
        data = ControlBase.serialize(self)
        data.update({'hname': self.hname})
        data.update({'specs': self.specs})
        data.update({'options': self.optios})
        data.update({'name': str(self.value)})
        return data

    def deserialize(self, properties):
        ControlBase.deserialize(self, properties)
        self.css = properties[u'css']
        self.hname = properties['hname']
        self.specs = properties['specs']
        self.options = properties['options']
