from pyforms_web.web.Controls.ControlBase import ControlBase
from django.apps import apps

class ControlQueryList(ControlBase):

	def __init__(self, label = "", defaultValue = "", helptext=''):
		self._titles 			= []
		self._select_entire_row = False
		self._read_only 		= False
		self._selected_index 	= -1
		self.list_display 		= []
		self.list_filter 		= []
		self._app = None
		self._model = None
		self._query = None
		super(ControlQueryList, self).__init__(label, defaultValue, helptext)


	def init_form(self): return "new ControlQueryList('{0}', {1})".format( self._name, str(self.serialize()) )

	def item_selection_changed_event(self): pass

	def dbl_click(self): pass

	@property
	def horizontal_headers(self): return map(str, self._titles)

	@horizontal_headers.setter
	def horizontal_headers(self, value):
		self.mark_to_update_client()
		self._titles = value

	@property
	def select_entire_row(self): return self._select_entire_row

	@select_entire_row.setter
	def select_entire_row(self, value):
		self.mark_to_update_client()
		self._select_entire_row = value

	@property
	def readonly(self): return self._read_only

	@readonly.setter
	def readonly(self, value):
		self.mark_to_update_client()
		self._read_only = value

	@property
	def selected_row_index(self): return self._selected_index

	@selected_row_index.setter
	def selected_row_index(self, value):
		self.mark_to_update_client()
		self._selected_index = value


	@property
	def value(self):
		if self._app and self._model and self._query:
			model = apps.get_model(self._app, self._model)
			qs = model.objects.all()
			qs.query = self._query
			return qs
		else:
			return None
	@value.setter
	def value(self, value):
		if value:
			self._model = value.model._meta.label.split('.')[-1]
			self._query = value.query
			self._app   = value.model._meta.app_label
			self._selected_index = -1
			
		oldvalue = self._value
		self._value = value
		if oldvalue!=value: 
			self.mark_to_update_client()
			self.changed_event()



	def serialize(self):
		data 	= ControlBase.serialize(self)
		queryset = self.value
		if queryset:
			model = queryset.model

			if self.list_display is None or len(self.list_display)==0:
				values = [ [int(m.pk), str(m)] for m in queryset]
			else:
				rows = []
				for m in queryset:
					row = [int(m.pk)]
					for field_name in self.list_display:
						row.append( str(getattr(m, field_name)) )
					rows.append(row)
				values = rows

			orderby_items = []
			for field in model._meta.get_fields():
				if hasattr(field, 'verbose_name'):
					orderby_items.append({
						'label': str(field.verbose_name), 
						'value': str(field.name)
					})

			filters_list = []
			for column_name in self.list_filter:
				field = model._meta.get_field(column_name)
				if not hasattr(field, 'verbose_name'):continue
				
				column_values = model.objects.values_list(column_name, flat=True).distinct()
				filters_list.append({
					'label':  str(field.verbose_name),
					'column': str(column_name),
					'items':  [{'label':str(v), 'key':str(v) } for v in column_values]
				})

		else:
			values = []
			orderby_items = []
			filters_list = []

		data.update({
			'orderby_items':		orderby_items,
			'filters_list': 		filters_list,
			'value':				'',
			'values':				values,
			'horizontal_headers': 	self.horizontal_headers,
			'read_only':			1 if self._read_only else 0,
			'selected_index':		self._selected_index,
			'select_entire_row': 	1 if self._select_entire_row else 0,
		})
		return data

	def deserialize(self, properties):
		ControlBase.deserialize(self,properties)

		self.horizontal_headers = properties['horizontal_headers']
		self._read_only 		= properties['read_only']==1
		self._selected_index 	= properties['selected_index']
		self._select_entire_row = properties['select_entire_row']==1
