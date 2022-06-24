import os
import shutil

import simplejson
from django.conf import settings

from pyforms_web.controls.control_base import ControlBase


class ControlMultipleUpload(ControlBase):

    def init_form(self):
        return "new ControlMultipleUpload('{0}', {1})".format(self._name, simplejson.dumps(self.serialize()))

    def filepaths(self):
        for filename in self.value:
            yield os.path.join(settings.MEDIA_ROOT, filename[len(settings.MEDIA_URL):])

    def move_to(self, dest_dirpath):
        dest_path = os.path.join(settings.MEDIA_ROOT, dest_dirpath)
        dest_files = []

        for filepath in self.filepaths():
            if not os.path.exists(filepath):
                continue

            os.makedirs(dest_path, exist_ok=True)
            filename = os.path.basename(filepath)
            dest_filepath = os.path.join(dest_path, filename)
            name, ext = os.path.splitext(filename)
            count = 0
            while os.path.exists(dest_filepath):
                filename = f'{name}_{count}{ext}'
                dest_filepath = os.path.join(dest_path, filename)
                count += 1

            shutil.move(filepath, dest_filepath)
            dest_files.append(os.path.join(settings.MEDIA_URL, dest_path, filename))

        return dest_files

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
