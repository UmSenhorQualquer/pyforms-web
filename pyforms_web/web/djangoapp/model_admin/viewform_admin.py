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
from pyforms_web.web.Controls.ControlLabel 			import ControlLabel

from django.core.exceptions import ValidationError, FieldDoesNotExist
from pyforms_web.web.djangoapp.model_admin.utils import get_fieldsets_strings
import traceback
from django.conf import settings
from django.db import models
import os


class ViewFormAdmin(BaseWidget):

	inlines 	 = []
	fieldsets	 = None

	def __init__(self, title, model, pk, parent=None):
		"""
		Parameters:
      		title  - Title of the app.
      		model  - Model with the App will represent.
      		parent - Variable with the content [model, foreign key id]. It is used to transform the App in an inline App
		"""
		BaseWidget.__init__(self, title)
		self.model 		 = model
		self.edit_fields = []

		self.parent_pk		= None
		self.parent_field 	= None
		self.parent_model 	= None
		self.object_pk 		= None

		# used to configure the interface to inline
		# it will filter the dataset by the foreign key
		if parent: self.set_parent(parent[0], parent[1])
		
		self.create_model_formfields()
		if pk:
			self.object_pk = pk
			self.show_edit_form()

	#################################################################################
	#################################################################################



	#################################################################################
	#################################################################################
	
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
			elif isinstance(field, models.BigAutoField):  				pyforms_field = ControlText( field.verbose_name )
			elif isinstance(field, models.BigIntegerField):  			pyforms_field = ControlInteger( field.verbose_name )
			elif isinstance(field, models.BinaryField):  				pyforms_field = ControlText( field.verbose_name )
			elif isinstance(field, models.BooleanField):  				pyforms_field = ControlCheckBox( field.verbose_name )
			elif isinstance(field, models.CharField):  					pyforms_field = ControlText( field.verbose_name )
			elif isinstance(field, models.CommaSeparatedIntegerField):	pyforms_field = ControlText( field.verbose_name )
			elif isinstance(field, models.DateTimeField):  				pyforms_field = ControlDateTime( field.verbose_name )
			elif isinstance(field, models.DateField):  					pyforms_field = ControlDate( field.verbose_name )
			elif isinstance(field, models.DecimalField):  				pyforms_field = ControlFloat( field.verbose_name )
			elif isinstance(field, models.DurationField):  				pyforms_field = ControlText( field.verbose_name )
			elif isinstance(field, models.EmailField):  				pyforms_field = ControlText( field.verbose_name )
			elif isinstance(field, models.FileField):  					pyforms_field = ControlFileUpload( field.verbose_name )
			elif isinstance(field, models.FilePathField):  				pyforms_field = ControlText( field.verbose_name )
			elif isinstance(field, models.FloatField):  				pyforms_field = ControlFloat( field.verbose_name )
			elif isinstance(field, models.ImageField):  				pyforms_field = ControlFileUpload( field.verbose_name )
			elif isinstance(field, models.IntegerField):  				pyforms_field = ControlInteger( field.verbose_name )
			elif isinstance(field, models.GenericIPAddressField):  		pyforms_field = ControlText( field.verbose_name )
			elif isinstance(field, models.NullBooleanField):  			pyforms_field = ControlText( field.verbose_name )
			elif isinstance(field, models.PositiveIntegerField):  		pyforms_field = ControlText( field.verbose_name )
			elif isinstance(field, models.PositiveSmallIntegerField): 	pyforms_field = ControlText( field.verbose_name )
			elif isinstance(field, models.SlugField):  					pyforms_field = ControlText( field.verbose_name )
			elif isinstance(field, models.SmallIntegerField):  			pyforms_field = ControlText( field.verbose_name )
			elif isinstance(field, models.TextField):  					pyforms_field = ControlLabel( field.verbose_name )
			elif isinstance(field, models.TimeField):  					pyforms_field = ControlText( field.verbose_name )
			elif isinstance(field, models.URLField):  					pyforms_field = ControlText( field.verbose_name )
			elif isinstance(field, models.UUIDField):  					pyforms_field = ControlText( field.verbose_name )
			elif isinstance(field, models.ForeignKey): 	
				#Foreign key
				pyforms_field = ControlCombo( field.verbose_name )
				for instance in field.rel.to.objects.all(): pyforms_field.add_item( str(instance), instance.pk )			
			elif isinstance(field, models.ManyToManyField):
				#Many to Many field
				pyforms_field = ControlMultipleSelection( field.verbose_name )
				for instance in field.rel.to.objects.all():
					pyforms_field.add_item( str(instance), instance.pk )

			if pyforms_field is not None: 
				setattr(self, field.name, pyforms_field)
				formset.append(field.name)
				self.edit_fields.append( pyforms_field )

		#Create the inlines eition forms.
		self.inlines_controls_name 	= []
		self.inlines_controls 		= []
		for inline in self.inlines:
			pyforms_field = ControlEmptyWidget()
			setattr(self, inline.__name__, pyforms_field)
			self.inlines_controls_name.append(inline.__name__)
			self.inlines_controls.append( pyforms_field )
			formset.append(inline.__name__)
			
		self.formset = self.fieldsets if self.fieldsets else formset


	def hide_form(self):
		for field in self.edit_fields: 		field.hide()
		for field in self.inlines_controls: field.hide()
	
	def show_form(self):
		for field in self.edit_fields: 		field.show()
		for field in self.inlines_controls: field.show()
		
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
				getattr(self, field.name).value = [str(o.pk) for o in getattr(obj, field.name).all()]
			
			getattr(self, field.name).enabled = False

		for inline in self.inlines:
			getattr(self, inline.__name__).value = inline( (self.model, self.object_pk) )



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


