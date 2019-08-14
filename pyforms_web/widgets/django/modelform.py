from pyforms_web.basewidget                         import BaseWidget, no_columns
from pyforms_web.controls.control_textarea           import ControlTextArea
from pyforms_web.controls.control_text               import ControlText
from pyforms_web.controls.control_integer            import ControlInteger
from pyforms_web.controls.control_float              import ControlFloat
from pyforms_web.controls.control_decimal            import ControlDecimal
from pyforms_web.controls.control_combo              import ControlCombo
from pyforms_web.controls.control_autocomplete       import ControlAutoComplete
from pyforms_web.controls.control_date               import ControlDate
from pyforms_web.controls.control_datetime           import ControlDateTime
from pyforms_web.controls.control_button             import ControlButton
from pyforms_web.controls.control_emptywidget        import ControlEmptyWidget
from pyforms_web.controls.control_fileupload         import ControlFileUpload
from pyforms_web.controls.control_checkbox           import ControlCheckBox
from pyforms_web.web.middleware import PyFormsMiddleware
from django.core.exceptions import ValidationError, FieldDoesNotExist, NON_FIELD_ERRORS
from .utils import get_fieldsets_strings
import traceback
from django.conf import settings
from django.db import models
import os
from confapp import conf

from pyforms_web.utils import get_lookup_verbose_name

import datetime
from django.utils import timezone



class ModelFormWidget(BaseWidget):
    """
    When a Pyforms application inherit from this class a form for the model ModelFormWidget.MODEL is created.

    **Usage example:**

    .. code:: python

       from funding.models import FundingOpportunity

       class EditFundingOpportunitiesApp(ModelFormWidget):

            TITLE = "Edit opportunities"
            MODEL = FundingOpportunity

            FIELDSETS = [
                'h2:Opportunity details',
                segment([
                    ('subject','fundingopportunity_published','fundingopportunity_rolling'),
                    ('fundingopportunity_name','fundingopportunity_end'),
                    ('_loi','fundingopportunity_loideadline', 'fundingopportunity_fullproposal'),
                    ('fundingopportunity_link','topics'),
                ]),
                'h2:Financing info',
                segment([
                    ('financingAgency','currency','paymentfrequency'),
                    ('fundingtype','fundingopportunity_value','fundingopportunity_duration'),
                ]),
                'h2:Description',
                segment([
                    'fundingopportunity_eligibility',
                    'fundingopportunity_scope',
                    'fundingopportunity_brifdesc',
                ])
            ]
    """
    MODEL             = None  #: class: Model to manage
    TITLE             = None  #: str: Title of the application
    INLINES           = []    #: list(class): Sub models to show in the interface
    FIELDSETS         = None  #: Formset of the edit form
    READ_ONLY         = []    #: list(str): List of readonly fields

    #: bool: Flag to show or hide the cancel button
    HAS_CANCEL_BTN_ON_EDIT = True
    #: bool: Flag to show or hide the cancel button
    HAS_CANCEL_BTN_ON_ADD  = True

    #: bool: Close the application on remove
    CLOSE_ON_REMOVE = False
    #: bool: Close the application on cancel
    CLOSE_ON_CANCEL = False

    #: bool: Call populate_list function of the parent application when object is saved, updated or deleted
    POPULATE_PARENT = True

    #: str: Label for the save button
    SAVE_BTN_LABEL     = '<i class="save icon"></i> Save'
    #: str: Label for the create button
    CREATE_BTN_LABEL   = '<i class="plus icon"></i> Create'
    #: str: Label for the cancel button
    CANCEL_BTN_LABEL   = '<i class="hide icon"></i> Close'
    #: str: Label for the delete button
    REMOVE_BTN_LABEL   = '<i class="trash alternate outline icon"></i> Remove'
    #: str: Label for the popup window for the delete confirmation
    POPUP_REMOVE_TITLE = 'The next objects are going to be affected or removed'

    def __init__(self, *args, **kwargs):
        """
        :param str title: Title of the app. By default will assume the value in the class variable TITLE.
        :param django.db.models.Model model: Model with the App will represent. By default will assume the value in the class variable MODEL.
        :param list(ModelAdminWidget) inlines: Sub models to show in the interface
        :param list(str) fieldsets: Organization of the fields
        :param int parent_pk: Parent model key
        :param django.db.models.Model parent_model: Parent model class
        :param int pk: Model register to manage
        """
        title = kwargs.get('title') if kwargs.get('title', None) else self.TITLE

        self.object_pk = kwargs.get('pk', None)
        self.model     = kwargs.get('model', self.MODEL)

        BaseWidget.__init__(self, *args, **kwargs )

        self.update_permissions_variables()

        if self.object_pk:
            if not self._has_view_permissions:
                self.formset = ['alert:No permissions']
                return
        else:
            if not self._has_add_permissions:
                self.formset = ['alert:No permissions']
                return


        self.fieldsets = self.get_fieldsets(kwargs.get('fieldsets',  self.FIELDSETS))
        self.readonly  = self.get_readonly(kwargs.get('readonly',  self.READ_ONLY))
        self.has_cancel_btn = kwargs.get('has_cancel_btn',  self.HAS_CANCEL_BTN_ON_ADD if self.object_pk is None else self.HAS_CANCEL_BTN_ON_EDIT)

        self.inlines = self.INLINES if len(self.INLINES)>0 else kwargs.get('inlines', self.INLINES)

        if self.fieldsets is None: self.fieldsets = self.FIELDSETS

        self._auto_fields          = []
        self._callable_fields      = []
        self.edit_fields           = []
        self.edit_buttons          = []
        self.inlines_apps          = []
        self.inlines_controls_name = []
        self.inlines_controls      = []

        # used to configure the interface to inline
        # it will filter the dataset by the foreign key
        self.parent_field = None
        self.parent_pk    = kwargs.get('parent_pk', None)
        self.parent_model = kwargs.get('parent_model', None)

        if self.parent_model and self.parent_pk:
            self.__set_parent(self.parent_model, self.parent_pk)
        #######################################################

        # Create the edit buttons buttons #####################

        if self._has_update_permissions:
            self._save_btn   = ControlButton(self.SAVE_BTN_LABEL, label_visible=False, default=self.save_btn_event)
            self.edit_buttons.append( self._save_btn )

        if self._has_add_permissions:
            self._create_btn = ControlButton(self.CREATE_BTN_LABEL, label_visible=False, default=self.__create_btn_event)
            self.edit_buttons.append( self._create_btn )

        if self._has_remove_permissions:
            self._remove_btn = ControlButton(self.REMOVE_BTN_LABEL,  css='red basic', label_visible=False, default=self.__remove_btn_event)
            self.edit_buttons.append( self._remove_btn )

        if self.has_cancel_btn:
            self._cancel_btn = ControlButton(self.CANCEL_BTN_LABEL, css='gray basic', label_visible=False, default=self.cancel_btn_event)
            self.edit_buttons.append( self._cancel_btn )

        self.edit_fields += self.edit_buttons
        #######################################################

        # In case the edition form is being used as inline ####
        # set the buttons for tiny size #######################
        if self.parent_model:
            for btn in self.edit_buttons: btn.css +=' tiny'
        #######################################################

        self.create_model_formfields()

        if self.object_pk:
            self.show_edit_form(pk=self.object_pk)
        else:
            self.show_create_form()



    #################################################################################
    #### PROPERTIES #################################################################
    #################################################################################

    @property
    def model_object(self):
        """
        django.db.models.Model object: Return the current object in edition.
        """

        if self.object_pk is None:
            return None
        else:
            queryset = self.model.objects.all()

            # check if the model has a query_set function
            # if so use it to get the data for visualization
            if hasattr(self.model, 'get_queryset'):
                request  = PyFormsMiddleware.get_request()
                queryset = self.model.get_queryset(request, queryset)

            try:
                return queryset.get(pk=self.object_pk)
            except self.model.DoesNotExist:
                return None

    #################################################################################
    #### FUNCTIONS ##################################################################
    #################################################################################

    def update_permissions_variables(self):
        if self.object_pk:
            self._has_update_permissions = self.has_update_permissions()
        else:
            self._has_update_permissions = False

        self._has_add_permissions = self.has_add_permissions()
        self._has_view_permissions = self.has_view_permissions()

        if self.object_pk:
            self._has_remove_permissions = self.has_remove_permissions()
        else:
            self._has_remove_permissions = False

    def get_readonly(self, default):
        """
        The function returns the readonly fields to be set in the form.

        :param list(str) default: Default readonly configuration.

        Returns:
            list(str): Read only fields. Check class variable READ_ONLY to know more about it.
        """
        return default

    def get_fieldsets(self, default):
        """
        The function returns the fieldsets organization to be set in the form.

        :param list(str) default: Default fieldsets configuration.

        Returns:
            list(str): fieldsets. Check class variable FIELDSETS to know more about it.
        """
        return default

    def get_buttons_row(self):
        """
        This function generate the formset configuration for the save, create,
        cancel and remove buttons,

        Returns:
            list(str): Returns the formset configuration that will be append to
            the end of the fieldsets.
        """
        buttons = []
        if self._has_update_permissions:   buttons.append('_save_btn')
        if self._has_add_permissions:      buttons.append('_create_btn')
        if self.has_cancel_btn:            buttons.append('_cancel_btn')
        if self._has_remove_permissions:   buttons.append('_remove_btn')
        return [no_columns(*buttons)]


    def hide_form(self):
        """
        This functions hides the create and edit form.
        """
        if self.parent and hasattr(self.parent, 'hide_form'):
            self.parent.hide_form()
        else:
            for field in self.edit_fields:      field.hide()
            for field in self.inlines_controls: field.hide()

    def show_form(self):
        """
        This shows the create and edit form.
        """
        for field in self.edit_fields:      field.show()
        for field in self.inlines_controls: field.show()

    def cancel_btn_event(self):
        """
        Event called when the cancel button is pressed
        """

        # for orquestra
        try:
            if self.LAYOUT_POSITION in [conf.ORQUESTRA_NEW_WINDOW,conf.ORQUESTRA_NEW_TAB]:
                self.close()
        except:
            pass

        # close the application on cancel
        if self.CLOSE_ON_CANCEL:
            self.close()
        # the application has a ModelAdmin app as parent. Call parent hide_form
        elif hasattr(self.parent, 'hide_form'):
            self.parent.hide_form()




    def autocomplete_search(self, queryset, keyword, control):
        """
        Function used by a combobox to get the items dynamically

        :param django.db.models.query.QuerySet queryset: Queryset from where to filter the results
        :param str keyword: Keyword for filter the results
        :param pyforms.controls.BaseControl: Control calling the autocomplete

        Returns:
            django.db.models.query.QuerySet: Queryset used to update the autocomplete control
        """
        field = self.model._meta.get_field(control.name)
        queryset = self.get_related_field_queryset(field, queryset)

        return queryset


    def get_related_field_queryset(self, field, queryset):
        """
        Function called to manages the query for related fields like ForeignKeys and ManyToMany.

        :param django.db.models.fields.Field field: Related django field.
        :param django.db.models.query.QuerySet queryset: Default queryset for the related field.

        Returns:
            django.db.models.query.QuerySet: Results for the search in the format.
        """
        return queryset

    def update_related_field(self, field, pyforms_field, queryset):
        """
        Function called update the related fields like ForeignKeys and ManyToMany.

        :param django.db.models.fields.Field field: Related django field.
        :param ControlBase pyforms_field: Pyforms field that will be updated.
        :param django.db.models.query.QuerySet queryset: Default queryset for the related field.
        """
        pass

        """
        if isinstance(field, models.ForeignKey):
            pass
            #Foreign key
            #pyforms_field.clear_items()
            #if field.null:
            #    pyforms_field.add_item( '', '-1' )
            #for instance in query:
            #    pyforms_field.add_item( str(instance), instance.pk )

        elif isinstance(field, models.ManyToManyField):
            #Many to Many field
            #pyforms_field.queryset = query
            pass
        """



    def show_create_form(self):
        """
        This function prepares the fields to be shown as create form.
        """

        #check if it has permissions to add new registers
        if not self._has_add_permissions:
            raise Exception('Your user does not have permissions to add')

        fields2show = self.get_visible_fields_names()

        self.__update_related_fields()

        # clear all the fields present in the model
        for field_name in fields2show:
            if hasattr(self, field_name):
                try:
                    field = self.model._meta.get_field(field_name)
                    pyforms_field = getattr(self, field_name)

                    if not hasattr(field, 'default') or field.default==models.fields.NOT_PROVIDED:
                        pyforms_field.value = None

                    elif callable(field.default):
                        pyforms_field.value = field.default()

                    elif isinstance(field, models.DecimalField) and type(field).__name__ == 'MoneyField':
                        pyforms_field.value = field.default.amount
                    else:
                        pyforms_field.value = field.default

                    if field.get_internal_type() in ('CharField', 'TextField') and field.blank:
                        pyforms_field.value = ''
                except FieldDoesNotExist:
                    pass

        for field in self.edit_fields: field.show()

        for inline in self.inlines_controls:
            inline.hide()

        if self._has_update_permissions: self._save_btn.hide()
        if self._has_remove_permissions: self._remove_btn.hide()

    def update_callable_fields(self):
        """
        Update the callable fields after the form is saved.
        """
        if not self._callable_fields: return

        obj = self.model_object
        if obj is None: return
        for field_name in self._callable_fields:
            pyforms_field       = getattr(self, field_name)
            value               = getattr(obj,  field_name)()
            pyforms_field.value = value

    def update_autonumber_fields(self):
        """
        Update the auto number fields after the form is saved.
        """
        if not self._auto_fields: return

        obj = self.model_object
        if obj is None: return
        for field_name in self._auto_fields:
            pyforms_field       = getattr(self, field_name)
            value               = getattr(obj,  field_name)
            pyforms_field.value = value


    def show_edit_form(self, pk=None):
        """
        This function prepares the fields to be shown as edit form.

        :param int pk: Primary key of the object to be show in the edit form.

        Returns:
            :django.db.models.Model object: Returns the object in edition.
        """

        if  pk: self.object_pk = pk

        if not self._has_view_permissions:
            raise Exception('Your user does not have permissions to save')


        for field in self.edit_fields:      field.show()
        for field in self.inlines_controls: field.show()
        if self._has_add_permissions:      self._create_btn.hide()

        self.__update_related_fields()

        obj = self.model_object
        fields2show = self.get_visible_fields_names()

        for field_name in fields2show:

            if hasattr(self, field_name) and hasattr(obj,  field_name):
                pyforms_field   = getattr(self, field_name)
                value           = getattr(obj,  field_name)

                try:
                    field = self.model._meta.get_field(field_name)
                except FieldDoesNotExist:
                    try:
                        field = getattr(self.model, field_name)
                    except AttributeError:
                        continue

                if callable(field) and not isinstance(field, models.Model):
                    pyforms_field.value = value()

                elif field_name in self.readonly:

                    if isinstance(field, models.ManyToManyField):
                        pyforms_field.value = ';'.join([str(o) for o in value.all()])

                    elif isinstance(value, datetime.datetime ):
                        if not value:
                            pyforms_field.value = ''
                        else:
                            value = timezone.localtime(value)
                            pyforms_field.value = value.strftime('%Y-%m-%d %H:%M')

                    elif isinstance(value, datetime.date ):
                        if not value:
                            pyforms_field.value = ''
                        else:
                            pyforms_field.value = value.strftime('%Y-%m-%d')

                    else:
                        if field.choices:
                            for v, l in field.choices:
                                if v==value:
                                    pyforms_field.value = l
                                    break
                        else:
                            pyforms_field.value = value

                elif isinstance(field, models.DecimalField) and type(field).__name__ == 'MoneyField':
                    # support django-money MoneyField
                    pyforms_field.value = value.amount

                elif isinstance(field, models.AutoField):
                    pyforms_field.value = value

                elif isinstance(field, models.FileField):
                    pyforms_field.value = value.url if value else None

                elif isinstance(field, models.ImageField):
                    pyforms_field.value = value.url if value else None

                elif isinstance(field, models.ForeignKey):
                    pyforms_field.value = value.pk if value else None

                elif isinstance(field, models.ManyToManyField):
                    pyforms_field.value = [str(o.pk) for o in value.all()]

                else:
                    pyforms_field.value = value

        self.inlines_apps = []
        for inline in self.inlines:
            pyforms_field = getattr(self, inline.__name__)
            pyforms_field._name = inline.__name__
            app = inline(parent_model=self.model, parent_pk=self.object_pk)
            self.inlines_apps.append(app)
            pyforms_field.value = app
            pyforms_field.show()

        self.update_permissions_variables()

        if hasattr(self, '_save_btn'):
            if self._has_update_permissions:
                self._save_btn.show()
            else:
                self._save_btn.hide()

        if hasattr(self, '_remove_btn'):
            if self._has_remove_permissions:
                self._remove_btn.show()
            else:
                self._remove_btn.hide()

        return obj


    def delete_event(self):
        """
        Function called to delete the current object in edition.

        Returns:
            :bool: True if the object was deleted with success, False if not.
        """
        if self.object_pk:
            obj = self.model_object
            obj.delete()
            self.object_pk = None
            if self._has_remove_permissions: self._remove_btn.hide()
            if self._has_add_permissions:    self._create_btn.show()
            if self._has_update_permissions: self._save_btn.hide()
            for field in self.inlines_controls: field.hide()
            if self.parent: self.parent.populate_list()
            return True
        else:
            return False

    def popup_remove_handler(self, popup=None, button=None):
        """
        Function that handles the buttons events of the object delete confirmation popup.

        :param BaseWidget popup: Popup application.
        :param str button: Label of the pressed button.
        """
        if button==self.CANCEL_BTN_LABEL:
            popup.close()
        elif button==self.REMOVE_BTN_LABEL:
            if self.delete_event():
                self.success('The object was deleted with success!','Success!')
                popup.close()
                if self.CLOSE_ON_REMOVE: self.close()
            else:
                popup.warning('The object was not deleted!','Warning!')






    def create_newobject(self):
        """
        Function called to create a new object of the model.

        Returns:
            :django.db.models.Model object: Created object
        """
        return self.model()

    def save_object(self, obj, **kwargs):
        """
        Function called to save the object
        It validates the form fields values.


        :param django.db.models.Model obj: Object to save.
        :param dict kwargs: Any named argument passed to this function will be passed to the Model save method. Example: Model.save(**kwargs).
        """

        ### validate form values
        obj.save(**kwargs)
        return obj






    def validate_object(self, obj):
        """
        Function called the model object

        :param django.db.models.Model obj: Object to validate.

        Returns:
            :django.db.models.Model object: Created object or None if the object was not saved with success.
        """

        # Validate the object
        try:

            obj.full_clean()

        except ValidationError as e:

            obj = None

            # Found errors, the object was not saved
            html = '<ul class="list">'
            for field_name, messages in e.message_dict.items():

                try:
                    if hasattr(self, field_name):
                        getattr(self, field_name).error = True
                        label = get_lookup_verbose_name(self.model, field_name)
                        html += '<li><b>{0}</b>'.format(label)
                        field_error = True
                    elif field_name==NON_FIELD_ERRORS:
                        field_error = False
                    else:
                        html += '<li><b>{0}</b>'.format(field_name)
                        field_error = True

                except FieldDoesNotExist:
                    field_error = False

                if field_error: html += '<ul>'
                for msg in messages: html += '<li>{0}</li>'.format(msg)
                if field_error: html += '</ul></li>'

            html+= '</ul>'
            raise Exception(html)

        return obj


    def update_object_fields(self, obj):
        """
        Update the obj fields values with the form inputs values

        :param django.db.models.Model obj: Object to update the values.

        Returns:
            :django.db.models.Model: Updated object.
        """

        # if it is working as an inline edition form #
        if self.parent_field:
            setattr(obj,
                self.parent_field.name,
                self.parent_model.objects.get(pk=self.parent_pk)
            )

        fields2show = self.get_visible_fields_names()

        for field in self.model._meta.get_fields():
            # ignore fields that are not in the formset
            if field.name not in fields2show: continue
            # ignore read only fields
            if field.name in self.readonly:   continue

            pyforms_field = getattr(self, field.name)
            value         = pyforms_field.value


            # if AutoField
            if   isinstance(field, models.AutoField):
                continue

            # if FileField
            elif isinstance(field, models.FileField):
                getattr(self, field.name).error = False

                # get the temporary path of the file
                tmp_filepath = getattr(self, field.name).value

                if tmp_filepath:
                    # get the temporary filename
                    tmp_filename = os.path.basename(tmp_filepath)

                    # in case the upload_to is callable get
                    if callable(field.upload_to):
                        # in the case the upload_to property it is a function
                        filepath = field.upload_to(obj, tmp_filename)
                        filename = os.path.basename(filepath)
                        dirpath  = os.path.dirname(filepath)
                    else:
                        dirpath = field.upload_to
                        filename = tmp_filename

                    try:
                        os.makedirs(os.path.join(settings.MEDIA_ROOT, dirpath))
                    except os.error as e:
                        pass

                    paths     = [p for p in value.split(os.path.sep) if len(p)>0][1:]
                    from_path = os.path.join(settings.MEDIA_ROOT,*paths)

                    if os.path.exists(from_path):
                        to_path = os.path.join(settings.MEDIA_ROOT, dirpath, filename)
                        os.rename(from_path, to_path)

                        url = '/'.join([dirpath]+[filename])
                        if url[0]=='/': url = url[1:]
                        setattr(obj, field.name, url)
                elif field.null:
                    setattr(obj, field.name, None)
                else:
                    setattr(obj, field.name, '')

            # if ForeignKey
            elif isinstance(field, models.ForeignKey):
                if value is not None:
                    try:
                        value = field.related_model.objects.get(pk=value)
                    except:
                        self.alert(
                            'The field [{0}] has an error.'.format(field.verbose_name)
                        )
                        pyforms_field.error = True
                else:
                    value = None

                setattr(obj, field.name, value)

            elif obj.pk and isinstance(field, models.ManyToManyField):
                pyforms_field.error = False
                getattr(obj, field.name).set([] if value is None else value)

            # all other fields except the ManyToManyField
            elif not isinstance(field, models.ManyToManyField):
                pyforms_field.error = False

                if isinstance(field, models.CharField) and value is None and field.null is False:
                    value = ''

                if value == '' and field.null:
                    value = None

                setattr(obj, field.name, value)

        return obj

    def save_related_fields(self, obj):
        """
        Save related fields

        :param django.db.models.Model obj: Parent object to save.

        Returns:
            :django.db.models.Mode: Object passed as parameter
        """
        for field in self.model._meta.get_fields():

            if isinstance(field, models.ManyToManyField) and hasattr(self, field.name):
                values          = getattr(self, field.name).value
                field_instance  = getattr(obj, field.name)

                field_instance.set([] if values is None else values)

        return obj


    def save_form_event(self, obj):
        """
        Function handling the form save.
        This function, updates the obj with the form values,
        validate the obj fields, and call the save_event function.

        :param django.db.models.Model obj: Model object used for the save.

        Returns:
            :boolean: It returns True or False if the save was successfully.
        """
        user = PyFormsMiddleware.user()

        # decides if an object is going to be created or updated
        new_object = obj.pk is None

        try:
            obj = self.update_object_fields(obj)
            obj = self.validate_object(obj)
            return self.save_event(obj, new_object)
        except Exception as e:
            traceback.print_exc()
            self.alert(str(e))
            return False

    def save_event(self, obj, new_object):
        """
        Function handling the form save.
        This function, updates the obj with the form values,
        validate the obj fields, and call the save_event function.

        :param django.db.models.Model obj: Model object used for the save.

        Returns:
            :boolean: It returns True or False if the save was successfully.
        """

        obj = self.save_object(obj)
        obj = self.save_related_fields(obj)

        self.object_pk = obj.pk
        self.update_callable_fields()
        self.update_autonumber_fields()

        # Add object mode
        if new_object:

            if self.parent and obj:
                # it is being use from a ModelAdminWidget

                # update the parent list
                if self.POPULATE_PARENT: self.parent.populate_list()

                self.cancel_btn_event()
                self.parent.show_edit_form(obj.pk)
                self.parent.success('The object <b>{0}</b> was saved with success!'.format(obj),'Success!')

            elif obj:
                # it is executing as a single app
                if self._has_add_permissions:    self._create_btn.hide()
                if self._has_update_permissions: self._save_btn.show()
                if self._has_remove_permissions: self._remove_btn.show()

                self.inlines_apps = []
                for inline in self.inlines:
                    pyforms_field       = getattr(self, inline.__name__)
                    pyforms_field._name = inline.__name__
                    app = inline(
                        parent_model=self.model,
                        parent_pk=self.object_pk
                    )
                    self.inlines_apps.append(app)
                    pyforms_field.value = app
                    pyforms_field.show()

                self.success('The object <b>{0}</b> was saved with success!'.format(obj),'Success!')

        # Update object mode
        else:

            if obj:
                self.success('The object <b>{0}</b> was saved with success!'.format(obj),'Success!')

                # update the parent list
                if self.POPULATE_PARENT and self.parent:
                    self.parent.populate_list()

        for inline in self.inlines_apps:
            inline.populate_list()

        return True










    #################################################################################
    #### PRIVATE FUNCTIONS ##########################################################
    #################################################################################

    def __set_parent(self, parent_model, parent_pk):
        """
        Set the form to work as inline

        :param django.db.models.Model parent_model: Parent model.
        :param int parent_pk: Parent object primary key.
        """
        self.parent_pk    = parent_pk
        self.parent_model = parent_model

        for field in self.model._meta.get_fields():
            if isinstance(field, models.ForeignKey):
                if issubclass(parent_model, field.related_model):
                    self.parent_field = field
                    break



    def get_visible_fields_names(self):
        """
        Function called to get names of the visible fields.

        Returns:
            :list(str): List names of the visible fields.
        """
        if self.fieldsets:
            fields = get_fieldsets_strings(self.fieldsets)
        else:
            fields = []
            for field in self.model._meta.get_fields():

                if field.one_to_many: continue
                if field.one_to_one and field.name.endswith('_ptr'): continue

                fields.append(field.name)

        if self.parent_field:
            try:
                fields.remove(self.parent_field.name)
            except ValueError: pass

        return [field for field in fields if field is not None]


    def __update_related_fields(self):
        """
        Update all related fields
        """
        fields2show = self.get_visible_fields_names()
        formset     = []

        for field in self.model._meta.get_fields():

            if not isinstance(
                field,
                (models.ForeignKey,models.ManyToManyField)
            ): continue

            if field.name not in fields2show: continue #only update this field if is visible
            if field.name in self.readonly:   continue

            pyforms_field = getattr(self, field.name)
            queryset = field.related_model.objects.all()

            #limit_choices = field.get_limit_choices_to()
            #if limit_choices:
            #    queryset = queryset.filter(**limit_choices)

            queryset = self.get_related_field_queryset(field, queryset)

            self.update_related_field(field, pyforms_field, queryset)



    def create_model_formfields(self):
        """
        Create the model edition form.
        """
        fields2show = self.get_visible_fields_names()
        formset     = []

        for field_name in fields2show:

            # if the field already exists then ignore the creation
            if hasattr(self, field_name): continue

            try:
                field = self.model._meta.get_field(field_name)
            except FieldDoesNotExist:
                try:
                    field = getattr(self.model, field_name)
                except AttributeError:
                    continue

            if hasattr(field, "field"):
                # follow relationships,e.g. ManyToManyRel
                field = field.field

            required = not field.blank and not field.has_default()

            if not (callable(field) and not isinstance(field, models.Model)):
                label = get_lookup_verbose_name(self.model, field_name)

            # if it is a function
            if callable(field) and not isinstance(field, models.Model):
                label = getattr(field, 'short_description') if hasattr(field, 'short_description') else field_name
                pyforms_field = ControlText( label, readonly=True, required=required, helptext=field.help_text )
                self._callable_fields.append( field_name )

            # if it is read only
            elif field.name in self.readonly:

                if isinstance(field, models.TextField):
                    pyforms_field = ControlTextArea( label, readonly=True, required=required, helptext=field.help_text )
                else:
                    pyforms_field = ControlText( label, readonly=True, required=required, helptext=field.help_text )

            # if it is AutoField
            elif isinstance(field, models.AutoField):
                pyforms_field = ControlText( label, readonly=True, required=required, helptext=field.help_text )
                self._auto_fields.append( field_name )


            elif isinstance(field, models.Field) and field.choices:
                pyforms_field = ControlCombo(
                    label,
                    items=[
                        (c[1], c[0])
                        for c in field.get_choices(include_blank=field.blank)
                    ],
                    default=field.default, required=required, helptext=field.help_text
                )
            elif isinstance(field, models.BigIntegerField):             pyforms_field = ControlInteger( label, default=field.default, required=required, helptext=field.help_text )
            elif isinstance(field, models.BooleanField):                pyforms_field = ControlCheckBox( label, default=field.default, required=required, helptext=field.help_text )
            elif isinstance(field, models.DateTimeField):               pyforms_field = ControlDateTime( label, default=field.default, required=required, helptext=field.help_text )
            elif isinstance(field, models.DateField):                   pyforms_field = ControlDate( label, default=field.default, required=required, helptext=field.help_text )
            elif isinstance(field, models.DecimalField):                pyforms_field = ControlDecimal( label, default=field.default, required=required, helptext=field.help_text )
            elif isinstance(field, models.FileField):                   pyforms_field = ControlFileUpload( label, default=field.default, required=required, helptext=field.help_text )
            elif isinstance(field, models.FloatField):                  pyforms_field = ControlFloat( label, default=field.default, required=required, helptext=field.help_text )
            elif isinstance(field, models.ImageField):                  pyforms_field = ControlFileUpload( label, default=field.default, required=required, helptext=field.help_text )
            elif isinstance(field, models.IntegerField):                pyforms_field = ControlInteger( label, default=field.default, required=required, helptext=field.help_text )
            elif isinstance(field, models.TextField):                   pyforms_field = ControlTextArea( label, default=field.default, required=required, helptext=field.help_text )
            elif isinstance(field, models.NullBooleanField):
                pyforms_field = ControlCombo(
                    label,
                    items=[('Unknown', None), ('Yes', True), ('No', False)],
                    default=field.default, required=required, helptext=field.help_text
                )
            elif isinstance(field, models.ForeignKey):
                query = field.related_model.objects.all()
                limit_choices = field.get_limit_choices_to()
                if limit_choices: query = query.filter(**limit_choices)

                pyforms_field = ControlAutoComplete(
                    label,
                    queryset=query,
                    queryset_filter=self.autocomplete_search,
                    default=field.default, required=required, helptext=field.help_text
                )
            elif isinstance(field, models.ManyToManyField):
                query = field.related_model.objects.all()
                limit_choices = field.get_limit_choices_to()
                if limit_choices: query = query.filter(**limit_choices)

                pyforms_field = ControlAutoComplete(
                    label,
                    queryset=query,
                    multiple=True,
                    queryset_filter=self.autocomplete_search, required=required, helptext=field.help_text
                )
            else:
                default = None
                if hasattr(field, 'default'): default = field.default
                pyforms_field = ControlText(
                    label,
                    default=default,
                    required=required,
                    helptext=field.help_text,
                )

            # add the field to the application
            if pyforms_field is not None:
                setattr(self, field_name, pyforms_field)
                formset.append(field_name)
                self.edit_fields.append( pyforms_field )

        #Create the inlines edition forms.
        self.inlines_controls_name  = []
        self.inlines_controls       = []
        for inline in self.inlines:
            pyforms_field           = ControlEmptyWidget()
            pyforms_field.name      = inline.__name__
            pyforms_field._parent   = self
            setattr(self, inline.__name__, pyforms_field)
            self.inlines_controls_name.append(inline.__name__)
            self.inlines_controls.append( pyforms_field )


        self.formset = self.fieldsets if self.fieldsets else formset
        self.formset = self.formset + self.get_buttons_row()


    def __create_btn_event(self):
        """
        Event called by the create button
        """
        if not self._has_add_permissions:
            raise Exception('You do not have permissions to add objects.')

        obj = self.create_newobject()
        self.save_form_event(obj)


    def save_btn_event(self):
        """
        Event called by the save button
        """
        obj = self.model_object

        if obj is None:
            # The object is None, call the create event
            self.__create_btn_event()
            return

        else:

            if not self._has_update_permissions:
                raise Exception('You do not have permissions to update the object.')

            self.save_form_event(obj)


    def __remove_btn_event(self):
        """
        Event called by the remove button
        """

        def related_objects(obj):
            objects = []
            for rel in list(obj.__class__._meta.related_objects):
                f = {rel.field.name: obj}
                rel_objects = rel.related_model.objects.filter(**f)

                for o in rel_objects:
                    objects.append( (o, related_objects(o) ) )
            return objects

        def related_objects_html(objects):
            html = "<ul>"
            for o, objs in objects:
                html += "<li>"
                html += "{1}: <b>{0}</b>".format(
                    str(o), o.__class__._meta.verbose_name
                )
                if len(objs)>0:
                    html += related_objects_html(objs)
                html += "</li>"
            html += "</ul>"
            return html

        if self.object_pk:
            obj = self.model_object

            if not self._has_remove_permissions:
                raise Exception('Your user does not have permissions to remove the object')

            objects = obj, related_objects(obj)
            html = related_objects_html([objects])

            popup = self.warning_popup(html,
                self.POPUP_REMOVE_TITLE,
                buttons=[self.REMOVE_BTN_LABEL,self.CANCEL_BTN_LABEL],
                handler=self.popup_remove_handler
            )
            popup.button_0.css = 'basic red'

            # update the parent list
            if self.POPULATE_PARENT and self.parent:
                self.parent.populate_list()








    def has_add_permissions(self):
        """
        The functions returns if the user has permissions to add objects or not.

        Returns:
            bool: True if has add permissions, False otherwise.
        """
        if hasattr(self, 'parent') and self.parent and not self.parent.has_add_permissions():
            return False

        queryset = self.model.objects.all()
        if  hasattr(queryset, 'has_add_permissions'):
            return queryset.has_add_permissions(
                PyFormsMiddleware.user()
            )
        else:
            return True

    def has_view_permissions(self):
        """
        The functions returns if the user has permissions to view the queryset or not.

        Returns:
            bool: True if has view permissions, False otherwise.
        """
        if self.model_object is None: return True

        if hasattr(self, 'parent') and self.parent and not isinstance(self.parent, ModelFormWidget) and not self.parent.has_view_permissions(self.model_object):
            return False

        queryset = self.model.objects.filter(pk=self.object_pk)
        if  hasattr(queryset, 'has_view_permissions'):
            user = PyFormsMiddleware.user()
            return queryset.has_view_permissions( user )
        else:
            return True

    def has_session_permissions(self, user):
        return self.has_view_permissions()

    def has_remove_permissions(self):
        """
        The functions returns if the user has permissions to remove the current queryset or not.

        Returns:
            bool: True if has remove permissions, False otherwise.
        """
        if hasattr(self, 'parent') and self.parent and not isinstance(self.parent, ModelFormWidget) and not self.parent.has_remove_permissions(self.model_object):
            return False

        queryset = self.model.objects.filter(pk=self.object_pk)
        if  hasattr(queryset, 'has_remove_permissions'):
            return queryset.has_remove_permissions( PyFormsMiddleware.user() )
        else:
            return True

    def has_update_permissions(self):
        """
        The functions returns if the user has permissions to update the current queryset or not.

        Returns:
            bool: True if has update permissions, False otherwise.
        """
        if hasattr(self, 'parent') and self.parent and not isinstance(self.parent, ModelFormWidget) and not self.parent.has_update_permissions(self.model_object):
            return False

        queryset = self.model.objects.filter(pk=self.object_pk)
        if  hasattr(queryset, 'has_update_permissions'):
            return queryset.has_update_permissions( PyFormsMiddleware.user() )
        else:
            return True
