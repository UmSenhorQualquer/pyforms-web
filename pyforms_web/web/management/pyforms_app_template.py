from confapp import conf
from pyforms_web.widgets.django import ModelAdminWidget

from {application_name}.models import {model_name}

class {model_name}AdminApp(ModelAdminWidget):
    

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
    
    #EDITFORM_CLASS = {model_name}ModelFormWidget    #edit form class
    #CONTROL_LIST   = ControlQueryList #Control to be used in to list the values
    
    #AUTHORIZED_GROUPS   = ['superuser'] #groups with authorization to visualize the app
    
    ########################################################
    #### ORQUESTRA CONFIGURATION ###########################
    ########################################################
    LAYOUT_POSITION      = conf.ORQUESTRA_HOME
    ORQUESTRA_MENU       = 'left{main_app}'
    ORQUESTRA_MENU_ORDER = 0
    ORQUESTRA_MENU_ICON  = 'dollar'
    ########################################################
    
    
    