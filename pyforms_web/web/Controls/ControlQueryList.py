from pyforms_web.web.Controls.ControlBase import ControlBase
from django.apps import apps
from django.db.models.constants import LOOKUP_SEP
from django.core.exceptions import FieldDoesNotExist
from django.utils.encoding import force_text
import simplejson

def get_verbose_name(model, lookup):
	# will return first non relational field's verbose_name in lookup
	parts = lookup.split(LOOKUP_SEP)
	for i, part in enumerate(parts):
		try:
			f = model._meta.get_field(part)
		except FieldDoesNotExist:
			# check if field is related
			for f in model._meta.related_objects:
				if f.get_accessor_name() == part:
					break
			else:
				raise ValueError("Invalid lookup string")

		if f.is_relation:
			model = f.related_model
			if (len(parts)-1)==i:
				return force_text(model._meta.verbose_name)
			else:
				continue

		return force_text(f.verbose_name)
		


class ControlQueryList(ControlBase):

	def __init__(self, label = "", defaultValue = "", helptext=''):
		self.rows_per_page 		= 10
		self._current_page 		= 1

		self.list_display 		= []
		self.list_filter 		= []
		self.filter_by 			= []
		self.sort_by 			= []
		self._selected_row_id   = -1 #row selected by the mouse

		# these informations is needed to serialize the control to the drive
		self._app 	= None
		self._model = None
		self._query = None
		####################################################################

		super(ControlQueryList, self).__init__(label, defaultValue, helptext)


	def init_form(self): return "new ControlQueryList('{0}', {1})".format( self._name, simplejson.dumps(self.serialize()) )

	def item_selection_changed_client_event(self):
		self.mark_to_update_client()
		self.item_selection_changed_event()

	def item_selection_changed_event(self): pass

	def __get_pages_2_show(self, queryset):
		if not queryset: return []

		total_rows 		= queryset.count()
		total_n_pages 	= (total_rows / self.rows_per_page) + (0 if (total_rows % self.rows_per_page)==0 else 1)
		start_page 		= self._current_page - 2
		end_page 		= self._current_page + 2

		if start_page<1:
			diff 	 	= 1 - start_page
			start_page 	= 1
			end_page 	+= diff
		if end_page>total_n_pages:
			end_page = total_n_pages
			if (end_page-4)>=1: start_page = (end_page-4)

		return [(start_page-1) if start_page>1 else -1] + range(start_page, end_page+1) + [ (end_page+1) if end_page<total_n_pages else -1]



	

	@property
	def selected_row_id(self): return self._selected_row_id
	@selected_row_id.setter
	def selected_row_id(self, value): self._selected_row_id = value
	
	@property
	def value(self):
		if self._app and self._model and self._query:
			# reconstruct the query ################################
			model 		= apps.get_model(self._app, self._model)
			qs 			= model.objects.all()
			qs.query 	= self._query
			for f in self.filter_by: 
				qs = qs.filter(**f)
			return qs
		else:
			return None

	@value.setter
	def value(self, value):
		if value:
			self._model = value.model._meta.label.split('.')[-1]
			self._query = value.query
			self._app   = value.model._meta.app_label
			self._selected_row_id = -1
			
		oldvalue = self._value
		self._value = value
		if oldvalue!=value: 
			self.mark_to_update_client()
			self.changed_event()



	def serialize(self):
		data 			= ControlBase.serialize(self)
		queryset 		= self.value

		rows 			= []
		filters_list 	= []
		headers 		= []

		if queryset:
			model 	 	 	= queryset.model
			

			row_start = self.rows_per_page*(self._current_page-1)
			row_end   = self.rows_per_page*(self._current_page)

			for sort in self.sort_by:
				direction = '-' if sort['desc'] else ''
				queryset = queryset.order_by( direction+sort['column'] )


			if self.list_display is None or len(self.list_display)==0:
				rows = [ [m.pk, str(m)] for m in queryset[row_start:row_end] ]
			else:
				rows = []
				for row in queryset.values_list(*(['pk']+self.list_display) )[row_start:row_end]:
					#row = [str(m.pk)]
					#for field_name in self.list_display:
					#	row.append( str(getattr(m, field_name)) )
					rows.append(row)

				#configure the headers titles
				for column_name in self.list_display:
					headers.append({
						'label':  get_verbose_name(model, column_name),
						'column': column_name
					})
			
			#configure the filters
			for column_name in self.list_filter:
				column_values = queryset.values_list(column_name, flat=True).distinct()
				filters_list.append({
					'label':  get_verbose_name(model, column_name),
					'column': column_name,
					'items':  [row for row in column_values]
				})
	

		data.update({
			'filters_list': 		filters_list,
			'filter_by':			self.filter_by,
			'sort_by':				self.sort_by,
			'pages':				{'current_page': self._current_page, 'pages_list':self.__get_pages_2_show(queryset) },
			'value':				'',
			'values':				rows,
			'horizontal_headers': 	headers,
			'selected_row_id':		self._selected_row_id
		})

		if self._selected_row_id: 
			data.update({})

		return data

	





	def deserialize(self, properties):
		ControlBase.deserialize(self,properties)
		self.sort_by 			= properties.get('sort_by', [])
		self.filter_by 			= properties.get('filter_by',[])
		self._current_page	    = int(properties['pages']['current_page'])
		self._selected_row_id 	= properties.get('selected_row_id', -1)
		
	def page_changed_event(self): 
		self._selected_row_id = -1
		self.mark_to_update_client()

	def sort_changed_event(self): 
		self._selected_row_id = -1
		self.mark_to_update_client()

	def filter_changed_event(self):
		self._selected_row_id = -1
		self._current_page 	  = 1
		self.mark_to_update_client()