from confapp import conf
from pyforms_web.widgets.django import ModelAdminWidget

from tutorial.models import Departments

class DepartmentsAdminApp(ModelAdminWidget):
    

    UID   = 'tutorial-Departments-app'.lower()
    MODEL = Departments
    
    TITLE = 'Departmentss'

    #list of filters fields
    #LIST_FILTER    = ['deptemp','deptmanager','dept_no','dept_name']

    #list of fields to display in the table
    #LIST_DISPLAY   = ['deptemp','deptmanager','dept_no','dept_name']
    
    #fields to be used in the search
    #SEARCH_FIELDS  = ['deptemp','deptmanager','dept_no','dept_name']
    
    #sub models to show in the interface
    #INLINES        = []
    
    #formset of the edit form
    FIELDSETS      = [('deptemp','deptmanager'),'dept_no','dept_name']
    
    #read only fields
    #READ_ONLY      = ['deptemp','deptmanager','dept_no','dept_name']
    
    #EDITFORM_CLASS = DepartmentsModelFormWidget    #edit form class
    #CONTROL_LIST   = ControlQueryList #Control to be used in to list the values
    
    #AUTHORIZED_GROUPS   = ['superuser'] #groups with authorization to visualize the app
    
    ########################################################
    #### ORQUESTRA CONFIGURATION ###########################
    ########################################################
    LAYOUT_POSITION      = conf.ORQUESTRA_HOME
    ORQUESTRA_MENU       = 'left'
    ORQUESTRA_MENU_ORDER = 0
    ORQUESTRA_MENU_ICON  = 'dollar'
    ########################################################
    
    
    