from pyforms_web.web.basewidget                         import BaseWidget, no_columns
from pyforms_web.web.controls.ControlTextArea           import ControlTextArea
from pyforms_web.web.controls.ControlText               import ControlText
from pyforms_web.web.controls.ControlInteger            import ControlInteger
from pyforms_web.web.controls.ControlFloat              import ControlFloat
from pyforms_web.web.controls.ControlCombo              import ControlCombo
from pyforms_web.web.controls.ControlDate               import ControlDate
from pyforms_web.web.controls.ControlDateTime           import ControlDateTime
from pyforms_web.web.controls.ControlButton             import ControlButton
from pyforms_web.web.controls.ControlQueryList          import ControlQueryList
from pyforms_web.web.controls.ControlMultipleSelection  import ControlMultipleSelection
from pyforms_web.web.controls.ControlEmptyWidget        import ControlEmptyWidget
from pyforms_web.web.controls.ControlFileUpload         import ControlFileUpload
from pyforms_web.web.controls.ControlCheckBox           import ControlCheckBox

from pyforms_web.web.django_pyforms.middleware import PyFormsMiddleware
from django.core.exceptions import ValidationError, FieldDoesNotExist
from pyforms_web.web.django_pyforms.model_admin.utils import get_fieldsets_strings
import traceback
from django.conf import settings
from django.db import models
import os




class EditFormAdmin(BaseWidget):

    MODEL     = None  #model to manage
    TITLE     = None  #title of the application
    INLINES   = []    #sub models to show in the interface
    FIELDSETS = None  #formset of the edit form
    READ_ONLY = []
    
    SAVE_BTN_LABEL     = '<i class="save icon"></i> Save'
    CREATE_BTN_LABEL   = '<i class="plus icon"></i> Create'
    CANCEL_BTN_LABEL   = '<i class="hide icon"></i> Close'
    REMOVE_BTN_LABEL   = '<i class="trash outline icon"></i> Remove'
    POPUP_REMOVE_TITLE = 'The next objects are going to be affected or removed'

    HAS_CANCEL_BTN     = True

    def __init__(self, *args, **kwargs):
        """
        Parameters:
            title - Title of the app
            model - Model to manage
            inlines - Inlines apps
            fieldsets - Organization of the fields
            parent_pk - Parent model key
            parent_model - Parent model class
            pk - Model register to manage
        """
        BaseWidget.__init__(self, 
            kwargs.get('title', self.TITLE), 
            parent_win=kwargs.get('parent_win', None)
        )
        self.model       = kwargs.get('model',     self.MODEL)
        self.inlines     = kwargs.get('inlines',   self.INLINES)
        self.fieldsets   = kwargs.get('fieldsets', self.FIELDSETS)
        self.readonly    = kwargs.get('readonly',  self.READ_ONLY)

        if 'parent_listapp' in kwargs: self.parent_listapp = kwargs.get('parent_listapp')
        
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
            self.set_parent(self.parent_model, self.parent_pk)
        #######################################################

        # buttons
        self._save_btn      = ControlButton(self.SAVE_BTN_LABEL)
        self._create_btn    = ControlButton(self.CREATE_BTN_LABEL)
        self._remove_btn    = ControlButton(self.REMOVE_BTN_LABEL)  
        if self.HAS_CANCEL_BTN:
            self._cancel_btn    = ControlButton(self.CANCEL_BTN_LABEL)
        
        self._remove_btn.css = 'red basic'
        if self.HAS_CANCEL_BTN:
            self._cancel_btn.css = 'gray basic'
        
        
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
        
    
        
        self.create_model_formfields()
        pk = kwargs.get('pk', None)
        if pk:
            self.object_pk = pk
            self.show_edit_form()
        else:
            self.show_create_form()


        self.formset = self.formset + self.get_buttons_row()

        #for inline in self.inlines:
        #    self.formset.append(inline.__name__)

        
    #################################################################################
    #################################################################################

    def get_buttons_row(self):
        buttons = ['_save_btn', '_create_btn']
        if self.HAS_CANCEL_BTN:
            buttons = buttons + ['_cancel_btn', ' ']
        buttons = buttons + ['_remove_btn']
        return [no_columns(*buttons)]
    
    def hide_form(self):
        if hasattr(self, 'parent_listapp'):
            self.parent_listapp.hide_form()
        else:
            for field in self.edit_fields:      field.hide()
            for field in self.inlines_controls: field.hide()
        
    def show_form(self):
        for field in self.edit_fields:      field.show()
        for field in self.inlines_controls: field.show()


    def cancel_btn_event(self):
        self.hide_form()









    #################################################################################
    #################################################################################
    
    def related_field_queryset(self, field, query):
        return query

    def update_related_fields(self):
        
        fields2show = self.get_visible_fields_names()       
        formset     = []

        for field in self.model._meta.get_fields():
            if field.name not in fields2show: continue #only update this field if is visible
            if field.name in self.readonly:  continue
            pyforms_field = None

            if isinstance(field, models.ForeignKey):
                #Foreign key
                pyforms_field = getattr(self, field.name)
                pyforms_field.clear_items()
                if field.null:
                    pyforms_field.add_item( '', -1 )           
                for instance in self.related_field_queryset(field, field.related_model.objects.all()):
                    pyforms_field.add_item( str(instance), instance.pk )            
            elif isinstance(field, models.ManyToManyField):
                #Many to Many field
                pyforms_field = getattr(self, field.name)
                pyforms_field.clear_items()
                for instance in self.related_field_queryset(field, field.related_model.objects.all()):
                    pyforms_field.add_item( str(instance), instance.pk )
        
    def create_model_formfields(self):
        """
            Create the model edition form
        """
        
        fields2show = self.get_visible_fields_names()       
        formset     = []

        for field in self.model._meta.get_fields():
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
            elif isinstance(field, models.ForeignKey):                  pyforms_field = ControlCombo( field.verbose_name.capitalize() )
            elif isinstance(field, models.ManyToManyField):             pyforms_field = ControlMultipleSelection( field.verbose_name.capitalize() )
                
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


    
    def show_create_form(self):

        #check if it has permissions to add new registers
        if hasattr(self, 'parent_listapp') and \
           not self.parent_listapp.has_add_permission():
           raise Exception('Your user does not have permissions to add')
            
            
        
        fields2show = self.get_visible_fields_names()

        self.update_related_fields()
        
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
        if  pk: self.object_pk = pk
        for field in self.edit_fields:      field.show()
        for field in self.inlines_controls: field.show()
        self._create_btn.hide()

        self.update_related_fields()

        obj = self.model_object
        fields2show = self.get_visible_fields_names()
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
                getattr(self, field.name).value = v.pk if v else None
            elif isinstance(field, models.ManyToManyField):                 
                getattr(self, field.name).value = [o.pk for o in getattr(obj, field.name).all()]
            
        self.inlines_apps = []
        for inline in self.inlines:
            getattr(self, inline.__name__)._name = inline.__name__
            app =  inline(parent_model=self.model, parent_pk=self.object_pk)
            self.inlines_apps.append(app)
            getattr(self, inline.__name__).value = app

        return obj


    def delete_event(self):
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
        if button==self.CANCEL_BTN_LABEL:
            popup.close()
        elif button==self.REMOVE_BTN_LABEL:
            if self.delete_event():
                self.success('The object was deleted with success!','Success!')
                popup.close()
            else:
                popup.warning('The object was not deleted!','Warning!')

    def create_object4save(self):
        return self.model()

    def save_event(self):
        fields2show = self.get_visible_fields_names()

        try:
            obj = self.model_object
            if obj is None: 
                #check if it has permissions to add new registers
                if hasattr(self, 'parent_listapp') and \
                   not self.parent_listapp.has_add_permission():
                   raise Exception('Your user does not have permissions to add')
                
                obj=self.create_object4save()
            
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
                    if value is not None and value!=-1: 
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
                    values = getattr(self, field.name).value
                    field_instance = getattr(obj, field.name)
                    field_instance.clear()

                    if field_instance.through is None:
                        for value in values:
                            o = field.related_model.objects.get(pk=value)
                            field_instance.add(o)
                    else:
                        for value in values:
                            o = field.related_model.objects.get(pk=value)
                            rel_obj = field_instance.through()
                            setattr(rel_obj,obj.__class__.__name__.lower(), obj)
                            setattr(rel_obj,o.__class__.__name__.lower(), o)
                            rel_obj.save()

            self.object_pk = obj.pk

            return obj

        except Exception as e:
            traceback.print_exc()
            self.alert(str(e))

            return None

    def set_parent(self, parent_model, parent_pk):
        self.parent_pk      = parent_pk
        self.parent_model   = parent_model

        for field in self.model._meta.get_fields():
            if isinstance(field, models.ForeignKey):
                if parent_model == field.related_model:
                    self.parent_field = field
                    break


    def get_visible_fields_names(self):
        #return the names of the visible fields
        fields = get_fieldsets_strings(self.fieldsets) if self.fieldsets else [field.name for field in self.model._meta.get_fields() if not(isinstance(field, models.OneToOneField) and field.name.endswith('_ptr'))]
        
        if self.parent_field: 
            try:
                fields.remove(self.parent_field.name)
            except ValueError: pass
        return fields


    #################################################################################
    #### PRIVATE FUNCTIONS ##########################################################
    #################################################################################

    def __create_btn_event(self):
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
        obj = self.save_event()
        if obj:
            self.success('The object <b>{0}</b> was saved with success!'.format(obj),'Success!')

    
    def __remove_btn_event(self):

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


        

    

    @property 
    def model_object(self):
        if self.object_pk is None:
            return None
        else:
            return self.model.objects.get(pk=self.object_pk)