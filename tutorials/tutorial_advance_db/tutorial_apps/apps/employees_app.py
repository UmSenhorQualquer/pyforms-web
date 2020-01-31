from confapp import conf
from pyforms_web.widgets.django import ModelAdminWidget

from tutorial.models import Employees

class EmployeesAdminApp(ModelAdminWidget):
    

    UID   = 'tutorial-Employees-app'.lower()
    MODEL = Employees
    
    TITLE = 'Employeess'

    #list of filters fields
    #LIST_FILTER    = ['deptemp','deptmanager','salaries','titles','emp_no','birth_date','first_name','last_name','gender','hire_date']

    #list of fields to display in the table
    #LIST_DISPLAY   = ['deptemp','deptmanager','salaries','titles','emp_no','birth_date','first_name','last_name','gender','hire_date']
    
    #fields to be used in the search
    #SEARCH_FIELDS  = ['deptemp','deptmanager','salaries','titles','emp_no','birth_date','first_name','last_name','gender','hire_date']
    
    #sub models to show in the interface
    #INLINES        = []
    
    #formset of the edit form
    #FIELDSETS      = ['deptemp','deptmanager','salaries','titles','emp_no','birth_date','first_name','last_name','gender','hire_date']
    
    #read only fields
    #READ_ONLY      = ['deptemp','deptmanager','salaries','titles','emp_no','birth_date','first_name','last_name','gender','hire_date']
    
    #EDITFORM_CLASS = EmployeesModelFormWidget    #edit form class
    #CONTROL_LIST   = ControlQueryList #Control to be used in to list the values
    
    #AUTHORIZED_GROUPS   = ['superuser'] #groups with authorization to visualize the app
    
    ########################################################
    #### ORQUESTRA CONFIGURATION ###########################
    ########################################################
    LAYOUT_POSITION      = conf.ORQUESTRA_HOME
    ORQUESTRA_MENU       = 'left>DepartmentsAdminApp'
    ORQUESTRA_MENU_ORDER = 0
    ORQUESTRA_MENU_ICON  = 'dollar'
    ########################################################
    
    
    