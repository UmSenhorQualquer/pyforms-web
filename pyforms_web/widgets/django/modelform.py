from pyforms_web.basewidget                         import BaseWidget, no_columns
from pyforms_web.controls.control_textarea           import ControlTextArea
from pyforms_web.controls.control_text               import ControlText
from pyforms_web.controls.control_integer            import ControlInteger
from pyforms_web.controls.control_float              import ControlFloat
from pyforms_web.controls.control_combo              import ControlCombo
from pyforms_web.controls.control_autocomplete       import ControlAutoComplete
from pyforms_web.controls.control_date               import ControlDate
from pyforms_web.controls.control_datetime           import ControlDateTime
from pyforms_web.controls.control_button             import ControlButton
from pyforms_web.controls.control_querylist          import ControlQueryList
from pyforms_web.controls.control_emptywidget        import ControlEmptyWidget
from pyforms_web.controls.control_fileupload         import ControlFileUpload
from pyforms_web.controls.control_checkbox           import ControlCheckBox
from pyforms_web.controls.control_multipleselectionquery  import ControlMultipleSelectionQuery

import collections
from pyforms_web.web.middleware import PyFormsMiddleware
from django.core.exceptions import ValidationError, FieldDoesNotExist
from .utils import get_fieldsets_strings
import traceback
from django.conf import settings
from django.db import models
import os
from django.db.models import Q

from pyforms_web.utils import get_lookup_verbose_name

import datetime
from django.utils import timezone



class ModelFormWidget(BaseWidget):
    """
    When a Pyforms application inherit from this class a form for the model EditFormAdmin.MODEL is created.

    **Usage example:**

    .. code:: python

       from funding.models import FundingOpportunity

       class EditFundingOpportunitiesApp(EditFormAdmin):
            
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

    MODEL          = None  #: class: Model to manage
    TITLE          = None  #: str: Title of the application
    INLINES        = []    #: list(class): Sub models to show in the interface
    FIELDSETS      = None  #: Formset of the edit form
    READ_ONLY      = []    #: list(str): List of readonly fields

    #: bool: Flag to show or hide the cancel button
    HAS_CANCEL_BTN_ON_EDIT = True
    #: bool: Flag to show or hide the cancel button
    HAS_CANCEL_BTN_ON_ADD  = True

    #: bool: Close the application on remove
    CLOSE_ON_REMOVE = False 
    #: bool: Close the application on cancel
    CLOSE_ON_CANCEL = False
 
    #: str: Label for the save button
    SAVE_BTN_LABEL     = '<i class="save icon"></i> Save' 
    #: str: Label for the create button
    CREATE_BTN_LABEL   = '<i class="plus icon"></i> Create'
    #: str: Label for the cancel button
    CANCEL_BTN_LABEL   = '<i class="hide icon"></i> Close'
    #: str: Label for the delete button
    REMOVE_BTN_LABEL   = '<i class="trash outline icon"></i> Remove'
    #: str: Label for the popup window for the delete confirmation
    POPUP_REMOVE_TITLE = 'The next objects are going to be affected or removed'
    
    def __init__(self, *args, **kwargs):
        """
        :param str title: Title of the app. By default will assume the value in the class variable TITLE.
        :param django.db.models.Model model: Model with the App will represent. By default will assume the value in the class variable MODEL.
        :param list(ModelAdmin) inlines: Sub models to show in the interface
        :param list(str) fieldsets: Organization of the fields
        :param int parent_pk: Parent model key
        :param django.db.models.Model parent_model: Parent model class
        :param int pk: Model register to manage
        """
        
        BaseWidget.__init__(self, *args, **kwargs )

        self.object_pk = kwargs.get('pk', None)
        self.model     = kwargs.get('model',     self.MODEL)
        self.fieldsets = kwargs.get('fieldsets', self.FIELDSETS)
        self.readonly  = kwargs.get('readonly',  self.READ_ONLY)
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
        self._save_btn   = ControlButton(self.SAVE_BTN_LABEL, label_visible=False, default=self.__save_btn_event)
        self.edit_buttons.append( self._save_btn )
        
        self._create_btn = ControlButton(self.CREATE_BTN_LABEL, label_visible=False, default=self.__create_btn_event)
        self.edit_buttons.append( self._create_btn )
        
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
            self.show_edit_form()
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

            return queryset.get(pk=self.object_pk)

    #################################################################################
    #### FUNCTIONS ##################################################################
    #################################################################################


    def get_buttons_row(self):
        """
        This function generate the formset configuration for the save, create,
        cancel and remove buttons,

        Returns:
            list(str): Returns the formset configuration that will be append to
            the end of the fieldsets.
        """
        buttons = ['_save_btn', '_create_btn']
        if self.has_cancel_btn:
            buttons = buttons + ['_cancel_btn', ' ']
        buttons = buttons + ['_remove_btn']
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
        if self.CLOSE_ON_CANCEL:
            self.close()
        else:
            self.hide_form()


    def autocomplete_search(self, queryset, keyword, control):
        """
        Function used by a combobox to get the items dynamically

        :param queryset keyword: Queryset from where to filter the results
        :param str keyword: Keyword for filter the results
        :param pyforms.controls.BaseControl: Control calling the autocomplete
        
        Returns:
            list(dict): Results for the search in the format
        
            .. code-block:: python
                    
                [{'name':name, 'value':id, 'text':text}, ...]

        """
        field = self.model._meta.get_field(control.name)
        queryset = self.related_field_queryset(field, queryset)

        return queryset

    
    def related_field_queryset(self, field, queryset):
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
        if ( self.parent and hasattr(self.parent, 'has_add_permission') ) and \
           not self.parent.has_add_permission():
           raise Exception('Your user does not have permissions to add')
            
        fields2show = self.get_visible_fields_names()

        self.__update_related_fields()

        # clear all the fields
        for field_name in fields2show:
            if hasattr(self, field_name):
                pyforms_field = getattr(self, field_name)
                pyforms_field.value = None

        for field in self.edit_fields: field.show()
        
        for inline in self.inlines_controls:
            inline.hide()

        self._save_btn.hide()
        self._remove_btn.hide()

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

        :param int pk: Primiry key of the object to be show in the edit form.

        Returns:
            :django.db.models.Model object: Returns the object in edition.
        """
        
        if  pk: self.object_pk = pk
        for field in self.edit_fields:      field.show()
        for field in self.inlines_controls: field.show()
        self._create_btn.hide()

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
                        pyforms_field.value = value

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
            self._remove_btn.hide()
            self._create_btn.show()
            self._save_btn.hide()
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

    def save_object(self, obj):
        """
        Function called to save the object

        :param django.db.models.Model obj: Object to save.
        
        """
        try:
            obj.full_clean()
        except ValidationError as e:
            html = '<ul class="list">'
            for field_name, messages in e.message_dict.items():
                
                try:
                    getattr(self, field_name).error = True

                    label = get_lookup_verbose_name(self.model, field_name)
                    html += '<li><b>{0}</b>'.format(label.capitalize())
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
        return obj

    def save_event(self):
        """
        Function called when the save is called.

        Returns:
            :django.db.models.Model object: Created object or None if the object was not saved with success.
        """
        fields2show = self.get_visible_fields_names()

        try:
            obj = self.model_object

            ## create an object if does not exists ####
            if obj is None: 
                #check if it has permissions to add new registers
                if ( self.parent and hasattr(self.parent, 'has_add_permission') ) and \
                   not self.parent.has_add_permission():
                   raise Exception('Your user does not have permissions to add')
                
                obj = self.create_newobject()

            ###########################################
            
            # if it is working as an inline edition form #
            if self.parent_field:
                setattr(obj, 
                    self.parent_field.name, 
                    self.parent_model.objects.get(pk=self.parent_pk)
                )
            ##############################################

            for field in self.model._meta.get_fields():
                if field.name not in fields2show: continue
                if field.name in self.readonly:   continue
                
                pyforms_field = getattr(self, field.name)
                value         = pyforms_field.value

                if   isinstance(field, models.AutoField):
                    continue
                
                elif isinstance(field, models.FileField):
                    getattr(self, field.name).error = False
                    value = getattr(self, field.name).value
                    if value:
                        try:
                            os.makedirs(os.path.join(settings.MEDIA_ROOT, field.upload_to))
                        except os.error as e:
                            pass

                        paths = [p for p in value.split('/') if len(p)>0][1:]
                        from_path   = os.path.join(settings.MEDIA_ROOT,*paths)
                        if os.path.exists(from_path):
                            to_path     = os.path.join(settings.MEDIA_ROOT, field.upload_to, os.path.basename(value) )
                            os.rename(from_path, to_path)
        
                            url = '/'.join([field.upload_to]+[os.path.basename(value) ])
                            if url[0]=='/': url = url[1:]
                            setattr(obj, field.name, url)
                    elif field.null:
                        setattr(obj, field.name, None)
                    else:
                        setattr(obj, field.name, '')
                
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

                elif not isinstance(field, models.ManyToManyField):
                    pyforms_field.error = False
                    setattr(obj, field.name, value)
                

            self.save_object(obj)
            
            for field in self.model._meta.get_fields():

                if isinstance(field, models.ManyToManyField) and hasattr(self, field.name):
                    values          = getattr(self, field.name).value
                    field_instance  = getattr(obj, field.name)

                    objs            = field.related_model.objects.filter(pk__in=values)
                    values_2_remove = field_instance.all().exclude(pk__in=[o.pk for o in objs])

                    for o in values_2_remove: 
                        field_instance.remove(o)

                    values_2_add    = objs.exclude(pk__in=[o.pk for o in field_instance.all()])
                    for o in values_2_add:
                        field_instance.add(o)
                    
                   
            self.object_pk = obj.pk

            self.update_callable_fields()
            self.update_autonumber_fields()

            

            return obj

        except Exception as e:
            traceback.print_exc()
            self.alert(str(e))

            return None

    

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
                if parent_model == field.related_model:
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

            queryset = self.related_field_queryset(field, queryset)

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

            pyforms_field = None

            if not (callable(field) and not isinstance(field, models.Model)):
                label = get_lookup_verbose_name(self.model, field_name)

            if callable(field) and not isinstance(field, models.Model):
                label = getattr(field, 'short_description') if hasattr(field, 'short_description') else field_name
                pyforms_field = ControlText( label.capitalize(), readonly=True )
                self._callable_fields.append( field_name )

            
            elif field.name in self.readonly:

                if isinstance(field, models.TextField):
                    pyforms_field = ControlTextArea( label.capitalize(), readonly=True )
                else:
                    pyforms_field = ControlText( label.capitalize(), readonly=True )
            
            elif isinstance(field, models.AutoField):
                pyforms_field = ControlText( label.capitalize(), readonly=True )
                self._auto_fields.append( field_name )
        
            elif isinstance(field, models.Field) and field.choices:
                pyforms_field = ControlCombo( 
                    label.capitalize(), 
                    items=[ (c[1],c[0]) for c in field.choices]
                )
            elif isinstance(field, models.BigIntegerField):             pyforms_field = ControlInteger( label.capitalize() )
            elif isinstance(field, models.BooleanField):                pyforms_field = ControlCheckBox( label.capitalize() )
            elif isinstance(field, models.DateTimeField):               pyforms_field = ControlDateTime( label.capitalize() )
            elif isinstance(field, models.DateField):                   pyforms_field = ControlDate( label.capitalize() )
            elif isinstance(field, models.DecimalField):                pyforms_field = ControlFloat( label.capitalize() )
            elif isinstance(field, models.FileField):                   pyforms_field = ControlFileUpload( label.capitalize() )
            elif isinstance(field, models.FloatField):                  pyforms_field = ControlFloat( label.capitalize() )
            elif isinstance(field, models.ImageField):                  pyforms_field = ControlFileUpload( label.capitalize() )
            elif isinstance(field, models.IntegerField):                pyforms_field = ControlInteger( label.capitalize() )
            elif isinstance(field, models.TextField):                   pyforms_field = ControlTextArea( label.capitalize() )
            elif isinstance(field, models.NullBooleanField):            
                pyforms_field = ControlCombo( 
                    label.capitalize(), 
                    items=[('Unknown', None), ('Yes', True), ('No', False)]
                )
            elif isinstance(field, models.ForeignKey):
                url = "/pyforms/autocomplete/{app_id}/{field_name}/{{query}}/".format(app_id=self.uid, field_name=field.name)
                
                query = field.related_model.objects.all()
                limit_choices = field.get_limit_choices_to()
                if limit_choices: query = query.filter(**limit_choices)
        
                pyforms_field = ControlAutoComplete( 
                    label.capitalize(), 
                    queryset=query,
                    queryset_filter=self.autocomplete_search
                )

            elif isinstance(field, models.ManyToManyField):
                url = "/pyforms/autocomplete/{app_id}/{field_name}/{{query}}/".format(app_id=self.uid, field_name=field.name)
                
                query = field.related_model.objects.all()
                limit_choices = field.get_limit_choices_to()
                if limit_choices: query = query.filter(**limit_choices)
        
                pyforms_field = ControlAutoComplete( 
                    label.capitalize(), 
                    queryset=query,
                    multiple=True,
                    queryset_filter=self.autocomplete_search
                )
            else:
                pyforms_field = ControlText( label.capitalize() )
            
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
        self.object_pk = None
        obj = self.save_event()

        if self.parent and obj:
            # it is being use from a ModelAdminWidget
            self.parent.show_edit_form(pk=self.object_pk)
            self.parent.hide_form()
        elif obj:
            # it is executing as a single app
            self._create_btn.hide()
            self._save_btn.show()
            self._remove_btn.show()

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
            

    def __save_btn_event(self):
        """
        Event called by the save button
        """
        obj = self.save_event()
        if obj:
            self.success('The object <b>{0}</b> was saved with success!'.format(obj),'Success!')

    
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
                    str(o), o.__class__._meta.verbose_name.title()
                )
                if len(objs)>0:
                    html += related_objects_html(objs)
                html += "</li>"
            html += "</ul>"
            return html

        if self.object_pk:
            obj = self.model_object

            objects = obj, related_objects(obj)
            html = related_objects_html([objects])

            popup = self.warning_popup(html, 
                self.POPUP_REMOVE_TITLE, 
                buttons=[self.REMOVE_BTN_LABEL,self.CANCEL_BTN_LABEL], 
                handler=self.popup_remove_handler
            )
            popup.button_0.css = 'basic red'    