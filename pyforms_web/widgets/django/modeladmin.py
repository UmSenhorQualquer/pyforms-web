from pyforms_web.basewidget                         import BaseWidget, segment
from pyforms_web.controls.control_textarea           import ControlTextArea
from pyforms_web.controls.control_text               import ControlText
from pyforms_web.controls.control_integer            import ControlInteger
from pyforms_web.controls.control_float              import ControlFloat
from pyforms_web.controls.control_combo              import ControlCombo
from pyforms_web.controls.control_date               import ControlDate
from pyforms_web.controls.control_datetime           import ControlDateTime
from pyforms_web.controls.control_button             import ControlButton
from pyforms_web.controls.control_querylist          import ControlQueryList
from pyforms_web.controls.control_multipleselection  import ControlMultipleSelection
from pyforms_web.controls.control_emptywidget        import ControlEmptyWidget
from pyforms_web.controls.control_fileupload         import ControlFileUpload
from pyforms_web.controls.control_checkbox           import ControlCheckBox


from pyforms_web.web.middleware import PyFormsMiddleware
from django.core.exceptions import ValidationError, FieldDoesNotExist
from .utils import get_fieldsets_strings
import traceback
from django.conf import settings
from django.db import models
import os


from .modelform import ModelFormWidget

class ModelAdminWidget(BaseWidget):
    """
    The class is used to generate an admin interface for ModelAdmin.MODEL.

    .. code:: python

       from suppliers.models import Suplier

       class SupplierAdminApp(ModelAdmin):

            MODEL = Supplier
            TITLE = 'Suppliers'
    """

    MODEL           = None  #: class: Model to manage
    TITLE           = None  #: str: Title of the application
    EDITFORM_CLASS  = ModelFormWidget #: class: Edit form class
    ADDFORM_CLASS   = None #: class: Create form class

    USE_DETAILS_TO_ADD  = True #: boolean: Use the flag to create the ControlEmptyWidget self._details. This control is used to load the ADDFORM_CLASS.
    USE_DETAILS_TO_EDIT = True #: boolean: Use the flag to create the ControlEmptyWidget self._details. This control is used to load the EDITFORM_CLASS.

    INLINES         = []    #: list(class): Sub models to show in the interface
    LIST_FILTER     = None  #: list(str): List of filters fields
    LIST_DISPLAY    = None  #: list(str): List of fields to display in the table
    SEARCH_FIELDS   = None  #: list(str): Fields to be used in the search

    CONTROL_LIST    = ControlQueryList #: class: Control to be used in to list the values
    FIELDSETS       = None  #: Formset of the edit form
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
        self.addmodel_class  = kwargs.get('addform_class', self.ADDFORM_CLASS if self.ADDFORM_CLASS else self.editmodel_class)
        
        # Set the class to behave as inline ModelAdmin ########
        self.parent_field = None
        self.parent_pk    = kwargs.get('parent_pk',    None)
        self.parent_model = kwargs.get('parent_model', None)
        
        if self.parent_model and self.parent_pk:
            self.set_parent(self.parent_model, self.parent_pk)
        
        has_add_permission  = self.has_add_permission()  and self.addmodel_class  is not None
        has_edit_permission = self.has_edit_permission() and self.editmodel_class is not None

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

        has_details = (self.USE_DETAILS_TO_ADD or self.USE_DETAILS_TO_EDIT) and (has_add_permission or has_edit_permission)
        if has_details:
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

        self.toolbar = self.get_toolbar_buttons(has_add_permission=has_add_permission)

        if self.parent_model:
            self.formset = [
                self.toolbar,
                '_details' if has_details else None,
                '_list',
            ]
        else:
            self.formset = [
                '_details' if has_details else None,
                segment( 
                    self.toolbar,
                    '_list'
                ),
            ]
        
        # if the user has edit permission then 
        if has_edit_permission:
            # events
            self._list.item_selection_changed_event = self.__list_item_selection_changed_event

        
        #if it is a inline app, add the title to the header
        
        if self.parent_model and self.title:
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

    def get_toolbar_buttons(self, has_add_permission=False):
        """
        This function generate the formset configuration for the top buttons,

        Returns:
            list(str): Returns the formset configuration that will be append to
            the end of the fieldsets.
        """
        return '_add_btn' if has_add_permission else None

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
        toolbar = [self.toolbar] if isinstance(self.toolbar, str) else self.toolbar
        if toolbar:
            for o in toolbar:
                if o and hasattr(self, o):
                    getattr(self, o).show()
        
        self._list.show()
        self._list.selected_row_id = -1
        self.populate_list()
        
        if hasattr(self, '_details'): 
            self._details.hide()

    def show_create_form(self):
        """
        Show an empty for for creation
        """
        # if there is no add permission then does not show the form
        if not self.has_add_permission(): return

        params = {
            'title':'Create', 
            'model':self.model, 
            'parent_model':self.parent_model,
            'parent_pk':self.parent_pk,
            'parent_win': self
        }

        if self.INLINES: params.update({'inlines':self.INLINES})
        if self.FIELDSETS: params.update({'fieldsets':self.FIELDSETS})
        if self.READ_ONLY: params.update({'readonly':self.READ_ONLY})

        createform = self.addmodel_class(**params)

        if hasattr(self, '_details') and self.USE_DETAILS_TO_ADD:
            self._list.hide()
            self._details.show()
            self._details.value = createform
            toolbar = [self.toolbar] if isinstance(self.toolbar, str) else self.toolbar
            if toolbar:
                for o in toolbar:
                    if o and hasattr(self, o):
                        getattr(self, o).hide()
        else:
            self._list.show()
            if hasattr(self, '_details'): 
                self._details.hide()


    def show_edit_form(self, pk=None):
        """
        Show the edition for for a specific object

        :param int pk: Primary key of the object to edit
        """
        # if there is no edit permission then does not show the form
        if not self.has_edit_permission(): return

        
        # create the edit form a add it to the empty widget details
        # override the function hide_form to make sure the list is shown after the user close the edition form
        params = {
            'title':'Edit', 
            'model':self.model, 
            'pk':pk,
            'parent_model':self.parent_model,
            'parent_pk':self.parent_pk,
            'parent_win': self
        }

        if self.INLINES:   params.update({'inlines':  self.INLINES}  )
        if self.FIELDSETS: params.update({'fieldsets':self.FIELDSETS})
        if self.READ_ONLY: params.update({'readonly': self.READ_ONLY})

        editform = self.editmodel_class(**params)

        if hasattr(self, '_details') and self.USE_DETAILS_TO_EDIT: 
            self._details.value = editform
            self._list.hide()
            self._details.show()

            # only if the button exists: 
            toolbar = [self.toolbar] if isinstance(self.toolbar, str) else self.toolbar
            if toolbar:
                for o in toolbar:
                    if o and hasattr(self, o): getattr(self, o).hide()

        else:
            self._list.show()
            if hasattr(self, '_details'): 
                self._details.hide()



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
            self._list.selected_row_id = None
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


    