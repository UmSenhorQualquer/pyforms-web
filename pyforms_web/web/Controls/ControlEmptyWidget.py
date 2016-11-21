from pyforms_web.web.Controls.ControlBase import ControlBase
from pyforms_web.web.BaseWidget import BaseWidget
import base64, dill, StringIO


class ControlEmptyWidget(ControlBase):

	def __init__(self, label = "", defaultValue = "", helptext=''):
		super(ControlEmptyWidget,self).__init__(label, defaultValue, helptext)
		self._widget = None

	def init_form(self):
		return """new ControlEmptyWidget('{0}', {1})""".format(
			self._name, 
			self.serialize()
		)


	def serialize(self):
		data = ControlBase.serialize(self)
		
		#Serialize the BaseWidget in the value
		if isinstance(self.value, BaseWidget):
			self.value.parent = None
		buf = StringIO.StringIO(); dill.dump(self.value, buf) 
		value = buf.getvalue()
		
		data.update({'value':base64.b64encode(value) })

		if isinstance(self.value, BaseWidget) and self._update_client:
			self._widget = self.value.init_form(parent=self.parent)
			data.update({'clear_widget': 1})
			data.update({'html':base64.b64encode(self._widget['code']) })
			data.update({'child_widget_id': self.value.uid })
		elif self.value=='' or self.value==None:
			data.update({'clear_widget': 1})
			
		if isinstance(self.value, BaseWidget):
			data.update({'widget_data': self.value.serializeForm()})
			
			
		return data

	def deserialize(self, properties):
		self._label   	  = properties.get('label','')
		self._help    	  = properties.get('help','')
		self._visible 	  = int(properties.get('visible',True))==1

		serialized_basewidget = properties.get('value',None)
		
		if serialized_basewidget:
			serialized_basewidget = base64.b64decode(serialized_basewidget)
			widget_data 		  = properties.get('widget_data', None)
			if serialized_basewidget!='' and widget_data and widget_data!='':
				self.value  = dill.loads(serialized_basewidget)
				if self.value and self.value!='':
					self.value.parent = self.parent
					self.value.loadSerializedForm( widget_data )


	def mark_to_update_client(self):
		 self._update_client = True
		 if self.parent is not None: self.httpRequest.updated_apps.add_bottom(self.parent)

	@property
	def value(self): return ControlBase.value.fget(self)

	@value.setter
	def value(self, value):
		ControlBase.value.fset(self, value)
		if value: value.is_new_app = False