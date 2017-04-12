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

from pyforms_web.web.djangoapp.model_admin.editform_admin import EditFormAdmin

class ModelAdmin(EditFormAdmin):

	inlines 	 = []
	list_filter  = None
	list_display = None
	search_fields= None
	
	fieldsets	 = None

	list_control = ControlQueryList

	def __init__(self, title, model, parent=None):
		"""
		Parameters:
      		title  - Title of the app.
      		model  - Model with the App will represent.
      		parent - Variable with the content [model, foreign key id]. It is used to transform the App in an inline App
		"""
		EditFormAdmin.__init__(self, title, model, None, parent)

		# buttons
		self._add_btn 		= ControlButton('<i class="plus icon"></i> Add')
		self._list 			= self.list_control('List')
		
		# events
		self._add_btn.value 	= self.show_create_form
		self._list.item_selection_changed_event = self.__list_item_selection_changed_event

		self.populate_list()
		self.create_model_formfields()
		self.hide_edit_create_form()
		
		

	#################################################################################
	#################################################################################

	def init_form(self, parent=None):
		self.formset = ['_add_btn', '_list'] + self.formset + [('_save_btn', '_create_btn','_remove_btn', '_cancel_btn')]
		return BaseWidget.init_form(self, parent)

	#################################################################################
	#################################################################################


	def get_queryset(self):
		"""
			the function retrives a queryset with all the rows.
			does not include the filters made by the user in the interface
		"""
		queryset = self.model.objects.all()
		#used to filter the model for inline fields
		if self.parent_field: queryset = queryset.filter(**{self.parent_field.name: self.parent_pk})
		return queryset

	def populate_list(self):
		"""
			configures the ControlQuerySet to display the data
		"""
		print("xxxxx")
		self._list.list_display  = self.list_display  if self.list_display  else []
		self._list.list_filter 	 = self.list_filter   if self.list_filter   else []
		self._list.search_fields = self.search_fields if self.search_fields else []
		self._list.value 		 = self.get_queryset()


	def hide_edit_create_form(self):
		self._add_btn.show()
		self._list.show()
		for field in self.edit_fields: 		field.hide()
		for field in self.inlines_controls: field.hide()
		self._list.selected_row_index = -1
		self.object_pk = None
		#self.populate_list()

	def hide_form(self):
		super(ModelAdmin,self).hide_form()
		self._add_btn.show()
		self._list.show()
		self._list.selected_row_id = -1

	def save_event(self):
		res = super(ModelAdmin,self).save_event()
		if res: self.populate_list()
		return res

	def show_create_form(self):
		self._add_btn.hide()
		self._list.hide()
		super(ModelAdmin,self).show_create_form()

	def show_edit_form(self, pk=None):
		self._add_btn.hide()
		self._list.hide()
		return super(ModelAdmin,self).show_edit_form(pk)

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

	def get_selected_row_object(self):
		#return the current selected object
		if int(self._list.selected_row_id)<0: return None
		return self._list.value.get(pk=self._list.selected_row_id)


	#################################################################################
	#### PRIVATE FUNCTIONS ##########################################################
	#################################################################################


	def __list_item_selection_changed_event(self):
		obj = self.get_selected_row_object()
		if obj:
			self.object_pk = obj.pk
			self.show_edit_form()
			
	def delete_event(self):
		EditFormAdmin.delete_event(self)
		self.hide_edit_create_form()
		self.populate_list()


	