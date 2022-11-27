import base64
import simplejson
from django.template.loader import render_to_string

from pyforms_web.controls.control_base import ControlBase


class ControlTemplate(ControlBase):

    def __init__(self, *args, **kwargs):
        super(ControlTemplate, self).__init__(*args, **kwargs)
        self._template = kwargs.get('template', None)
        # Action triggered from the template html
        self.action_param = None
        # Data received from the template html
        self.submit_action_data = None

    def init_form(self):
        return """new ControlTemplate('{0}', {1})""".format(
            self._name,
            simplejson.dumps(self.serialize())
        )

    def serialize(self):
        data = super().serialize()

        if self._template is not None:
            try:
                html = render_to_string(self._template, self.value)
            except Exception as e:
                html = str(e)
        else:
            html = 'No template was defined'

        html = base64.b64encode(html.encode('utf-8'))

        data.update({'value': html})
        return data

    def deserialize(self, properties):
        self._label = properties.get('label', '')
        self._help = properties.get('help', '')
        self._visible = properties.get('visible', True)
        self.action_param = properties.get('action_param', None)
        self.submit_action_data = properties.get('submit_action_data', None)

    @property
    def template(self):
        return self._template

    @template.setter
    def template(self, value):
        self._template = value
