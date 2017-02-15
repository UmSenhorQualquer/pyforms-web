import os
from django.conf import settings
from pyforms_web.web.Controls.ControlBase import ControlBase

class ControlFileUpload(ControlBase):

	def init_form(self):
		return "new ControlFileUpload('{0}', {1})".format( self._name, str(self.serialize()) )

	@property
	def value(self): return str(ControlBase.value.fget(self))

	@value.setter
	def value(self, value):ControlBase.value.fset(self, value)

	def serialize(self):
		data 	  = super(ControlFileUpload, self).serialize()
		if self.value:
			try:
				filepath = os.path.join( settings.MEDIA_ROOT, self.value[len(settings.MEDIA_URL):] )
				file_data = {
					'name': os.path.basename(self.value),
					'size': os.path.getsize(filepath),
					'file': 'http://localhost:8000'+self.value,
					 'url':'http://localhost:8000'+self.value
				}
				data.update({ 'file_data':file_data })
			except OSError:
				pass

		return data