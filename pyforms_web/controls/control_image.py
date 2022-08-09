from pyforms_web.controls.control_base import ControlBase

try:
    import cv2
except:
    print('no cv2 installed')
import base64
import numpy as np
from io import StringIO
from PIL import Image
import simplejson


class ControlImage(ControlBase):

    def __init__(self, *args, **kwargs):
        self._filename = None
        super(ControlImage, self).__init__(*args, **kwargs)

    def init_form(self):
        return "new ControlImage('{0}', {1})".format(self._name, simplejson.dumps(self.serialize()))

    def save(self, data):
        if self.value != None: data['value'] = self._value

    def load(self, data):
        if 'value' in data: self.value = data['value']

    def repaint(self):
        pass

    def set_url(self, url):
        if self._value != url:
            self.mark_to_update_client()
            self.changed_event()
        self._value = url

    @property
    def value(self):
        return ControlBase.value.fget(self)

    @value.setter
    def value(self, value):
        if self._value != value:
            self.mark_to_update_client()
            self.changed_event()

        if len(value) == 0:
            self._value = ''
        elif isinstance(value, np.ndarray):
            self._value = value
        elif isinstance(value, str) and value.startswith('http'):
            self._value = value
        elif isinstance(value, str):
            self._value = cv2.imread(value)

    def serialize(self):
        data = ControlBase.serialize(self)
        image = self.value
        if isinstance(image, np.ndarray):
            if len(image.shape) > 2: image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            buff = StringIO.StringIO()
            image.save(buff, format="PNG")
            content = buff.getvalue()
            buff.close()
            data.update({'value': {
                'base64': base64.b64encode(content)
            }})
        else:
            data.update({'value': {
                'url': self._value
            }})
        return data
