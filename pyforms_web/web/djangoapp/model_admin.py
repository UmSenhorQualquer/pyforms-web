from pyforms_web.web.BaseWidget import BaseWidget
from pyforms_web.web.Controls.ControlTextArea import ControlTextArea
from pyforms_web.web.Controls.ControlText import ControlText
from pyforms_web.web.Controls.ControlCombo import ControlCombo
from pyforms_web.web.Controls.ControlDate import ControlDate
from pyforms_web.web.Controls.ControlButton import ControlButton
from pyforms_web.web.Controls.ControlList import ControlList
from pyforms_web.web.Controls.ControlMultipleSelection import ControlMultipleSelection
from pyforms_web.web.Controls.ControlEmptyWidget import ControlEmptyWidget
from pyforms_web.web.Controls.ControlFileUpload import ControlFileUpload
from django.conf import settings
from django.db import models
import collections, os


def get_strs(l):
	if not isinstance(l, collections.Iterable): return []
	res = []
	for e in l:
		if isinstance(e, str): res.append(e)
		else: res += get_strs(e)
	return res


class ModelAdmin(BaseWidget):

	list_display = None
	inlines 	 = []
	fieldsets	 = None

	def __init__(self, title, model, parent=None):
		BaseWidget.__init__(self, title)
		self.model = model
		self.edit_fields = []

		self.parent_pk		= None
		self.parent_field 	= None
		self.parent_model 	= None
		self.object_pk 		= None

		if parent: self.set_parent(parent[0], parent[1])

		
		self._add_btn 		= ControlButton('<i class="plus icon"></i> Add')
		self._list 			= ControlList('List')
		self._save_btn 		= ControlButton('<i class="save icon"></i> Save')
		self._create_btn 	= ControlButton('<i class="plus icon"></i> Create')
		self._remove_btn 	= ControlButton('<i class="minus icon"></i> Remove')			
		self._cancel_btn 	= ControlButton('<i class="hide icon"></i> Cancel')

		
		self.edit_fields.append( self._save_btn )
		self.edit_fields.append( self._create_btn )
		self.edit_fields.append( self._remove_btn )
		self.edit_fields.append( self._cancel_btn )
				
		self._add_btn.value 	= self.__add_btn_event
		self._cancel_btn.value 	= self.__cancel_btn_event
		self._create_btn.value 	= self.__create_btn_event
		self._remove_btn.value 	= self.__remove_btn_event
		self._save_btn.value 	= self.__save_btn_event
		self._list.item_selection_changed_event = self.__list_item_selection_changed_event

		self._list.select_entire_row = True
		self.__populate_list()

		self.set_model_formfields()
		


	def set_model_formfields(self):
		fields2show = self.get_visible_fields_names()
		
		formset 		 = []
		for field in self.model._meta.get_fields():
			if field.name not in fields2show: continue

			if hasattr(field, 'verbose_name'):
				pyforms_field = None

				if isinstance(field, models.AutoField): continue
				if isinstance(field, models.ForeignKey): 	
					pyforms_field = ControlCombo( field.verbose_name )
					for instance in field.rel.to.objects.all():
						pyforms_field.add_item( str(instance), instance.pk )
				if isinstance(field, models.CharField):  		pyforms_field = ControlText( field.verbose_name )
				if isinstance(field, models.FileField):  		pyforms_field = ControlFileUpload( field.verbose_name )
				if isinstance(field, models.TextField):  		pyforms_field = ControlTextArea( field.verbose_name )
				if isinstance(field, models.DateTimeField): 	pyforms_field = ControlDate( field.verbose_name )
				if isinstance(field, models.ManyToManyField):

					pyforms_field = ControlMultipleSelection( field.verbose_name )
					for instance in field.rel.to.objects.all():
						pyforms_field.add_item( str(instance), instance.pk )			
				
				if pyforms_field is not None: 
					setattr(self, field.name, pyforms_field)
					formset.append(field.name)
					self.edit_fields.append( pyforms_field )

		self.inlines_controls_name = []
		self.inlines_controls = []
		for inline in self.inlines:
			pyforms_field = ControlEmptyWidget()
			setattr(self, inline.__name__, pyforms_field)
			self.inlines_controls_name.append(inline.__name__)
			self.inlines_controls.append( pyforms_field )
			formset.append(inline.__name__)
			
		self.formset = self.fieldsets if self.fieldsets else formset

		self.hide_edit_create_form()


	def init_form(self, parent=None):

		self.formset = ['_add_btn', '_list'] + self.formset + [('_save_btn', '_create_btn','_remove_btn', '_cancel_btn')]
		return super(ModelAdmin, self).init_form(parent)

	def __populate_list(self):
		queryset = self.model.objects.all()
		if self.parent_field:
			queryset = queryset.filter(**{self.parent_field.name: self.parent_pk})
			
		if self.list_display is None:
			self._list.horizontal_headers = ['',self.model._meta.verbose_name]
			self._list.value = [ [m.pk, str(m)] for m in queryset]
		else:
			self._list.horizontal_headers = ['']+[self.model._meta.get_field(field_name).verbose_name for field_name in self.list_display]
			rows = []
			for m in queryset:
				row = [m.pk]
				for field_name in self.list_display:
					row.append( getattr(m, field_name) )
				rows.append(row)
			self._list.value = rows

		
		
	def __add_btn_event(self):
		self.show_create_form()

	def __cancel_btn_event(self):
		self.hide_edit_create_form()
		


	def show_create_form(self):
		self._add_btn.hide()
		self._list.hide()
		for field in self.edit_fields: field.show()
		self._save_btn.hide()

		fields2show = self.get_visible_fields_names()
		
		for field in self.model._meta.get_fields():
			if field.name not in fields2show: continue

			if isinstance(field, (models.ForeignKey,models.CharField,models.TextField, models.DateTimeField) ):
				getattr(self, field.name).value = ''

	def show_edit_form(self):
		self._add_btn.hide()
		self._list.hide()
		for field in self.edit_fields: 		field.show()
		for field in self.inlines_controls: field.show()
		self._create_btn.hide()

		obj = self.model.objects.get(pk=self.object_pk)
		fields2show = self.get_visible_fields_names()
		for field in self.model._meta.get_fields():
			if field.name not in fields2show: continue

			if isinstance(field, (models.CharField,models.TextField)):
				getattr(self, field.name).value = getattr(obj, field.name)

			if isinstance(field, models.FileField):
				getattr(self, field.name).value = getattr(obj, field.name).url if getattr(obj, field.name) else ''

			if isinstance(field, models.DateTimeField ):
				getattr(self, field.name).value = getattr(obj, field.name).strftime("%Y-%m-%d")

			if isinstance(field, models.ForeignKey):
				value = getattr(obj, field.name).pk
				getattr(self, field.name).value = getattr(obj, field.name).pk

			if isinstance(field, models.ManyToManyField):					
				getattr(self, field.name).value = [str(o.pk) for o in getattr(obj, field.name).all()]

		for inline in self.inlines:
			getattr(self, inline.__name__).value = inline( (self.model, self.object_pk) )

	def hide_edit_create_form(self):
		self._add_btn.show()
		self._list.show()
		for field in self.edit_fields: 		field.hide()
		for field in self.inlines_controls: field.hide()
		self._list.selected_row_index = -1
		self.object_pk = None

	def __create_btn_event(self):
		fields2show = self.get_visible_fields_names()
		
		obj = self.model()
		for field in self.model._meta.get_fields():
			if field.name not in fields2show: continue

			field_name = '{0}'.format(field.name)

			if isinstance(field, (models.CharField,models.TextField, models.DateTimeField) ):
				value = getattr(self, field_name).value
				setattr(obj, field.name, value)

			if isinstance(field, models.ForeignKey):
				value = getattr(self, field_name).value
				value = field.rel.to.objects.get(pk=value)
				setattr(obj, field.name, value)

			if isinstance(field, models.FileField):
				value = getattr(self, field_name).value
				if value:
					try:
						os.makedirs(os.path.join(settings.MEDIA_ROOT, field.upload_to))
					except os.error as e:
						pass

					paths = [p for p in value.split('/') if len(p)>0][1:]
					from_path 	= os.path.join(settings.MEDIA_ROOT,*paths)
					to_path 	= os.path.join(settings.MEDIA_ROOT, field.upload_to, os.path.basename(value) )
					os.rename(from_path, to_path)

					url = '/'.join([field.upload_to]+[os.path.basename(value) ])
					setattr(obj, field.name, url)
				elif field.null:
					setattr(obj, field.name, None)
				else:
					setattr(obj, field.name, '')

		if self.parent_model:
			parent = self.parent_model.objects.get(pk=self.parent_pk)
			setattr(obj, self.parent_field.name, parent)
		obj.save()

		self.object_pk = obj.pk
		self.__populate_list()

		if self.inlines:
			self.show_edit_form()
		else:
			self.hide_edit_create_form()

		self.success('The object <b>{0}</b> was created with success!'.format(obj),'Success!')

	def __save_btn_event(self):
		fields2show = self.get_visible_fields_names()
		
		obj = self.model.objects.get(pk=self.object_pk)
		for field in self.model._meta.get_fields():
			if field.name not in fields2show: continue

			field_name = '{0}'.format(field.name)

			if isinstance(field, (models.CharField,models.TextField, models.DateTimeField) ):
				value = getattr(self, field_name).value
				setattr(obj, field.name, value)

			if isinstance(field, models.ForeignKey):
				value = getattr(self, field_name).value
				value = field.rel.to.objects.get(pk=value)
				setattr(obj, field.name, value)

			if isinstance(field, models.FileField):
				value = getattr(self, field_name).value
				if value:
					try:
						os.makedirs(os.path.join(settings.MEDIA_ROOT, field.upload_to))
					except os.error as e:
						pass

					paths = [p for p in value.split('/') if len(p)>0][1:]
					from_path 	= os.path.join(settings.MEDIA_ROOT,*paths)
					to_path 	= os.path.join(settings.MEDIA_ROOT, field.upload_to, os.path.basename(value) )
					os.rename(from_path, to_path)

					url = '/'.join([field.upload_to]+[os.path.basename(value) ])
					setattr(obj, field.name, url)
				elif field.null:
					setattr(obj, field.name, None)
				else:
					setattr(obj, field.name, '')

		obj.save()

		for field in self.model._meta.get_fields():
			if isinstance(field, models.ManyToManyField):
				values = getattr(self, field.name).value
				field_instance = getattr(obj, field.name)
				field_instance.clear()
				for value in values:
					o = field.rel.to.objects.get(pk=value)
					field_instance.add(o)

		self.__populate_list()
		self.hide_edit_create_form()

		self.success('The object <b>{0}</b> was saved with success!'.format(obj),'Success!')

	def __list_item_selection_changed_event(self):
		if self._list.selected_row_index>=0:
			self.object_pk = self._list.value[self._list.selected_row_index][0]
			self.show_edit_form()
			

	def __remove_btn_event(self):
		if self.object_pk:
			obj = self.model.objects.get(pk=self.object_pk)
			obj.delete()
			self.hide_edit_create_form()
			self.__populate_list()


	def set_parent(self, parent_model, parent_pk):
		self.parent_pk 		= parent_pk
		self.parent_model 	= parent_model

		for field in self.model._meta.get_fields():
			if isinstance(field, models.ForeignKey):
				if parent_model == field.rel.to:
					self.parent_field = field
					break


	def get_visible_fields_names(self):
		fields = get_strs(self.fieldsets) if self.fieldsets else [field.name for field in self.model._meta.get_fields()]
		if self.parent_field: fields.remove(self.parent_field.name)
		return fields