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

	MODEL 	        = None 	#model to manage
	TITLE 	   		= None	#title of the application
	EDITFORM_CLASS  = EditFormAdmin #edit form class

	INLINES 		= []	#sub models to show in the interface
	LIST_FILTER 	= None	#list of filters fields
	LIST_DISPLAY 	= None  #list of fields to display in the table
	SEARCH_FIELDS 	= None  #fields to be used in the search

	FIELDSETS 		= None  #formset of the edit form
	CONTROL_LIST 	= ControlQueryList #Control to be used in to list the values

	

	def __init__(self, *args, **kwargs):
		"""
		Parameters:
      		title  - Title of the app.
      		model  - Model with the App will represent.
      		parent - Variable with the content [model, foreign key id]. It is used to transform the App in an inline App
		"""
		# buttons
		title = kwargs.get('title', self.TITLE)

		BaseWidget.__init__(self, title)
		self.model 			 = kwargs.get('model', self.MODEL)
		self.editmodel_class = kwargs.get('editform_class', self.EDITFORM_CLASS)
		
		# Set the class to behave as inline ModelAdmin ########
		self.parent_field = None
		self.parent_pk	  = kwargs.get('parent_pk', None)
		self.parent_model = kwargs.get('parent_model', None)
		if self.parent_model and self.parent_pk:
			self.set_parent(self.parent_model, self.parent_pk)
		#######################################################

		self._add_btn 	= ControlButton('<i class="plus icon"></i> Add')
		self._list 		= self.CONTROL_LIST('List')
		self._details   = ControlEmptyWidget('Details')
		
		self.formset    = ['_add_btn', '_list', '_details']
	
		# events
		self._add_btn.include_label = False
		self._add_btn.value 		= self.show_create_form
		self._list.item_selection_changed_event = self.__list_item_selection_changed_event

		self._details.hide()
		
		if self.parent_model:
			self.formset = ['h2:'+str(title)]+self.formset

		self.populate_list()

		
		

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
		self._list.list_display  = self.LIST_DISPLAY  if self.LIST_DISPLAY  else []
		self._list.list_filter 	 = self.LIST_FILTER   if self.LIST_FILTER   else []
		self._list.search_fields = self.SEARCH_FIELDS if self.SEARCH_FIELDS else []
		self._list.value 		 = self.get_queryset()

		
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
			title='Create', 
			model=self.model, 
			inlines=self.INLINES,
			parent_model=self.parent_model,
			parent_pk=self.parent_pk,
			fieldsets=self.FIELDSETS
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
			title='Edit', 
			model=self.model, 
			pk=pk, 
			inlines=self.INLINES,
			parent_model=self.parent_model,
			parent_pk=self.parent_pk,
			fieldsets=self.FIELDSETS
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


	