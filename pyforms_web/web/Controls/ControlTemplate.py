from pyforms_web.web.Controls.ControlBase import ControlBase
from django.template.loader import render_to_string
import simplejson

class ControlTemplate(ControlBase):


	def __init__(self, label = "", defaultValue = None, helptext=''):
		super(ControlTemplate, self).__init__(label, None, helptext)
		self._template = defaultValue
		self.action_param = None

	def init_form(self):
		return """new ControlTemplate('{0}', {1})""".format(
			self._name, 
			simplejson.dumps(self.serialize()) 
		)

	def serialize(self):
		data = super(ControlTemplate,self).serialize()		
		html = render_to_string(self._template, self.value)
		data.update({'value':html})
		return data


	def deserialize(self, properties):
		self._label   = properties.get('label','')
		self._help    = properties.get('help','')
		self._visible = properties.get('visible',True)
		self.action_param = properties.get('action_param', None)
		
	@property
	def template(self):
	    return self._template
	@template.setter
	def template(self, value): self._template = value
