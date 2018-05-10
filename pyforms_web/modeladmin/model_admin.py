from pyforms_web.basewidget                         import BaseWidget, segment
from pyforms_web.controls.ControlTextArea           import ControlTextArea
from pyforms_web.controls.ControlText               import ControlText
from pyforms_web.controls.ControlInteger            import ControlInteger
from pyforms_web.controls.ControlFloat              import ControlFloat
from pyforms_web.controls.ControlCombo              import ControlCombo
from pyforms_web.controls.ControlDate               import ControlDate
from pyforms_web.controls.ControlDateTime           import ControlDateTime
from pyforms_web.controls.ControlButton             import ControlButton
from pyforms_web.controls.ControlQueryList          import ControlQueryList
from pyforms_web.controls.ControlMultipleSelection  import ControlMultipleSelection
from pyforms_web.controls.ControlEmptyWidget        import ControlEmptyWidget
from pyforms_web.controls.ControlFileUpload         import ControlFileUpload
from pyforms_web.controls.ControlCheckBox           import ControlCheckBox

from pyforms_web.web.middleware import PyFormsMiddleware
from django.core.exceptions import ValidationError, FieldDoesNotExist
from .utils import get_fieldsets_strings
import traceback
from django.conf import settings
from django.db import models
import os


from .editform_admin import EditFormAdmin

class ModelAdmin(BaseWidget):
    """
    Class used to generate automatically an admin interface for a specific model

    """

    MODEL           = None  #: class: Model to manage
    TITLE           = None  #: str: Title of the application
    EDITFORM_CLASS  = EditFormAdmin #: class: Edit form class

    INLINES         = []    #: list(class): Sub models to show in the interface
    LIST_FILTER     = None  #: list(str): List of filters fields
    LIST_DISPLAY    = None  #: list(str): List of fields to display in the table
    SEARCH_FIELDS   = None  #: list(str): Fields to be used in the search

    FIELDSETS       = None  #: Formset of the edit form
    CONTROL_LIST    = ControlQueryList #: class: Control to be used in to list the values
    READ_ONLY       = []    #: list(str): List of readonly fields 

    LIST_ROWS_PER_PAGE = 10 #: int: number of rows to show per page
    LIST_N_PAGES = 5        #: int: number of pages to show in the list bottom

    #: str: Label of the add button
    ADD_BTN_LABEL = '<i class="plus icon"></i> Add'
    

    def __init__(self, *args, **kwargs):
        """
        :param str title: Title of the app. By default will assume the value in the class variable TITLE.
        :param django.db.models.Model model: Model the App will manages. By default will assume the value in the class variable MODEL.
        :param class editform_class: Class used to generate the edition form. By default will assume the value in the class variable EDITFORM_CLASS.
        :param int parent_pk: (optional) Used to generate the inline interface. Primary key of the parent model
        :param Model parent_model: (optional) Used to generate the inline interface. Parent model
        """
        title                = kwargs.get('title', self.TITLE)
        self.model           = kwargs.get('model', self.MODEL)
        self.editmodel_class = kwargs.get('editform_class', self.EDITFORM_CLASS)
        
        # Set the class to behave as inline ModelAdmin ########
        self.parent_field = None
        self.parent_pk    = kwargs.get('parent_pk',    None)
        self.parent_model = kwargs.get('parent_model', None)
        
        if self.parent_model and self.parent_pk:
            self.set_parent(self.parent_model, self.parent_pk)
        
        has_add_permission = self.has_add_permission()
        has_edit_permission = self.has_edit_permission()

        BaseWidget.__init__(self, title)
        
        #######################################################
        self._list = self.CONTROL_LIST(
            'List',
            list_display = self.LIST_DISPLAY  if self.LIST_DISPLAY  else [],
            list_filter  = self.LIST_FILTER   if self.LIST_FILTER   else [],
            search_fields= self.SEARCH_FIELDS if self.SEARCH_FIELDS else [],
            rows_per_page= self.LIST_ROWS_PER_PAGE,
            n_pages      = self.LIST_N_PAGES
        )

        if has_add_permission or has_edit_permission:
            self._details = ControlEmptyWidget('Details', visible=False)
        
        ##############################################
        # Check if the add button should be included
        if has_add_permission:

            self._add_btn = ControlButton(
                self.ADD_BTN_LABEL,
                label_visible=False,
                default=self.show_create_form
            )
            if self.parent_model: self._add_btn.css = 'tiny basic blue'
        ##############################################

        if self.parent_model:
            self.formset = [
                '_add_btn' if has_add_permission else None,
                '_list',
                '_details' if has_add_permission or has_edit_permission else None,
            ]
        else:
            self.formset = [
                segment( 
                    '_add_btn' if has_add_permission else None,
                    '_list'
                ),
                '_details' if has_add_permission or has_edit_permission else None,
            ]
        
        # if the user has edit permission then 
        if has_add_permission:
            # events
            self._list.item_selection_changed_event = self.__list_item_selection_changed_event

        
        #if it is a inline app, add the title to the header
        
        if self.parent_model:
            self.formset = ['h3:'+str(title)]+self.formset

        self.populate_list()

    #################################################################################
    #### PROPERTIES #################################################################
    #################################################################################

    @property
    def selected_row_object(self):
        """
        django.db.models.Model: Return the current selected row object. If no row is selected return None.
        """
        if int(self._list.selected_row_id)<0: return None
        return self._list.value.get(pk=self._list.selected_row_id)

    #################################################################################
    #### FUNCTIONS ##################################################################
    #################################################################################

    def populate_list(self):
        """
            Function called to configure the CONTROL_LIST to display the data
        """
        self._list.value = self.__get_queryset()


    def get_queryset(self, request, queryset):
        """
            The function retrives the queryset used to polulate the list.
            
            :param django.db.models.query.QuerySet queryset: 
                Default queryset used to populate the list.
                This queryset may have already applied the next filters:
                - If this class is being used as a inline app, the filters to select only the rows related with the parent app are applied. 
                - If the model being managed by this class has a function called get_queryset(request, queryset), the filters applied by this function are applied. (this helps maintaining the visualization rules on the side of the model)

            Returns:
                django.db.models.query.QuerySet: Returns the queryset used to populate the list.
        """
        
        return queryset

    
        
    def hide_form(self):
        """
        Function called to hide the form
        """
        # only if the button exists: 
        # if there is not add permission the add button is not created.
        if hasattr(self, '_add_btn'): self._add_btn.show()
        
        self._list.show()
        self._list.selected_row_id = -1
        self.populate_list()
        self._details.hide()

    def show_create_form(self):
        """
        Show an empty for for creation
        """
        # if there is no add permission then does not show the form
        if not self.has_add_permission(): return
        
        self._add_btn.hide()
        self._list.hide()
        self._details.show()

        createform = self.editmodel_class(
            title='Create', 
            model=self.model, 
            inlines=self.INLINES,
            parent_model=self.parent_model,
            parent_pk=self.parent_pk,
            fieldsets=self.FIELDSETS,
            readonly=self.READ_ONLY,
            parent_win=self
        )

        self._details.value  = createform




    def show_edit_form(self, pk=None):
        """
        Show the edition for for a specific object

        :param int pk: Primary key of the object to edit
        """
        # if there is no edit permission then does not show the form
        if not self.has_edit_permission(): return

        # only if the button exists: 
        # if there is not add permission the add button is not created.
        if hasattr(self, '_add_btn'): self._add_btn.hide()

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
            fieldsets=self.FIELDSETS,
            readonly=self.READ_ONLY,
            parent_listapp=self
        )
        self._details.value = editform
        


    def set_parent(self, parent_model, parent_pk):
        """
        Function called to set prepare the Application to work as an inline
        
        :param django.db.models.Model parent_model: Model of the parent Edition form
        :param int parent_pk: Primary key of the parent object
        """
        
        self.parent_pk      = parent_pk
        self.parent_model   = parent_model

        for field in self.model._meta.get_fields():
            if isinstance(field, models.ForeignKey):
                if parent_model == field.related_model:
                    self.parent_field = field
                    break

    
    def has_add_permission(self):
        """
        Function called to check if one has permission to add new objects.
        
        Returns:
            bool: True if has add permission, False otherwise.
        """
        return True

    def has_edit_permission(self):
        """
        Function called to check if one has permission to edit the objects.
        
        Returns:
            bool: True if has edit permission, False otherwise.
        """
        return True

    #################################################################################
    #### PRIVATE FUNCTIONS ##########################################################
    #################################################################################


    def __list_item_selection_changed_event(self):
        """
        Event called when a row is selected. It shows the edition for row.
        """
        obj = self.selected_row_object
        if obj:
            self.object_pk = obj.pk
            self.show_edit_form(obj.pk)

    def __get_queryset(self):
        """
        
        """
        queryset = self.model.objects.all()

        #used to filter the model for inline fields
        if self.parent_field: 
            queryset = queryset.filter(**{self.parent_field.name: self.parent_pk})

        # check if the model has a query_set function
        # if so use it to get the data for visualization
        request  = PyFormsMiddleware.get_request()

        if hasattr(self.model, 'get_queryset'):
            queryset = self.model.get_queryset(request, queryset)
        
        return self.get_queryset(request, queryset)


    