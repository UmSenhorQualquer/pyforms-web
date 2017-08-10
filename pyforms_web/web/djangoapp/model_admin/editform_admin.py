from pyforms_web.web.BaseWidget 						import BaseWidget
from pyforms_web.web.Controls.ControlTextArea 			import ControlTextArea
from pyforms_web.web.Controls.ControlText 				import ControlText
from pyforms_web.web.Controls.ControlInteger 			import ControlInteger
from pyforms_web.web.Controls.ControlFloat 				import ControlFloat
from pyforms_web.web.Controls.ControlCombo 				import ControlCombo
from pyforms_web.web.Controls.ControlDate 				import ControlDate
from pyforms_web.web.Controls.ControlDateTime 			import ControlDateTime
from pyforms_web.web.Controls.ControlButton 			import ControlButton
from pyforms_web.web.Controls.ControlQueryList 			import ControlQueryList
from pyforms_web.web.Controls.ControlMultipleSelection 	import ControlMultipleSelection
from pyforms_web.web.Controls.ControlEmptyWidget 		import ControlEmptyWidget
from pyforms_web.web.Controls.ControlFileUpload 		import ControlFileUpload
from pyforms_web.web.Controls.ControlCheckBox 			import ControlCheckBox

from django.core.exceptions import ValidationError, FieldDoesNotExist
from pyforms_web.web.djangoapp.model_admin.utils import get_fieldsets_strings
import traceback
from django.conf import settings
from django.db import models
import os


class EditFormAdmin(BaseWidget):

	inlines 	 = []
	fieldsets	 = None
	
	SAVE_BTN_LABEL   = '<i class="save icon"></i> Save'
	CREATE_BTN_LABEL = '<i class="plus icon"></i> Create'
	CANCEL_BTN_LABEL = '<i class="hide icon"></i> Close'
	REMOVE_BTN_LABEL = '<i class="trash outline icon"></i> Remove'

	def __init__(self, title, model, pk, parent=None, parent_win=None):
		"""
		Parameters:
			title  - Title of the app.
			model  - Model with the App will represent.
			parent - Variable with the content [model, foreign key id]. It is used to transform the App in an inline App
		"""
		BaseWidget.__init__(self, title, parent_win=parent_win)
		self.model 		 = model
		self.edit_fields = []

		self.parent_pk		= None
		self.parent_field 	= None
		self.parent_model 	= None
		self.object_pk 		= None

		# used to configure the interface to inline
		# it will filter the dataset by the foreign key
		if parent: self.set_parent(parent[0], parent[1])

		# buttons
		self._save_btn 		= ControlButton(self.SAVE_BTN_LABEL)
		self._create_btn 	= ControlButton(self.CREATE_BTN_LABEL)
		self._remove_btn 	= ControlButton(self.REMOVE_BTN_LABEL)	
		self._cancel_btn 	= ControlButton(self.CANCEL_BTN_LABEL)
		
		self._remove_btn.css = 'red basic'
		self._cancel_btn.css = 'gray basic'
		
		
		self.edit_fields.append( self._save_btn )
		self.edit_fields.append( self._create_btn )
		self.edit_fields.append( self._remove_btn )
		self.edit_fields.append( self._cancel_btn )

		for field in self.edit_fields: field.hide()
				
		# events
		self._create_btn.value 	= self.__create_btn_event
		self._remove_btn.value 	= self.__remove_btn_event
		self._save_btn.value 	= self.__save_btn_event
		self._cancel_btn.value 	= self.cancel_btn_event
		
		self._create_btn.include_label	= False
		self._remove_btn.include_label	= False
		self._save_btn.include_label	= False
		self._cancel_btn.include_label	= False
		
		
		
		self.create_model_formfields()
		if pk:
			self.object_pk = pk
			self.show_edit_form()
		else:
			self.show_create_form()

	#################################################################################
	#################################################################################

	def init_form(self, parent=None):
		self.formset = self.formset + [(BaseWidget.FORM_NO_ROW_ALIGNMENT, '_save_btn', '_create_btn', '_cancel_btn', ' ' ,'_remove_btn')]
		return super(EditFormAdmin, self).init_form(parent)

	#################################################################################
	#################################################################################
	
	def hide_form(self):
		for field in self.edit_fields: 		field.hide()
		for field in self.inlines_controls: field.hide()
	
	def show_form(self):
		for field in self.edit_fields: 		field.show()
		for field in self.inlines_controls: field.show()


	def cancel_btn_event(self):
		self.hide_form()









	#################################################################################
	#################################################################################

	def update_related_fields(self):

		fields2show = self.get_visible_fields_names()		
		formset 	= []

		for field in self.model._meta.get_fields():
			if field.name not in fields2show: continue #only update this field if is visible
			pyforms_field = None

			if isinstance(field, models.ForeignKey):
				#Foreign key
				pyforms_field = getattr(self, field.name)
				pyforms_field.clear_items()
				for instance in field.rel.to.objects.all():
					pyforms_field.add_item( str(instance), instance.pk )			
			elif isinstance(field, models.ManyToManyField):
				#Many to Many field
				pyforms_field = getattr(self, field.name)
				pyforms_field.clear_items()
				for instance in field.rel.to.objects.all():
					pyforms_field.add_item( str(instance), instance.pk )

		"""
		#Create the inlines eition forms.
		self.inlines_controls_name 	= []
		self.inlines_controls 		= []
		for inline in self.inlines:
			pyforms_field = ControlEmptyWidget()
			#pyforms_field._parent = self
			setattr(self, inline.__name__, pyforms_field)
			self.inlines_controls_name.append(inline.__name__)
			self.inlines_controls.append( pyforms_field )
			formset.append(inline.__name__)"""
			


	def create_model_formfields(self):
		"""
			Create the model edition form
		"""
		
		fields2show = self.get_visible_fields_names()		
		formset 	= []

		for field in self.model._meta.get_fields():
			if field.name not in fields2show: continue #only create this field if is visible
			pyforms_field = None

			if isinstance(field, models.AutoField): continue
			elif isinstance(field, models.BigAutoField):  				pyforms_field = ControlText( field.verbose_name.capitalize() )
			elif isinstance(field, models.BigIntegerField):  			pyforms_field = ControlInteger( field.verbose_name.capitalize() )
			elif isinstance(field, models.BinaryField):  				pyforms_field = ControlText( field.verbose_name.capitalize() )
			elif isinstance(field, models.BooleanField):  				pyforms_field = ControlCheckBox( field.verbose_name.capitalize() )
			elif isinstance(field, models.CharField):  					pyforms_field = ControlText( field.verbose_name.capitalize() )
			elif isinstance(field, models.CommaSeparatedIntegerField):	pyforms_field = ControlText( field.verbose_name.capitalize() )
			elif isinstance(field, models.DateTimeField):  				pyforms_field = ControlDateTime( field.verbose_name.capitalize() )
			elif isinstance(field, models.DateField):  					pyforms_field = ControlDate( field.verbose_name.capitalize() )
			elif isinstance(field, models.DecimalField):  				pyforms_field = ControlFloat( field.verbose_name.capitalize() )
			elif isinstance(field, models.DurationField):  				pyforms_field = ControlText( field.verbose_name.capitalize() )
			elif isinstance(field, models.EmailField):  				pyforms_field = ControlText( field.verbose_name.capitalize() )
			elif isinstance(field, models.FileField):  					pyforms_field = ControlFileUpload( field.verbose_name.capitalize() )
			elif isinstance(field, models.FilePathField):  				pyforms_field = ControlText( field.verbose_name.capitalize() )
			elif isinstance(field, models.FloatField):  				pyforms_field = ControlFloat( field.verbose_name.capitalize() )
			elif isinstance(field, models.ImageField):  				pyforms_field = ControlFileUpload( field.verbose_name.capitalize() )
			elif isinstance(field, models.IntegerField):  				pyforms_field = ControlInteger( field.verbose_name.capitalize() )
			elif isinstance(field, models.GenericIPAddressField):  		pyforms_field = ControlText( field.verbose_name.capitalize() )
			elif isinstance(field, models.NullBooleanField):  			pyforms_field = ControlText( field.verbose_name.capitalize() )
			elif isinstance(field, models.PositiveIntegerField):  		pyforms_field = ControlText( field.verbose_name.capitalize() )
			elif isinstance(field, models.PositiveSmallIntegerField): 	pyforms_field = ControlText( field.verbose_name.capitalize() )
			elif isinstance(field, models.SlugField):  					pyforms_field = ControlText( field.verbose_name.capitalize() )
			elif isinstance(field, models.SmallIntegerField):  			pyforms_field = ControlText( field.verbose_name.capitalize() )
			elif isinstance(field, models.TextField):  					pyforms_field = ControlTextArea( field.verbose_name.capitalize() )
			elif isinstance(field, models.TimeField):  					pyforms_field = ControlText( field.verbose_name.capitalize() )
			elif isinstance(field, models.URLField):  					pyforms_field = ControlText( field.verbose_name.capitalize() )
			elif isinstance(field, models.UUIDField):  					pyforms_field = ControlText( field.verbose_name.capitalize() )
			elif isinstance(field, models.ForeignKey): 					pyforms_field = ControlCombo( field.verbose_name.capitalize() )
			elif isinstance(field, models.ManyToManyField):  			pyforms_field = ControlMultipleSelection( field.verbose_name.capitalize() )
				
			if pyforms_field is not None: 
				setattr(self, field.name, pyforms_field)
				formset.append(field.name)
				self.edit_fields.append( pyforms_field )

		#Create the inlines eition forms.
		self.inlines_controls_name 	= []
		self.inlines_controls 		= []
		for inline in self.inlines:
			pyforms_field = ControlEmptyWidget()
			#pyforms_field._parent = self
			setattr(self, inline.__name__, pyforms_field)
			self.inlines_controls_name.append(inline.__name__)
			self.inlines_controls.append( pyforms_field )
			formset.append(inline.__name__)
			
		for c in self.controls: pass
		self.formset = self.fieldsets if self.fieldsets else formset


	
	def show_create_form(self):
		fields2show = self.get_visible_fields_names()

		self.update_related_fields()
		
		for field in self.model._meta.get_fields():
			if field.name not in fields2show: 						continue
			if isinstance(field, models.AutoField): 				continue
			elif isinstance(field, models.BigAutoField):  			continue
			elif isinstance(field, models.BigIntegerField):  		getattr(self, field.name).value = None
			elif isinstance(field, models.BinaryField):  			getattr(self, field.name).value = None
			elif isinstance(field, models.BooleanField):  			getattr(self, field.name).value = None
			elif isinstance(field, models.CharField):  				getattr(self, field.name).value = None
			elif isinstance(field, models.CommaSeparatedIntegerField):getattr(self, field.name).value = None
			elif isinstance(field, models.DateField):  				getattr(self, field.name).value = None
			elif isinstance(field, models.DateTimeField):  			getattr(self, field.name).value = None
			elif isinstance(field, models.DecimalField):  			getattr(self, field.name).value = None
			elif isinstance(field, models.DurationField):  			getattr(self, field.name).value = None
			elif isinstance(field, models.EmailField):  			getattr(self, field.name).value = None
			elif isinstance(field, models.FileField):  				getattr(self, field.name).value = None
			elif isinstance(field, models.FilePathField):  			getattr(self, field.name).value = None
			elif isinstance(field, models.FloatField):  			getattr(self, field.name).value = None
			elif isinstance(field, models.ImageField):  			getattr(self, field.name).value = None
			elif isinstance(field, models.IntegerField):  			getattr(self, field.name).value = None
			elif isinstance(field, models.GenericIPAddressField):  	getattr(self, field.name).value = None
			elif isinstance(field, models.NullBooleanField):  		getattr(self, field.name).value = None
			elif isinstance(field, models.PositiveIntegerField):  	getattr(self, field.name).value = None
			elif isinstance(field, models.PositiveSmallIntegerField): getattr(self, field.name).value = None
			elif isinstance(field, models.SlugField):  				getattr(self, field.name).value = None
			elif isinstance(field, models.SmallIntegerField):  		getattr(self, field.name).value = None
			elif isinstance(field, models.TextField):  				getattr(self, field.name).value = None
			elif isinstance(field, models.TimeField):  				getattr(self, field.name).value = None
			elif isinstance(field, models.URLField):  				getattr(self, field.name).value = None
			elif isinstance(field, models.UUIDField):  				getattr(self, field.name).value = None
			elif isinstance(field, models.ForeignKey):				getattr(self, field.name).value = None

		for field in self.edit_fields: field.show()
		self._save_btn.hide()
		self._remove_btn.hide()




	def show_edit_form(self, pk=None):
		if pk: self.object_pk = pk
		for field in self.edit_fields: 		field.show()
		for field in self.inlines_controls: field.show()
		self._create_btn.hide()

		self.update_related_fields()

		obj = self.model.objects.get(pk=self.object_pk)
		fields2show = self.get_visible_fields_names()
		for field in self.model._meta.get_fields():
			if field.name not in fields2show: continue

			if isinstance(field, models.AutoField): 				continue
			elif isinstance(field, models.BigAutoField):  			continue
			elif isinstance(field, models.BigIntegerField):  		getattr(self, field.name).value = getattr(obj, field.name)
			elif isinstance(field, models.BinaryField):  			getattr(self, field.name).value = getattr(obj, field.name)
			elif isinstance(field, models.BooleanField):  			getattr(self, field.name).value = getattr(obj, field.name)
			elif isinstance(field, models.CharField):  				getattr(self, field.name).value = getattr(obj, field.name)
			elif isinstance(field, models.CommaSeparatedIntegerField):getattr(self, field.name).value = getattr(obj, field.name)
			elif isinstance(field, models.DateField):  				getattr(self, field.name).value = getattr(obj, field.name)
			elif isinstance(field, models.DateTimeField):  			getattr(self, field.name).value = getattr(obj, field.name)
			elif isinstance(field, models.DecimalField):  			getattr(self, field.name).value = getattr(obj, field.name)
			elif isinstance(field, models.DurationField):  			getattr(self, field.name).value = getattr(obj, field.name)
			elif isinstance(field, models.EmailField):  			getattr(self, field.name).value = getattr(obj, field.name)
			elif isinstance(field, models.FileField):  				getattr(self, field.name).value = getattr(obj, field.name).url if getattr(obj, field.name) else None
			elif isinstance(field, models.FilePathField):  			getattr(self, field.name).value = getattr(obj, field.name)
			elif isinstance(field, models.FloatField):  			getattr(self, field.name).value = getattr(obj, field.name)
			elif isinstance(field, models.ImageField):  			getattr(self, field.name).value = getattr(obj, field.name).url if getattr(obj, field.name) else None
			elif isinstance(field, models.IntegerField):  			getattr(self, field.name).value = getattr(obj, field.name)
			elif isinstance(field, models.GenericIPAddressField):  	getattr(self, field.name).value = getattr(obj, field.name)
			elif isinstance(field, models.NullBooleanField):  		getattr(self, field.name).value = getattr(obj, field.name)
			elif isinstance(field, models.PositiveIntegerField):  	getattr(self, field.name).value = getattr(obj, field.name)
			elif isinstance(field, models.PositiveSmallIntegerField): getattr(self, field.name).value = getattr(obj, field.name)
			elif isinstance(field, models.SlugField):  				getattr(self, field.name).value = getattr(obj, field.name)
			elif isinstance(field, models.SmallIntegerField):  		getattr(self, field.name).value = getattr(obj, field.name)
			elif isinstance(field, models.TextField):  				getattr(self, field.name).value = getattr(obj, field.name)
			elif isinstance(field, models.TimeField):  				getattr(self, field.name).value = getattr(obj, field.name)
			elif isinstance(field, models.URLField):  				getattr(self, field.name).value = getattr(obj, field.name)
			elif isinstance(field, models.UUIDField):  				getattr(self, field.name).value = getattr(obj, field.name)
			elif isinstance(field, models.ForeignKey):
				v = getattr(obj, field.name)
				getattr(self, field.name).value = v.pk if v else None
			elif isinstance(field, models.ManyToManyField):					
				getattr(self, field.name).value = [o.pk for o in getattr(obj, field.name).all()]
			
		for inline in self.inlines:
			getattr(self, inline.__name__).value = inline( (self.model, self.object_pk) )

		return obj

	def delete_event(self):
		if self.object_pk:
			obj = self.model.objects.get(pk=self.object_pk)
			obj.delete()
			self.object_pk = None
			return True
		else:
			return False


	def save_event(self):
		fields2show = self.get_visible_fields_names()

		try:

			obj = self.model.objects.get(pk=self.object_pk) if self.object_pk else self.model()
			
			for field in self.model._meta.get_fields():
				if field.name not in fields2show: continue
			
				if isinstance(field, models.AutoField): 			continue
				elif isinstance(field, models.BigAutoField):  		continue
				elif isinstance(field, models.BigIntegerField):
					getattr(self, field.name).error = False
					setattr(obj, field.name, getattr(self, field.name).value)
				elif isinstance(field, models.BinaryField):
					getattr(self, field.name).error = False
					setattr(obj, field.name, getattr(self, field.name).value)
				elif isinstance(field, models.BooleanField):
					getattr(self, field.name).error = False  				
					setattr(obj, field.name, getattr(self, field.name).value)
				elif isinstance(field, models.CharField):
					getattr(self, field.name).error = False 					
					setattr(obj, field.name, getattr(self, field.name).value)
				elif isinstance(field, models.CommaSeparatedIntegerField):
					getattr(self, field.name).error = False	
					setattr(obj, field.name, getattr(self, field.name).value)
				elif isinstance(field, models.DateField):
					getattr(self, field.name).error = False
					value = getattr(self, field.name).value
					setattr(obj, field.name, (value if len(value) else None) )
				elif isinstance(field, models.DateTimeField):
					getattr(self, field.name).error = False
					value = getattr(self, field.name).value
					setattr(obj, field.name, (value if len(value) else None) )
				elif isinstance(field, models.DecimalField):
					getattr(self, field.name).error = False
					setattr(obj, field.name, getattr(self, field.name).value)
				elif isinstance(field, models.DurationField):
					getattr(self, field.name).error = False
					setattr(obj, field.name, getattr(self, field.name).value)
				elif isinstance(field, models.EmailField):
					getattr(self, field.name).error = False
					setattr(obj, field.name, getattr(self, field.name).value)
				elif isinstance(field, models.FilePathField):
					getattr(self, field.name).error = False
					setattr(obj, field.name, getattr(self, field.name).value)
				elif isinstance(field, models.FloatField):
					getattr(self, field.name).error = False
					setattr(obj, field.name, getattr(self, field.name).value)
				elif isinstance(field, models.ImageField):
					getattr(self, field.name).error = False
					value = getattr(self, field.name).value
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
						if url[0]=='/': url = url[1:]
						setattr(obj, field.name, url)
					elif field.null:
						setattr(obj, field.name, None)
					else:
						setattr(obj, field.name, '')
				elif isinstance(field, models.FileField):
					getattr(self, field.name).error = False
					value = getattr(self, field.name).value
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
						if url[0]=='/': url = url[1:]
						setattr(obj, field.name, url)
					elif field.null:
						setattr(obj, field.name, None)
					else:
						setattr(obj, field.name, '')
				elif isinstance(field, models.IntegerField):
					getattr(self, field.name).error = False
					setattr(obj, field.name, getattr(self, field.name).value)
				elif isinstance(field, models.GenericIPAddressField):
					getattr(self, field.name).error = False
					setattr(obj, field.name, getattr(self, field.name).value)
				elif isinstance(field, models.NullBooleanField):
					getattr(self, field.name).error = False
					setattr(obj, field.name, getattr(self, field.name).value)
				elif isinstance(field, models.PositiveIntegerField):
					getattr(self, field.name).error = False
					setattr(obj, field.name, getattr(self, field.name).value)
				elif isinstance(field, models.PositiveSmallIntegerField):
					getattr(self, field.name).error = False
					setattr(obj, field.name, getattr(self, field.name).value)
				elif isinstance(field, models.SlugField):
					getattr(self, field.name).error = False
					setattr(obj, field.name, getattr(self, field.name).value)
				elif isinstance(field, models.SmallIntegerField):
					getattr(self, field.name).error = False
					setattr(obj, field.name, getattr(self, field.name).value)
				elif isinstance(field, models.TextField):
					getattr(self, field.name).error = False
					setattr(obj, field.name, getattr(self, field.name).value)
				elif isinstance(field, models.TimeField):
					getattr(self, field.name).error = False
					setattr(obj, field.name, getattr(self, field.name).value)
				elif isinstance(field, models.URLField):
					getattr(self, field.name).error = False
					setattr(obj, field.name, getattr(self, field.name).value)
				elif isinstance(field, models.UUIDField):
					getattr(self, field.name).error = False
					setattr(obj, field.name, getattr(self, field.name).value)
				elif isinstance(field, models.ForeignKey):
					getattr(self, field.name).error = False
					value = getattr(self, field.name).value
					value = field.rel.to.objects.get(pk=value)
					setattr(obj, field.name, value)

			try:
				obj.full_clean()
			except ValidationError as e:
				html = '<ul class="list">'
				for key, messages in e.message_dict.items():
					
					try:
						field = self.model._meta.get_field(key)
						getattr(self, field.name).error = True

						html += '<li><b>{0}</b>'.format(field.verbose_name)

						field_error = True
				
					except FieldDoesNotExist:
						field_error = False
					except AttributeError:
						field_error = False


					if field_error: html += '<ul>'
					for msg in messages: html += '<li>{0}</li>'.format(msg)
					if field_error: html += '</ul></li>'
					
				html+= '</ul>'
				self.alert(html)
				return None

			obj.save()
			
			for field in self.model._meta.get_fields():
				if isinstance(field, models.ManyToManyField) and hasattr(self, field.name):
					values = getattr(self, field.name).value
					field_instance = getattr(obj, field.name)
					field_instance.clear()

					if field_instance.through is None:
						for value in values:
							o = field.rel.to.objects.get(pk=value)
							field_instance.add(o)
					else:
						for value in values:
							o = field.rel.to.objects.get(pk=value)
							rel_obj = field_instance.through()
							setattr(rel_obj,obj.__class__.__name__.lower(), obj)
							setattr(rel_obj,o.__class__.__name__.lower(), o)
							rel_obj.save()

			self.object_pk = obj.pk

			return obj

		except Exception as e:
			traceback.print_exc()
			self.alert(str(e))

			return None

	def set_parent(self, parent_model, parent_pk):
		self.parent_pk 		= parent_pk
		self.parent_model 	= parent_model

		for field in self.model._meta.get_fields():
			if isinstance(field, models.ForeignKey):
				if parent_model == field.rel.to:
					self.parent_field = field
					break


	def get_visible_fields_names(self):
		#return the names of the visible fields
		fields = get_fieldsets_strings(self.fieldsets) if self.fieldsets else [field.name for field in self.model._meta.get_fields()]
		if self.parent_field: fields.remove(self.parent_field.name)
		return fields


	#################################################################################
	#### PRIVATE FUNCTIONS ##########################################################
	#################################################################################

	def __create_btn_event(self):
		self.object_pk = None
		obj = self.save_event()
		if obj:
			self.success('The object <b>{0}</b> was saved with success!'.format(obj),'Success!')


	def __save_btn_event(self):
		obj = self.save_event()
		if obj:
			self.success('The object <b>{0}</b> was saved with success!'.format(obj),'Success!')

	
	def __remove_btn_event(self):
		self.delete_event()
		self.success('The object was deleted with success!','Success!')

	