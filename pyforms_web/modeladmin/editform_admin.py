from pyforms_web.basewidget                         import BaseWidget, no_columns
from pyforms_web.controls.ControlTextArea           import ControlTextArea
from pyforms_web.controls.ControlText               import ControlText
from pyforms_web.controls.ControlInteger            import ControlInteger
from pyforms_web.controls.ControlFloat              import ControlFloat
from pyforms_web.controls.ControlCombo              import ControlCombo
from pyforms_web.controls.ControlAutoComplete       import ControlAutoComplete
from pyforms_web.controls.ControlDate               import ControlDate
from pyforms_web.controls.ControlDateTime           import ControlDateTime
from pyforms_web.controls.ControlButton             import ControlButton
from pyforms_web.controls.ControlQueryList          import ControlQueryList
from pyforms_web.controls.ControlEmptyWidget        import ControlEmptyWidget
from pyforms_web.controls.ControlFileUpload         import ControlFileUpload
from pyforms_web.controls.ControlCheckBox           import ControlCheckBox
from pyforms_web.controls.ControlMultipleSelectionQuery  import ControlMultipleSelectionQuery


from pyforms_web.web.middleware import PyFormsMiddleware
from django.core.exceptions import ValidationError, FieldDoesNotExist
from .utils import get_fieldsets_strings
import traceback
from django.conf import settings
from django.db import models
import os
from django.db.models import Q




class EditFormAdmin(BaseWidget):

    MODEL          = None  #: class: Model to manage
    TITLE          = None  #: str: Title of the application
    INLINES        = []    #: list(class): Sub models to show in the interface
    FIELDSETS      = None  #: Formset of the edit form
    READ_ONLY      = []    #: list(str): List of readonly fields 
    HAS_CANCEL_BTN = True  #: bool: Flag to show or hide the cancel button
 
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

        self.model       = kwargs.get('model',     self.MODEL)
        self.inlines     = kwargs.get('inlines',   self.INLINES)
        self.fieldsets   = kwargs.get('fieldsets', self.FIELDSETS)
        self.readonly    = kwargs.get('readonly',  self.READ_ONLY)

        if self.fieldsets is None: self.fieldsets = self.FIELDSETS
        
        self.edit_fields            = []
        self.inlines_apps           = []
        self.inlines_controls_name  = []
        self.inlines_controls       = []
        
        self.object_pk = None

        # used to configure the interface to inline
        # it will filter the dataset by the foreign key
        self.parent_field = None
        self.parent_pk    = kwargs.get('parent_pk', None)
        self.parent_model = kwargs.get('parent_model', None)
        if self.parent_model and self.parent_pk:
            self.__set_parent(self.parent_model, self.parent_pk)
        #######################################################

        # buttons
        self._save_btn      = ControlButton(self.SAVE_BTN_LABEL)
        self._create_btn    = ControlButton(self.CREATE_BTN_LABEL)
        self._remove_btn    = ControlButton(self.REMOVE_BTN_LABEL,  css='red basic')  
        if self.HAS_CANCEL_BTN:
            self._cancel_btn = ControlButton(self.CANCEL_BTN_LABEL, css='gray basic')

        if self.parent_model:
            self._save_btn.css       += ' tiny'
            self._create_btn.css     += ' tiny'
            self._remove_btn.css     += ' tiny'
            if self.HAS_CANCEL_BTN:
                self._cancel_btn.css += ' tiny'
        
        self.edit_fields.append( self._save_btn )
        self.edit_fields.append( self._create_btn )
        self.edit_fields.append( self._remove_btn )
        if self.HAS_CANCEL_BTN:
            self.edit_fields.append( self._cancel_btn )

        for field in self.edit_fields: field.hide()
                
        # events
        self._create_btn.value  = self.__create_btn_event
        self._remove_btn.value  = self.__remove_btn_event
        self._save_btn.value    = self.__save_btn_event
        if self.HAS_CANCEL_BTN:
            self._cancel_btn.value  = self.cancel_btn_event
        
        self._create_btn.label_visible  = False
        self._remove_btn.label_visible  = False
        self._save_btn.label_visible    = False
        if self.HAS_CANCEL_BTN:
            self._cancel_btn.label_visible  = False
        

        self.__create_model_formfields()
        pk = kwargs.get('pk', None)
        if pk:
            self.object_pk = pk
            self.show_edit_form()
        else:
            self.show_create_form()


        self.formset = self.formset + self.get_buttons_row()

        for inline in self.inlines:
            self.formset.append(inline.__name__)

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
                queryset = self.model.get_queryset(queryset, request)
           
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
        if self.HAS_CANCEL_BTN:
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
        self.hide_form()

    


    def autocomplete_search(self, keyword, field):
        """
        Function used by a combobox to get the items dynamically

        :param str keywork: Keyword for filter the results
        :param django.db.models.fields.Field field: Django field where the autocomplete will be applied
        
        Returns:
            list(dict): Results for the search in the format
        
            .. code-block:: python
                    
                [{'name':name, 'value':id, 'text':text}, ...]

        """
        query = field.related_model.objects.all()
        query = self.related_field_queryset(field, query)

        if hasattr(field.related_model, 'autocomplete_search_fields'):
            or_filter = Q()
            for search_field in field.related_model.autocomplete_search_fields():
                or_filter.add( Q(**{search_field:keyword}), Q.OR)
        else:
            or_filter = Q(pk=keyword)

        try:
            return [{'name':str(o), 'value':o.pk, 'text':str(o)} for o in query.filter(or_filter)]
        except:
            return []

    
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
            
        fields2show = self.__get_visible_fields_names()

        self.__update_related_fields()
        
        for field in self.model._meta.get_fields():
            if field.name not in fields2show:                       continue
            if isinstance(field, models.AutoField):                 continue
            elif isinstance(field, models.BigAutoField):            continue
            elif isinstance(field, models.OneToOneField) and field.name.endswith('_ptr'):   continue
            elif isinstance(field, models.BigIntegerField):         getattr(self, field.name).value = None
            elif isinstance(field, models.BinaryField):             getattr(self, field.name).value = None
            elif isinstance(field, models.BooleanField):            getattr(self, field.name).value = None
            elif isinstance(field, models.CharField):               getattr(self, field.name).value = None
            elif isinstance(field, models.CommaSeparatedIntegerField):getattr(self, field.name).value = None
            elif isinstance(field, models.DateField):               getattr(self, field.name).value = None
            elif isinstance(field, models.DateTimeField):           getattr(self, field.name).value = None
            elif isinstance(field, models.DecimalField):            getattr(self, field.name).value = None
            elif isinstance(field, models.DurationField):           getattr(self, field.name).value = None
            elif isinstance(field, models.EmailField):              getattr(self, field.name).value = None
            elif isinstance(field, models.FileField):               getattr(self, field.name).value = None
            elif isinstance(field, models.FilePathField):           getattr(self, field.name).value = None
            elif isinstance(field, models.FloatField):              getattr(self, field.name).value = None
            elif isinstance(field, models.ImageField):              getattr(self, field.name).value = None
            elif isinstance(field, models.IntegerField):            getattr(self, field.name).value = None
            elif isinstance(field, models.GenericIPAddressField):   getattr(self, field.name).value = None
            elif isinstance(field, models.NullBooleanField):        getattr(self, field.name).value = None
            elif isinstance(field, models.PositiveIntegerField):    getattr(self, field.name).value = None
            elif isinstance(field, models.PositiveSmallIntegerField): getattr(self, field.name).value = None
            elif isinstance(field, models.SlugField):               getattr(self, field.name).value = None
            elif isinstance(field, models.SmallIntegerField):       getattr(self, field.name).value = None
            elif isinstance(field, models.TextField):               getattr(self, field.name).value = None
            elif isinstance(field, models.TimeField):               getattr(self, field.name).value = None
            elif isinstance(field, models.URLField):                getattr(self, field.name).value = None
            elif isinstance(field, models.UUIDField):               getattr(self, field.name).value = None
            elif isinstance(field, models.ForeignKey):              getattr(self, field.name).value = None

        for field in self.edit_fields: field.show()
        self._save_btn.hide()
        self._remove_btn.hide()




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
        fields2show = self.__get_visible_fields_names()
        for field in self.model._meta.get_fields():
            if field.name not in fields2show: continue

            if isinstance(field, models.AutoField):                 continue
            elif field.name in self.readonly:                       getattr(self, field.name).value = str(getattr(obj, field.name))
            elif isinstance(field, models.BigAutoField):            continue
            elif isinstance(field, models.OneToOneField) and field.name.endswith('_ptr'):   continue
            elif isinstance(field, models.BigIntegerField):           getattr(self, field.name).value = getattr(obj, field.name)
            elif isinstance(field, models.BinaryField):               getattr(self, field.name).value = getattr(obj, field.name)
            elif isinstance(field, models.BooleanField):              getattr(self, field.name).value = getattr(obj, field.name)
            elif isinstance(field, models.CharField):                 getattr(self, field.name).value = getattr(obj, field.name)
            elif isinstance(field, models.CommaSeparatedIntegerField):getattr(self, field.name).value = getattr(obj, field.name)
            elif isinstance(field, models.DateField):                 getattr(self, field.name).value = getattr(obj, field.name)
            elif isinstance(field, models.DateTimeField):             getattr(self, field.name).value = getattr(obj, field.name)
            elif isinstance(field, models.DecimalField):              getattr(self, field.name).value = getattr(obj, field.name)
            elif isinstance(field, models.DurationField):             getattr(self, field.name).value = getattr(obj, field.name)
            elif isinstance(field, models.EmailField):                getattr(self, field.name).value = getattr(obj, field.name)
            elif isinstance(field, models.FileField):                 getattr(self, field.name).value = getattr(obj, field.name).url if getattr(obj, field.name) else None
            elif isinstance(field, models.FilePathField):             getattr(self, field.name).value = getattr(obj, field.name)
            elif isinstance(field, models.FloatField):                getattr(self, field.name).value = getattr(obj, field.name)
            elif isinstance(field, models.ImageField):                getattr(self, field.name).value = getattr(obj, field.name).url if getattr(obj, field.name) else None
            elif isinstance(field, models.IntegerField):              getattr(self, field.name).value = getattr(obj, field.name)
            elif isinstance(field, models.GenericIPAddressField):     getattr(self, field.name).value = getattr(obj, field.name)
            elif isinstance(field, models.NullBooleanField):          getattr(self, field.name).value = getattr(obj, field.name)
            elif isinstance(field, models.PositiveIntegerField):      getattr(self, field.name).value = getattr(obj, field.name)
            elif isinstance(field, models.PositiveSmallIntegerField): getattr(self, field.name).value = getattr(obj, field.name)
            elif isinstance(field, models.SlugField):                 getattr(self, field.name).value = getattr(obj, field.name)
            elif isinstance(field, models.SmallIntegerField):         getattr(self, field.name).value = getattr(obj, field.name)
            elif isinstance(field, models.TextField):                 getattr(self, field.name).value = getattr(obj, field.name)
            elif isinstance(field, models.TimeField):                 getattr(self, field.name).value = getattr(obj, field.name)
            elif isinstance(field, models.URLField):                  getattr(self, field.name).value = getattr(obj, field.name)
            elif isinstance(field, models.UUIDField):                 getattr(self, field.name).value = getattr(obj, field.name)
            elif isinstance(field, models.ForeignKey):
                v = getattr(obj, field.name)
                getattr(self, field.name).value = str(v.pk) if v else None
            elif isinstance(field, models.ManyToManyField):                 
                getattr(self, field.name).value = [str(o.pk) for o in getattr(obj, field.name).all()]
            
        self.inlines_apps = []
        for inline in self.inlines:
            getattr(self, inline.__name__)._name = inline.__name__
            app =  inline(parent_model=self.model, parent_pk=self.object_pk)
            self.inlines_apps.append(app)
            getattr(self, inline.__name__).value = app

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
            else:
                popup.warning('The object was not deleted!','Warning!')

    def create_newobject(self):
        """
        Function called to create a new object of the model.

        Returns:
            :django.db.models.Model object: Created object
        """
        return self.model()

    def save_event(self):
        """
        Function called when the save is called.

        Returns:
            :django.db.models.Model object: Created object or None if the object was not saved with success.
        """
        fields2show = self.__get_visible_fields_names()

        try:
            obj = self.model_object
            if obj is None: 
                #check if it has permissions to add new registers
                if ( self.parent and hasattr(self.parent, 'has_add_permission') ) and \
                   not self.parent.has_add_permission():
                   raise Exception('Your user does not have permissions to add')
                
                obj=self.create_newobject()
            
            if self.parent_field:
                setattr(obj, self.parent_field.name, self.parent_model.objects.get(pk=self.parent_pk))
            
            for field in self.model._meta.get_fields():
                if field.name not in fields2show: continue
            
                if isinstance(field, models.AutoField):             continue
                elif isinstance(field, models.BigAutoField):        continue
                elif isinstance(field, models.OneToOneField) and field.name.endswith('_ptr'):   continue
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
                elif isinstance(field, models.DateTimeField):
                    getattr(self, field.name).error = False
                    setattr(obj, field.name, getattr(self, field.name).value )
                elif isinstance(field, models.DateField):
                    getattr(self, field.name).error = False
                    setattr(obj, field.name, getattr(self, field.name).value )
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
                    if value is not None and value!='-1': 
                        value = field.related_model.objects.get(pk=value)
                    else:
                        value = None
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
                    values          = getattr(self, field.name).value
                    field_instance  = getattr(obj, field.name)
                    allvalues       = field_instance.all()

                    if field_instance.through is None:
                        for value in values:
                            o = field.related_model.objects.get(pk=value)
                            if o not in allvalues:
                                field_instance.add(o)

                            allvalues = allvalues.exclude(pk=value)

                        for o in allvalues: o.delete()
                    else:
                        added_values = []
                        
                        # add the values
                        for value in values:    
                            if value not in allvalues:
                                added_values.append(value)
                                field_instance.add(value)
                        
                        # remove the non selected values
                        for value in allvalues:
                            if value not in added_values:
                                field_instance.remove(value)
                        


            self.object_pk = obj.pk

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
        self.parent_pk      = parent_pk
        self.parent_model   = parent_model

        for field in self.model._meta.get_fields():
            if isinstance(field, models.ForeignKey):
                if parent_model == field.related_model:
                    self.parent_field = field
                    break


    def __get_visible_fields_names(self):
        """
        Function called to get names of the visible fields.

        Returns:
            :list(str): List names of the visible fields.
        """
        fields = get_fieldsets_strings(self.fieldsets) if self.fieldsets else [field.name for field in self.model._meta.get_fields() if not(isinstance(field, models.OneToOneField) and field.name.endswith('_ptr'))]
        
        if self.parent_field: 
            try:
                fields.remove(self.parent_field.name)
            except ValueError: pass
        return fields


    def __update_related_fields(self):
        """
        Update all related fields 
        """
        fields2show = self.__get_visible_fields_names()       
        formset     = []

        for field in self.model._meta.get_fields():

            if not isinstance(
                field, 
                (models.ForeignKey,models.ManyToManyField)
            ): continue
    
            if field.name not in fields2show: continue #only update this field if is visible
            if field.name in self.readonly:   continue
            
            pyforms_field = getattr(self, field.name)
            queryset      = self.related_field_queryset(field, field.related_model.objects.all())

            self.update_related_field(field, pyforms_field, queryset)

            
    def __create_model_formfields(self):
        """
        Create the model edition form.
        """
        fields2show = self.__get_visible_fields_names()       
        formset     = []

        for field in self.model._meta.get_fields():
            if hasattr(self, field.name):     continue
            if field.name not in fields2show: continue #only create this field if is visible
            pyforms_field = None

            if isinstance(field, models.AutoField): continue
            elif field.name in self.readonly:
                pyforms_field = ControlText( field.verbose_name.capitalize(), readonly=True )
            elif isinstance(field, models.Field) and field.choices:
                pyforms_field = ControlCombo( 
                    field.verbose_name.capitalize(), 
                    items=[ (c[1],c[0]) for c in field.choices]
                )
            elif isinstance(field, models.BigAutoField):                pyforms_field = ControlText( field.verbose_name.capitalize() )
            elif isinstance(field, models.BigIntegerField):             pyforms_field = ControlInteger( field.verbose_name.capitalize() )
            elif isinstance(field, models.BinaryField):                 pyforms_field = ControlText( field.verbose_name.capitalize() )
            elif isinstance(field, models.BooleanField):                pyforms_field = ControlCheckBox( field.verbose_name.capitalize() )
            elif isinstance(field, models.CharField):                   pyforms_field = ControlText( field.verbose_name.capitalize() )
            elif isinstance(field, models.CommaSeparatedIntegerField):  pyforms_field = ControlText( field.verbose_name.capitalize() )
            elif isinstance(field, models.DateTimeField):               pyforms_field = ControlDateTime( field.verbose_name.capitalize() )
            elif isinstance(field, models.DateField):                   pyforms_field = ControlDate( field.verbose_name.capitalize() )
            elif isinstance(field, models.DecimalField):                pyforms_field = ControlFloat( field.verbose_name.capitalize() )
            elif isinstance(field, models.DurationField):               pyforms_field = ControlText( field.verbose_name.capitalize() )
            elif isinstance(field, models.EmailField):                  pyforms_field = ControlText( field.verbose_name.capitalize() )
            elif isinstance(field, models.FileField):                   pyforms_field = ControlFileUpload( field.verbose_name.capitalize() )
            elif isinstance(field, models.FilePathField):               pyforms_field = ControlText( field.verbose_name.capitalize() )
            elif isinstance(field, models.FloatField):                  pyforms_field = ControlFloat( field.verbose_name.capitalize() )
            elif isinstance(field, models.ImageField):                  pyforms_field = ControlFileUpload( field.verbose_name.capitalize() )
            elif isinstance(field, models.IntegerField):                pyforms_field = ControlInteger( field.verbose_name.capitalize() )
            elif isinstance(field, models.GenericIPAddressField):       pyforms_field = ControlText( field.verbose_name.capitalize() )
            elif isinstance(field, models.NullBooleanField):            
                pyforms_field = ControlCombo( 
                    field.verbose_name.capitalize(), 
                    items=[('Unknown', None), ('Yes', True), ('No', False)]
                )
            elif isinstance(field, models.PositiveIntegerField):        pyforms_field = ControlText( field.verbose_name.capitalize() )
            elif isinstance(field, models.PositiveSmallIntegerField):   pyforms_field = ControlText( field.verbose_name.capitalize() )
            elif isinstance(field, models.SlugField):                   pyforms_field = ControlText( field.verbose_name.capitalize() )
            elif isinstance(field, models.SmallIntegerField):           pyforms_field = ControlText( field.verbose_name.capitalize() )
            elif isinstance(field, models.TextField):                   pyforms_field = ControlTextArea( field.verbose_name.capitalize() )
            elif isinstance(field, models.TimeField):                   pyforms_field = ControlText( field.verbose_name.capitalize() )
            elif isinstance(field, models.URLField):                    pyforms_field = ControlText( field.verbose_name.capitalize() )
            elif isinstance(field, models.UUIDField):                   pyforms_field = ControlText( field.verbose_name.capitalize() )
            elif isinstance(field, models.ForeignKey):

                url = "/pyforms/autocomplete/{app_id}/{field_name}/{{query}}/".format(app_id=self.uid, field_name=field.name)
                pyforms_field = ControlAutoComplete( 
                    field.verbose_name.capitalize(), 
                    items_url=url,
                    model=field.related_model
                )

            elif isinstance(field, models.ManyToManyField):

                url = "/pyforms/autocomplete/{app_id}/{field_name}/{{query}}/".format(app_id=self.uid, field_name=field.name)
                pyforms_field = ControlAutoComplete( 
                    field.verbose_name.capitalize(), 
                    items_url=url,
                    model=field.related_model,
                    multiple=True
                )

            if pyforms_field is not None: 
                setattr(self, field.name, pyforms_field)
                formset.append(field.name)
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



    def __create_btn_event(self):
        """
        Event called by the create button
        """
        self.object_pk = None
        obj = self.save_event()
        if obj:
            self._create_btn.hide()
            self._save_btn.show()
            self._remove_btn.show()
            for i, field in enumerate(self.inlines_controls):
                app = self.inlines_apps[i]
                app.populate_list()
                app.parent_pk = obj.pk
                field.show()
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
                html += "{1}: <b>{0}</b>".format( str(o), o.__class__._meta.verbose_name.title() )
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