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

class ModelAdmin(BaseWidget):

	inlines 	 = []
	list_filter  = None
	list_display = None
	search_fields= None
	
	fieldsets	 = None

	list_control = ControlQueryList

	def __init__(self, title, model, parent=None, editmodel_class=EditFormAdmin):
		"""
		Parameters:
      		title  - Title of the app.
      		model  - Model with the App will represent.
      		parent - Variable with the content [model, foreign key id]. It is used to transform the App in an inline App
		"""
		# buttons
		BaseWidget.__init__(self, title)
		self.model 		  = model
		self.parent_pk	  = None
		self.parent_field = None
		self.parent_model = None
		self.editmodel_class = editmodel_class
		
		if parent: self.set_parent(parent[0], parent[1])

		self._add_btn 	= ControlButton('<i class="plus icon"></i> Add')
		self._list 		= self.list_control('List')
		self._details   = ControlEmptyWidget('Details')
		
		self.formset = ['_add_btn', '_list', '_details']
	
		# events
		self._add_btn.include_label = False
		self._add_btn.value 		= self.show_create_form
		self._list.item_selection_changed_event = self.__list_item_selection_changed_event

		self.populate_list()

		self._details.hide()
		
		if self.parent_model:
			self.formset = ['h2:'+title]+self.formset
		
		

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
		self._list.list_display  = self.list_display  if self.list_display  else []
		self._list.list_filter 	 = self.list_filter   if self.list_filter   else []
		self._list.search_fields = self.search_fields if self.search_fields else []
		query					 = self.get_queryset()
		self._list.value 		 = query

		
	def hide_form(self):
		self._add_btn.show()
		self._list.show()
		self._list.selected_row_id = -1
		self.populate_list()
		self._details.hide()

	def show_create_form(self):
		
		self._add_btn.hide()
		self._list.hide()
		self._details.show()

		createform = self.editmodel_class(
			'Create', 
			self.model, 
			None, 
			inlines=self.inlines,
			parent_model=((self.parent_model, self.parent_pk) if self.parent_model is not None else None),
			fieldsets = self.fieldsets
		)
		createform.hide_form = self.hide_form
		self._details.value  = createform


	def show_edit_form(self, pk=None):
		
		self._add_btn.hide()
		self._list.hide()		
		self._details.show()
		
	
		# create the edit form a add it to the empty widget details
		# override the function hide_form to make sure the list is shown after the user close the edition form
		editform = self.editmodel_class(
			'Edit', 
			self.model, 
			pk, 
			inlines=self.inlines, 
			parent_model=((self.parent_model, self.parent_pk) if self.parent_model is not None else None),
			fieldsets = self.fieldsets if hasattr(self, 'fieldsets') else None
		)
		
		editform.hide_form 	= self.hide_form
		self._details.value = editform
		
	def set_parent(self, parent_model, parent_pk):
		self.parent_pk 		= parent_pk
		self.parent_model 	= parent_model

		for field in self.model._meta.get_fields():
			if isinstance(field, models.ForeignKey):
				if parent_model == field.related_model:
					self.parent_field = field
					break

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
			self.show_edit_form(obj.pk)


	