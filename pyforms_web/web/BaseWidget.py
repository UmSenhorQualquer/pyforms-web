
from pyforms_web.web.Controls.ControlBase import ControlBase
from pyforms_web.web.Controls.ControlFile import ControlFile
from pyforms_web.web.Controls.ControlSlider import ControlSlider
from pyforms_web.web.Controls.ControlText import ControlText
from pyforms_web.web.Controls.ControlCheckBox import ControlCheckBox
from pyforms_web.web.Controls.ControlLabel import ControlLabel
try:
    from pyforms_web.web.Controls.ControlPlayer import ControlPlayer
except:
    print("ControlPlayer is not available")
from pyforms_web.web.Controls.ControlButton import ControlButton
from pyforms_web.web.django_pyforms.Applications import ApplicationsLoader
from pyforms_web.web.django_pyforms.middleware import PyFormsMiddleware
import uuid, os, shutil, base64, inspect
import base64, dill, simplejson, filelock
from pyforms import conf
from django.template.loader import render_to_string

from pyforms_web.web.utils import make_lambda_func

class BaseWidget(object):
    """
    The class implements a application window
    """
    TITLE           = None
    LAYOUT_POSITION = None
    
    FORM_NO_ROW_ALIGNMENT = 0

    REFRESH_TIMEOUT = None #time in milliseconds to refresh the application

    def __init__(self, *args, **kwargs):
        self._formset       = None
        self._splitters     = []
        self._title         = kwargs.get('title', args[0] if len(args)>0 else self.TITLE)
        self._formLoaded    = False
        self._controls      = []
        self._html          = ''
        self._js            = ''
        self._close_widget  = False

        self.init_form_result = None
         
        self._uid =  self.UID if hasattr(self, 'UID') else str(uuid.uuid4())

        self._messages        = []
        self._js_code2execute = [];

        self.parent = kwargs.get('parent_win', None)
        self.is_new_app = True

        PyFormsMiddleware.add(self)



    
    ############################################################################
    ############ FUNCTIONS #####################################################
    ############################################################################

    def init_form(self, parent=None):
        """
        Generate the module Form
        """
        
        self._html = ''
        self._js = ''
        self._controls = [c.init_form() for c in self.controls.values()]
        if self._formset != None: 
            self._html += self.generate_panel(self._formset, add_field_class=False)
            

        parent_code = 'undefined'
        if parent: parent_code = "'{0}'".format(parent.uid)

        extra_data = {'refresh_timeout': self.REFRESH_TIMEOUT, 'messages':self._messages}

        modulename = inspect.getmodule(self).__name__ + '.' + self.__class__.__name__

        self._js = '[{0}]'.format(",".join(self._controls))
        self._html += """
        <script type="text/javascript">pyforms.add_app( new BaseWidget('{2}', '{0}', {1}, {3}, {4}) );</script>
        """.format(modulename, self._js, self.uid, parent_code, simplejson.dumps(extra_data))
        self._formLoaded = True

        self._messages = []
        self.mark_to_update_client()

        return {'code': self._html, 'title': self._title, 'app_id':self.uid, 'refresh_timeout':  self.REFRESH_TIMEOUT }
        

    def generate_tabs(self, formsetdict):
        """
        Generate QTabWidget for the module form
        @param formset: Tab form configuration
        @type formset: dict
        """
        tabs_head = ""
        tabs_body = ""
        tab_id = uuid.uuid4()

        for index, (key, item) in enumerate( sorted(formsetdict.items()) ):
            active = 'active' if index==0 else ''
            tabs_body += "<div class='ui bottom attached {3} tab segment' data-tab='{4}-{5}'  id='{0}-tab{1}' >{2}</div>".format(tab_id, index, self.generate_panel(item), active, tab_id, index)
            tabs_head += "<div class='{1} item' data-tab='{2}-{3}' >{0}</div>".format(key[key.find(':')+1:], active, tab_id, index)

        return """<div id='{0}' class='ui top attached tabular menu' >{1}</div>{2}<script type='text/javascript'>$('#{0}.menu .item').tab();</script>""".format(tab_id, tabs_head, tabs_body)

    

    def generate_panel(self, formset, add_field_class=True):
        """  
        Generate a panel for the module form with all the controls formset format example: 
        
        .. code-block:: python

            [
                ('_video', '_arenas', '_run'), 
                {
                    "Player": [
                        '_threshold',
                        "_player",
                        "=",
                        "_results",
                        "_query"
                    ], 
                    "Background image":[
                        (' ', '_selectBackground', '_paintBackground'),
                        '_image'
                    ]
                }, 
                "_progress"
            ]  
        
        **tuple**: displays the controls horizontally.  

        **list**: displays the controls vertically.   

        **dict**: displays the controls in Tabs.   

        **'||'**: splits the controls with a horizontal line.   

        **'='**: splits the controls with a vertical line.   
        
        """
        control = ""
        if '=' in formset:
            tmp = list( formset )
            index = tmp.index('=')
            firstPanel = self.generate_panel(formset[0:index])
            secondPanel = self.generate_panel(formset[index+1:])
            splitter_id =uuid.uuid4()
            self._splitters.append( splitter_id )
            control = ("<div id='%s' class='horizontalSplitter' ><div>" + firstPanel + "</div><div>" + secondPanel + "</div></div>") % ( splitter_id, )
            return control
        elif '||' in formset:
            tmp = list( formset )
            index = tmp.index('||')
            firstPanel = self.generate_panel(formset[0:index])
            secondPanel = self.generate_panel(formset[index+1:])
            splitter_id = uuid.uuid4()
            self._splitters.append( splitter_id )
            control = ("<div id='%s' class='verticalSplitter' ><div>" + firstPanel + "</div><div>" + secondPanel + "</div></div>") % ( splitter_id, )
            return control
        
        layout = ""
        if type(formset) is tuple:
            for row in formset:
                if isinstance(row, (list, tuple)):
                    panel = self.generate_panel( row )
                    layout += "<div class='rows %s' >%s</div>" % ('field' if add_field_class else '', panel)
                elif row == " ":
                    layout += "<div class='field' ></div>"
                elif type(row) is dict and row.get('is-segment', False):
                    seg = self.generate_segments(row)
                    layout += seg
                elif type(row) is dict:
                    tabs = self.generate_tabs(row)
                    layout += tabs
                else:
                    control = self.controls.get(row, None)
                    if control==None:
                        if not isinstance(row, str): continue
                    
                        if row.startswith('info:'): layout += "<span class='info' >%s</span>" % row[5:]
                        elif row.startswith('h1:'): layout += "<h1>%s</h1>" % row[3:]
                        elif row.startswith('h2:'): layout += "<h2>%s</h2>" % row[3:]
                        elif row.startswith('h3:'): layout += "<h3>%s</h3>" % row[3:]
                        elif row.startswith('h4:'): layout += "<h4>%s</h4>" % row[3:]
                        elif row.startswith('h5:'): layout += "<h5>%s</h5>" % row[3:]
                        elif row.startswith('warning:'): layout += "<div class='ui warning visible  message'>%s</div>" % row[8:]
                        elif row.startswith('alert:'):   layout += "<div class='ui alert message'>%s</div>" % row[6:]
                        else: layout += "<div class='ui message'>%s</div>" % row
                    else:
                        #self._controls.append( control.init_form() )
                        layout += "%s" % control
        elif type(formset) is list:
            for row in formset:
                if isinstance(row, tuple):
                    panel   = self.generate_panel( row )
                    layout += "<div class='row fields {1}' >{0}</div>".format(panel, self.__get_fields_class(row))
                elif isinstance(row, list):
                    panel   = self.generate_panel( row )
                    layout += "<div class='row fields' >{0}</div>".format(panel)
                elif row == " ":
                    layout += "<div class='field-empty-space' ></div>"
                elif type(row) is dict and row.get('is-segment', False):
                    seg = self.generate_segments(row)
                    layout += seg
                elif type(row) is dict:
                    tabs    = self.generate_tabs(row)
                    layout += tabs
                else:
                    control = self.controls.get(row, None)
                    if control==None:
                        
                        if not isinstance(row, str): continue
                    
                        if row.startswith('info:'): layout += "<span class='info' >%s</span>" % row[5:]
                        elif row.startswith('h1:'): layout += "<h1>%s</h1>" % row[3:]
                        elif row.startswith('h1-right:'): layout += "<h1 class='ui right floated header' >%s</h1>" % row[9:]
                        elif row.startswith('h2:'): layout += "<h2>%s</h2>" % row[3:]
                        elif row.startswith('h2-right:'): layout += "<h2 class='ui right floated header' >%s</h2>" % row[9:]
                        elif row.startswith('h3:'): layout += "<h3>%s</h3>" % row[3:]
                        elif row.startswith('h4:'): layout += "<h4>%s</h4>" % row[3:]
                        elif row.startswith('h5:'): layout += "<h5>%s</h5>" % row[3:]
                        elif row.startswith('warning:'):    layout += "<div class='ui warning visible  message'>%s</div>" % row[8:]
                        elif row.startswith('alert:'):      layout += "<div class='ui alert error message'>%s</div>" % row[6:]
                        elif row == '-': layout += '<div class="ui clearing divider"></div>'
                        else: layout += "<div class='ui message'>%s</div>" % row
                    else:
                        #self._controls.append( control.init_form() )
                        layout += str(control)
        
        return layout


    
    def save_form(self, data={}, path=None):
        """
        Called to save the form  

        TODO
        """
        pass

    def load_form(self, data, path=None):
        """
        Called to load a form  
        
        TODO
        """
        pass
    
    def save_window(self):
        pass

    def load_window(self):
        pass

    def load_form_filename(self, filename):
        """
        Load the forms from a file  
        
        TODO
        """
        pass

    def close(self):
        """
        Close the application
        """
        self.mark_to_update_client()
        self._close_widget = True

    def message(self, msg, title=None, msg_type=None):
        """
        Write a simple message
        """
        msg = { 'type': msg_type if msg_type else '', 'messages':msg if isinstance(msg, list) else [msg], 'title':title }
        self._messages.append(msg)
        self.mark_to_update_client()
    def success(self,   msg, title=None):
        """
        Write a success message
        """
        self.message(msg, title, msg_type='success')
    def info(self,      msg, title=None):
        """
        Write a info message
        """
        self.message(msg, title, msg_type='info')
    def warning(self,   msg, title=None):
        """
        Write a warning message
        """
        self.message(msg, title, msg_type='warning');
    def alert(self,     msg, title=None):
        """
        Write a alert message
        """
        self.message(msg, title, msg_type='error')

    def message_popup(self, msg, title='', buttons=None, handler=None, msg_type='success'):
        """
        Show a popup message window
        """
        self._active_popup_msg = PopupWindow(title, msg, buttons, handler, msg_type='success', parent_win=self)
        return self._active_popup_msg
    def success_popup(self, msg, title='', buttons=None, handler=None):
        """
        Show a popup success message window
        """
        return self.message_popup(msg, title, buttons, handler, msg_type='success')
    def info_popup(self, msg, title='', buttons=None, handler=None):
        """
        Show a popup info message window
        """
        return self.message_popup(msg, title, buttons, handler, msg_type='info')
    def warning_popup(self, msg, title='', buttons=None, handler=None):
        """
        Show a popup warning message window
        """
        return self.message_popup(msg, title, buttons, handler, msg_type='warning')
    def alert_popup(self, msg, title='', buttons=None, handler=None):
        """
        Show a popup alert message window
        """
        return self.message_popup(msg, title, buttons, handler, msg_type='alert')

    
    ##########################################################################
    ############ WEB functions ###############################################
    ##########################################################################

    def generate_segments(self, formsetdict):
        """
        Generate the html to organize the formset in segments
        """
        html = ''
        for key, item in sorted(formsetdict.items()):
            if item==True: continue
            
            html += "<h2 class='ui header' >{0}</h2>".format(key[key.find(':')+1:])
            html += "<div class='ui segment pyforms-segment' >"
            html += self.generate_panel(item, add_field_class=False)
            html += "</div>"
        return html

    def __get_fields_class(self, row):
        """
        Get the css class to be used on the Controls organization
        """
        if len(row)>=1 and row[0]==self.FORM_NO_ROW_ALIGNMENT: return 'no-alignment'

        if   len(row)==2: return 'two'
        elif len(row)==3: return 'three'
        elif len(row)==4: return 'four'
        elif len(row)==5: return 'five'
        elif len(row)==6: return 'six'
        elif len(row)==7: return 'seven'
        elif len(row)==8: return 'eight'
        elif len(row)==9: return 'nine'
        elif len(row)==10: return 'ten'
        elif len(row)==11: return 'eleven'
        elif len(row)==12: return 'twelve'
        elif len(row)==13: return 'thirteen'
        elif len(row)==14: return 'fourteen'
        elif len(row)==15: return 'fiveteen'
        elif len(row)==16: return 'sixteen'
        elif len(row)==17: return 'seventeen'
        elif len(row)==18: return 'eighteen'
        elif len(row)==19: return 'nineteen'
        elif len(row)==20: return 'twenty'
        elif len(row)==21: return 'twentyone'
        elif len(row)==22: return 'twentytwo'
        else: return ''

    def commit(self):
        """
        Save all the application updates to a file, so it can be used in the next session. 
        """
        for key, item in self.controls.items(): item.commit()

        user = PyFormsMiddleware.user()
        # save the modifications
        userpath = os.path.join(
            conf.PYFORMS_WEB_APPS_CACHE_DIR,
            '{0}-{1}'.format(user.pk, user.username) 
        )
        if not os.path.exists(userpath): os.makedirs(userpath)

        app_path = os.path.join(userpath, "{0}.app".format(self.uid) )

        lock = filelock.FileLock("lockfile.txt")
        with lock.acquire(timeout=4):
            with open(app_path, 'wb') as f: 
                dill.dump(self, f)

    def execute_js(self, code):
        """
        This function executs a javascript on the client side
        """
        self._js_code2execute.append(code)

    

    def mark_to_update_client(self):
        """
        Used to flag pyforms that the application was updated and the updates should be sent to the client side
        """
        request = PyFormsMiddleware.get_request()
        if  request is not None and \
            hasattr(request,'updated_apps'):
            request.updated_apps.add_top(self)

    def load_serialized_form(self, params):
        """
        Load the json parameters sent by the client side
        """
        widgets = []

        if hasattr(self, 'parent') and isinstance(self.parent, (str,str)):
            self.parent = PyFormsMiddleware.get_instance(self.parent)
    

        for key, value in params.items():
            control = self.controls.get(key, None)
            if control!=None: 
                if control.__class__.__name__=='ControlEmptyWidget':
                    widgets.append( (control, params[key]) )
                else:
                    control.deserialize(params[key])
        
        for control, data in widgets: control.deserialize(data)

        if 'event' in params.keys():
            control = params['event']['control']
            if control in self.controls.keys():
                item = self.controls[control]
                func = getattr(item, params['event']['event'])
                func()
            elif control=='self':
                func = getattr(self, params['event']['event'])
                func()                  

                    

    def serialize_form(self):
        """
        Serialize the Form to a control
        """
        res = {
            'uid':              self.uid, 
            'layout_position':  self.LAYOUT_POSITION if hasattr(self, 'LAYOUT_POSITION') else 5,
            'title':            self.title,
            'close_widget':     self._close_widget,
            'js-code':          list(self._js_code2execute)
        }
        
        self._js_code2execute = []
        
        if len(self._messages)>0: 
            res.update({'messages': self._messages})
            self._messages = []

        for key, item in self.controls.items():

            if item.was_updated:
                res[item._name] = item.serialize()
                try:
                    if isinstance(item, ControlPlayer ) and item._value!=None and item._value!='':
                        item._value.release() #release any open video
                except:
                    pass
        
        return res


    @classmethod
    def has_permissions(cls, user):
        """
        This class method, verifies if a user has permissions to execute the application
        """
        if hasattr(cls, 'AUTHORIZED_GROUPS'):
            if user.is_superuser and 'superuser' in cls.AUTHORIZED_GROUPS: 
                return True
            if user.groups.filter(name__in=cls.AUTHORIZED_GROUPS).exists():
                return True
        else:
            return True

        return False
        
    def has_session_permissions(self, user):
        """
        It verifies if a user has permissions to execute the application during the runtime.
        """
        return True



    ##########################################################################
    ############ EVENTS ######################################################
    ##########################################################################

    def before_close_event(self):
        """
        Function called before the Form is closed.  
        
        TODO
        """
        pass

    ##########################################################################
    ############ WEB events ##################################################
    ##########################################################################

    def refresh_event(self):
        """
        Event called every X time defined by refresh_timeout variable.
        """
        pass



    ############################################################################
    ############ Properties ####################################################
    ############################################################################

    
    @property
    def controls(self):
        """
        Return all the form controls from the the module
        """
        result = {}
        for name, var in vars(self).items():
            if isinstance(var, ControlBase):
                var.parent  = self
                var._name   = name
                result[name]= var

        return result

    @property
    def form(self): 
        """
        Return the basewidget html. The html is based on the 'basewidget-template.html' template
        """
        return render_to_string( 
            os.path.join('pyforms', 'basewidget-template.html'), 
            {'application_html': self._html, 'application_id': self.uid}
        )

    @property
    def title(self):
        """
        Return and set the title of the application
        """
        return self._title

    @title.setter
    def title(self, value): self._title = value

    @property
    def mainmenu(self):
        """
        Return and set the mainmenu  
        
        TODO
        """
        return None

    @mainmenu.setter
    def mainmenu(self, value):
        pass


    @property
    def formset(self):
        """
        Return and set the Controls organization in the form
        """
        return self._formset

    @formset.setter
    def formset(self, value): self._formset = value


    @property
    def uid(self):
        """
        Return and set the application unique identifier
        """
        return self._uid

    @uid.setter
    def uid(self, value): self._uid = value

    @property
    def visible(self):
        """
        Return a boolean indicating if the form is visible or not 
        """
        return True


    ############################################################################
    ############ WEB Properties ################################################
    ############################################################################
    
        
    @property
    def js(self):
        """
        Return the form javascript
        """
        return self._js
    
    
    
   
    
    
    











class PopupWindow(BaseWidget):
    LAYOUT_POSITION = 4

    def __init__(self, title, msg, buttons, handler, msg_type, parent_win=None):
        BaseWidget.__init__(self, title, parent_win=parent_win)
        
        self._label = ControlLabel(default=msg)
        #self._label.css = msg_type
       
        if buttons:
            buttons_formset = [0]
            for i, b in enumerate(buttons):
                name = 'button_{0}'.format(i)
                setattr(self, name, ControlButton(b))
                getattr(self, name ).value = make_lambda_func(handler, popup=self, button=b)
                buttons_formset.append(name)
    
        self.formset = ['_label'] + [tuple(buttons_formset)]
       