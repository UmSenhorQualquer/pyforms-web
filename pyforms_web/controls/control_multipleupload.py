import os

import simplejson
from django.conf import settings

from pyforms_web.controls.control_base import ControlBase


class ControlMultipleUpload(ControlBase):

    def init_form(self):
        return "new ControlMultipleUpload('{0}', {1})".format(self._name, simplejson.dumps(self.serialize()))

    @property
    def filepaths(self):
        for filename in self.value:
            yield os.path.join(settings.MEDIA_ROOT, filename[len(settings.MEDIA_URL):])

    def serialize(self):
        data = super().serialize()
        if self.value:

            files = []
            for filename in self.value:
                filepath = os.path.join(settings.MEDIA_ROOT, filename[len(settings.MEDIA_URL):])
                files.append({
                    'name': os.path.basename(filename),
                    'size': os.path.getsize(filepath),
                    'file': filename,
                    'url': filename
                })
            data.update({'file_data': files})

        return data
