import os
import shutil

from django.conf import settings
from django.db.models import NOT_PROVIDED
from pyforms_web.controls.control_base import ControlBase
import simplejson

class ControlFileUpload(ControlBase):

	def init_form(self):
		return "new ControlFileUpload('{0}', {1})".format( self._name, simplejson.dumps(self.serialize()) )

	@property
	def filepath(self):
		if self.value:
			return os.path.join(settings.MEDIA_ROOT, self.value[len(settings.MEDIA_URL):] )
		else:
			return None

	def move_to(self, dest_dirpath):
		dest_path = os.path.join(settings.MEDIA_ROOT, dest_dirpath)

		if not os.path.exists(self.filepath):
			return

		os.makedirs(dest_path, exist_ok=True)
		filename = os.path.basename(self.filepath)
		dest_filepath = os.path.join(dest_path, filename)
		name, ext = os.path.splitext(filename)
		count = 0
		while os.path.exists(dest_filepath):
			filename = f'{name}_{count}{ext}'
			dest_filepath = os.path.join(dest_path, filename)
			count += 1

		shutil.move(self.filepath, dest_filepath)
		self.value = os.path.join(settings.MEDIA_URL, dest_path, filename)
		return self.value

	def serialize(self):
		data = super(ControlFileUpload, self).serialize()

		if self.value and self.value!=NOT_PROVIDED:
			try:
				file_data = {
					'name': os.path.basename(self.value),
					'size': os.path.getsize(self.filepath),
					'file': self.value,
					 'url': self.value
				}
				data.update({ 'file_data':file_data })
			except OSError:
				pass

		return data