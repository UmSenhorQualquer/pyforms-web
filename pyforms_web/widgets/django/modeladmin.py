from pyforms_web.basewidget                     import BaseWidget, segment
from pyforms_web.controls.control_button        import ControlButton
from pyforms_web.controls.control_querylist     import ControlQueryList
from pyforms_web.controls.control_emptywidget   import ControlEmptyWidget
from pyforms_web.web.middleware                 import PyFormsMiddleware
from .modelform                                 import ModelFormWidget
from django.db                                  import models

class ModelAdminWidget(BaseWidget):
    """
    The class is used to generate an admin interface for ModelAdmin.MODEL.

    .. code:: python

       from suppliers.models import Suplier

       class SupplierAdminApp(ModelAdminWidget):

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
    LIST_HEADERS    = None  #: list(str): Table columns headers. It will override the LIST_DISPLAY
    LIST_COLS_SIZES = None  #: list(str): Table columns sizes. Should use style units.
    LIST_COLS_ALIGN = None  #: list(str): Table columns alignments. Should use style units.

    SEARCH_FIELDS   = None  #: list(str): Fields to be used in the search

    EXPORT_CSV         = False #: boolean: Flag to activate the export of data to csv. The value of this flag is overwritten by the function has_export_csv_permissions
    EXPORT_CSV_COLUMNS = None #: list(str): List of fields to export to the csv file. By default it will assume the fields in the LIST_DISPLAY variable
    EXPORT_CSV_HEADERS = {} #: dict(str: str): Provide custom header labels to fields listed in EXPORT_CSV_COLUMNS, e.g. {'date': 'Procedure Date'}

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
        title                = kwargs.get('title') if kwargs.get('title', None) else self.TITLE
        self.model           = kwargs.get('model') if kwargs.get('model', None) else self.MODEL
        self.editmodel_class = kwargs.get('editform_class') if kwargs.get('editform_class', None) else self.EDITFORM_CLASS
        self.addmodel_class  = kwargs.get('addform_class', self.ADDFORM_CLASS if self.ADDFORM_CLASS else self.editmodel_class)

        # Set the class to behave as inline ModelAdmin ########
        self.parent_field = None
        self.parent_pk    = kwargs.get('parent_pk',    None)
        self.parent_model = kwargs.get('parent_model', None)

        if self.parent_model and self.parent_pk:
            self.set_parent(self.parent_model, self.parent_pk)

        BaseWidget.__init__(self, title)

        user = PyFormsMiddleware.user()

        #######################################################
        self._list = self.CONTROL_LIST(
            'List',
            headers      = self.LIST_HEADERS  if self.LIST_HEADERS  else None,
            list_display = self.LIST_DISPLAY  if self.LIST_DISPLAY  else [],
            list_filter  = self.LIST_FILTER   if self.LIST_FILTER   else [],
            search_fields= self.SEARCH_FIELDS if self.SEARCH_FIELDS else [],
            rows_per_page= self.LIST_ROWS_PER_PAGE,
            n_pages      = self.LIST_N_PAGES,
            export_csv   = self.has_export_csv_permissions(user),
            export_csv_columns = self.get_export_csv_columns(user),
            export_csv_headers = self.EXPORT_CSV_HEADERS,
            columns_size=self.LIST_COLS_SIZES  if self.LIST_COLS_SIZES  else None,
            columns_align=self.LIST_COLS_ALIGN if self.LIST_COLS_ALIGN else None,
        )

        has_details = self.USE_DETAILS_TO_ADD or self.USE_DETAILS_TO_EDIT
        if has_details:
            self._details = ControlEmptyWidget('Details', visible=False)

        ##############################################
        # Check if the add button should be included
        has_add_permission = self.has_add_permissions() and self.addmodel_class is not None

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
        # force the list to be updated
        self._list.mark_to_update_client()

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


    def get_related_field_queryset(self, request, list_queryset, field, queryset):
        """
        Called to return the main list filters for the ForeignKeys and ManyToMany fields.

        :param django.http.request.HttpRequest request: HttpRequest originating the call of this function.
        :param django.db.models.query.QuerySet list_queryset: Queryset of the main list.
        :param django.db.models.fields.Field field: Related django field.
        :param django.db.models.query.QuerySet queryset: Default queryset for the related field.

        Returns:
            django.db.models.query.QuerySet: Results.
        """
        if hasattr(queryset, 'list_permissions'):
            return queryset.list_permissions(request.user)
        else:
            return queryset


    def hide_form(self):
        """
        Function called to hide the form
        """

        # hide details
        if hasattr(self, '_details'): self._details.hide()

        # show the buttons, only if the they exists:
        toolbar = [self.toolbar] if isinstance(self.toolbar, str) else self.toolbar
        if toolbar:
            for o in toolbar:
                if o and hasattr(self, o):
                    getattr(self, o).show()

        self._list.show()
        self._list.selected_row_id = -1
        self.populate_list()



    def show_create_form(self):
        """
        Show an empty for for creation
        """
        # if there is no add permission then does not show the form
        if not self.has_add_permissions(): return

        params = {
            'title':'Create',
            'model':self.model,
            'parent_model':self.parent_model,
            'parent_pk':self.parent_pk,
            'parent_win': self
        }

        if self.INLINES:   params.update({'inlines':self.INLINES})
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


    def show_edit_form(self, obj_pk=None):
        """
        Show the edition for for a specific object

        :param int obj_pk: Primary key of the object to be show in the edit form.
        """
        obj = self.model.objects.get(pk=obj_pk)
        # if there is no edit permission then does not show the form
        if not self.has_view_permissions(obj): return


        # create the edit form a add it to the empty widget details
        # override the function hide_form to make sure the list is shown after the user close the edition form
        params = {
            'title':'Edit',
            'model':self.model,
            'pk':obj.pk,
            'parent_model':self.parent_model,
            'parent_pk':self.parent_pk,
            'parent_win': self
        }

        if self.INLINES:   params.update({'inlines':  self.INLINES}  )
        if self.FIELDSETS: params.update({'fieldsets':self.FIELDSETS})
        if self.READ_ONLY: params.update({'readonly': self.READ_ONLY})

        editmodel_class = self.get_editmodel_class(obj)
        editform = editmodel_class(**params)

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


    def get_editmodel_class(self, obj):
        """
        Gets the pyforms app to edit the object

        :param django.db.models.Model obj: Object to be edited
        """
        return self.editmodel_class


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
                if issubclass(parent_model, field.related_model):
                    self.parent_field = field
                    break

    def has_add_permissions(self):
        """
        Function called to check if one has permission to add new objects.

        Returns:
            bool: True if has add permission, False otherwise.
        """
        queryset = self.model.objects.all()
        if  hasattr(queryset, 'has_add_permissions'):
            return queryset.has_add_permissions( PyFormsMiddleware.user() )
        else:
            return True


    def has_view_permissions(self, obj):
        """
        Function called to check if one has permission to view the current queryset.

        :param django.db.models.Model obj: object to view.

        Returns:
            bool: True if has view permissions, False otherwise.
        """
        queryset = self.model.objects.filter(pk=obj.pk)
        if  hasattr(queryset, 'has_view_permissions'):
            return queryset.has_view_permissions( PyFormsMiddleware.user() )
        else:
            return True

    def has_remove_permissions(self, obj):
        """
        Function called to check if one has permission to remove the current queryset.

        :param django.db.models.Model obj: object to remove.

        Returns:
            bool: True if has remove permissions, False otherwise.
        """
        return True

    def has_update_permissions(self, obj):
        """
        Function called to check if one has permission to update the current queryset.

        :param django.db.models.Model obj: object to update.

        Returns:
            bool: True if has update permissions, False otherwise.
        """
        return True


    def has_export_csv_permissions(self, user):
        """
        Function called to check if one has permission to export the objects to csv.

        :param django.contrib.auth.models.User: User to check the permission.

        Returns:
            bool: True if has permissions, False otherwise.
        """
        return self.EXPORT_CSV

    def get_export_csv_columns(self, user):
        """
        Function called to get the columns for the csv export.

        :param django.contrib.auth.models.User: User to check the permission.

        Returns:
            list(str): List of columns names.
        """
        return self.EXPORT_CSV_COLUMNS if self.EXPORT_CSV_COLUMNS is not None else self.LIST_DISPLAY


    #################################################################################
    #### PRIVATE FUNCTIONS ##########################################################
    #################################################################################




    def __list_item_selection_changed_event(self):
        """
        Event called when a row is selected. It shows the edition for row.
        """
        obj = self.selected_row_object
        if obj:
            # if the user has edit permission then
            if self.has_view_permissions(obj):
                self.object_pk = obj.pk
                self._list.selected_row_id = None
                self.show_edit_form(obj.pk)
            else:
                raise Exception('You do not have permissions to visualize this record.')


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

        if hasattr(queryset, 'list_permissions'):
            queryset = queryset.list_permissions(request.user)

        if hasattr(self.model, 'get_queryset'):
            queryset = self.model.get_queryset(request, queryset)

        return self.get_queryset(request, queryset)


