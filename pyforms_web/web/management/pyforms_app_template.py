#from django_pyforms.model_admin.editform_admin import EditFormAdmin
#from pyforms_web.controls.ControlQueryList import ControlQueryList

from pyforms.basewidget import ModelAdmin
from orquestra.plugins import LayoutPositions

from {application_name}.models import {model_name}


# class {model_name}EditFormAdmin(EditFormAdmin):

#     MODEL     = {model_name}  #model to manage
#     TITLE     = '{model_verbose_name}'  #title of the application
    
#     #INLINES   = []    #sub models to show in the interface
#     #FIELDSETS = None  #formset of the edit form
#     #READ_ONLY = []
    
#     #SAVE_BTN_LABEL     = '<i class="save icon"></i> Save'
#     #CREATE_BTN_LABEL   = '<i class="plus icon"></i> Create'
#     #CANCEL_BTN_LABEL   = '<i class="hide icon"></i> Close'
#     #REMOVE_BTN_LABEL   = '<i class="trash outline icon"></i> Remove'
#     #POPUP_REMOVE_TITLE = 'The next objects are going to be affected or removed'

#     #HAS_CANCEL_BTN_ON_ADD  = True #Flag to show or hide the cancel button
#     #HAS_CANCEL_BTN_ON_EDIT = True #Flag to show or hide the cancel button

#    def delete_event(self):
#        return super({model_name}EditFormAdmin,self).delete_event()

class {model_name}AdminApp(ModelAdmin):
    

    UID   = '{application_name}-{model_name}-app'.lower()
    MODEL = {model_name}
    
    TITLE = '{model_verbose_name}'

    #list of filters fields
    #LIST_FILTER    = [{fields_list}]

    #list of fields to display in the table
    #LIST_DISPLAY   = [{fields_list}]
    
    #fields to be used in the search
    #SEARCH_FIELDS  = [{fields_list}]
    
    #sub models to show in the interface
    #INLINES        = []
    
    #formset of the edit form
    #FIELDSETS      = [{fields_list}]
    
    #read only fields
    #READ_ONLY      = [{fields_list}]
    
    #EDITFORM_CLASS = {model_name}EditFormAdmin    #edit form class
    #CONTROL_LIST   = ControlQueryList #Control to be used in to list the values
    
    ########################################################
    #### ORQUESTRA CONFIGURATION ###########################
    ########################################################
    LAYOUT_POSITION      = LayoutPositions.HOME
    ORQUESTRA_MENU       = 'left{main_app}'
    ORQUESTRA_MENU_ORDER = 0
    ORQUESTRA_MENU_ICON  = 'dollar'
    #AUTHORIZED_GROUPS   = ['superuser'] #groups with authorization to visualize the app
    ########################################################
    
    
    