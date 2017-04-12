from pyforms_web.web.Controls.ControlBase import ControlBase
import simplejson, collections

class ControlQueryCombo(ControlBase):


	def __init__(self, label = "", defaultValue = "", helptext=''):
		super(ControlQueryCombo, self).__init__(label, defaultValue,helptext)

		# these informations is needed to serialize the control to the drive
		self._app 	= None
		self._model = None
		self._query = None
		self._column = None
		####################################################################

	def init_form(self): return "new ControlQueryCombo('{0}', {1})".format( self._name, simplejson.dumps(self.serialize()) )
	
	def serialize(self):
		data = ControlBase.serialize(self)
		items = []
		for key, value in self.queryset:
			items.append({'label': key, 'value': value }) 
		data.update({ 'items': items, 'value': self._value })
		return data

	@property
	def display_column(self): return self._column

	@property
	def display_column(self): return self._column
	
	@property
	def queryset(self):
		if self._app and self._model and self._query:
			# reconstruct the query ################################
			model 		= apps.get_model(self._app, self._model)
			qs 			= model.objects.all()
			qs.query 	= self._query
			return qs
		else:
			return None

	@queryset.setter
	def queryset(self, value):
	
		if value:
			self._model = value.model._meta.label.split('.')[-1]
			self._query = value.query
			self._app   = value.model._meta.app_label
			self.value  = None
		else:
			self._model = None
			self._query = None
			self._app	= None