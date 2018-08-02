try:
    from .controls.control_player import ControlPlayer
except:
    pass

from .controls.control_base     import ControlBase
from .controls.control_file     import ControlFile
from .controls.control_slider   import ControlSlider
from .controls.control_text     import ControlText
from .controls.control_checkbox import ControlCheckBox
from .controls.control_label    import ControlLabel
from .controls.control_button   import ControlButton

from .web.applications import ApplicationsLoader
from .web.middleware   import PyFormsMiddleware

from pyforms_web.organizers import no_columns, segment
from django.template.loader import render_to_string
from .utils import make_lambda_func
from confapp import conf

import uuid, os, inspect, dill, simplejson, filelock

   
class BaseWidget(object):
    """
    The class implements a application form
    """

    TITLE = None #: str: Title of the application.

    #: int or str: Id of the layout handler function registered in the javascript by the function [pyforms.register_layout_place] or Element DOM id in the HTML where the application should be shown.
    LAYOUT_POSITION = None 
    
    #: str: Time in milliseconds to refresh the application.
    REFRESH_TIMEOUT = None

    #: str: Css classes to add to the form.
    CSS = ''

    def __init__(self, *args, **kwargs):
        """
        :param str title: Title of the app. By default will assume the value in the class variable TITLE.
        :param BaseWidget parent_win: Parent BaseWidget

        **Example:**

        .. code:: python

           class FeedViewerApp(BaseWidget):

                TITLE = 'Feed viewer'
                 
                def __init__(self, *args, **kwargs):
                    
                    self._likebtn    = ControlButton(label_visible=False, labeled=True)
                    self._htmlviewer = ControlTemplate('Html', template=self.VIEWER_TEMPLATE)
                    
                    self.formset = ['_likebtn', '_htmlviewer']
        """
        self._formset       = None
        self._splitters     = []
        self._title         = kwargs.get('title', args[0] if len(args)>0 else self.TITLE)
        self._formLoaded    = False
        self._controls      = []
        self._html          = ''
        self._js            = ''
        self._css           = kwargs.get('css', self.CSS)
        self.refresh_timeout= kwargs.get('refresh_timeout', self.REFRESH_TIMEOUT)
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
        Generate the application Form. Return the dict:

        .. code:: python
        
           {
                'code': ...,           # HTML code that will initialize the application.
                'title': ...,          # Title of the application.
                'css': ...,            # Application CSS.
                'app_id': ...,         # Application id.
                'refresh_timeout': ... # Application refresh time.
           }

        """
        
        self._html = ''
        self._js = ''
        self._controls = [c.init_form() for c in self.controls.values()]
        if self._formset != None: 
            self._html += self.generate_panel(self._formset)
            

        parent_code = 'undefined'
        if parent: parent_code = "'{0}'".format(parent.uid)

        extra_data = {'refresh_timeout': self.refresh_timeout, 'messages':self._messages}

        modulename = inspect.getmodule(self).__name__ + '.' + self.__class__.__name__

        self._js = '[{0}]'.format(",".join(self._controls))
        self._html += """
        <script type="text/javascript">pyforms.add_app( new BaseWidget('{2}', '{0}', {1}, {3}, {4}) );</script>
        """.format(modulename, self._js, self.uid, parent_code, simplejson.dumps(extra_data))
        self._formLoaded = True

        self._messages = []
        self.mark_to_update_client()


        res =  {
            'code': self._html,
            'title': self._title,
            'css': self._css,
            'app_id':self.uid, 
            'refresh_timeout':  self.refresh_timeout
        }

       
        return res
        






    def generate_segment(self, row):
        """
        Generate the html to organize the formset in segments
        """
        html  = "<div class='field {field_css}' style='{field_style}' ><div class='ui segment pyforms-segment {css}' style='{style}' >".format(
            css=row.css,
            style=row.style,
            field_css=row.field_css,
            field_style=row.field_style)
        html += self.generate_panel( list(row) )
        html += "</div></div>"
        return html

    def generate_nocolumns(self, formset):
        """
        Generate the html for the no_columns organizer
        """
        layout  = "<div class='row fields {size} {css}' style='{style}' >".format(
            size=self.__get_fields_class(formset),
            css=formset.css,
            style=formset.style
        )
        for row in formset:
            layout += self.generate_panel( row )
        return layout+"</div>"


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

    def generate_control(self, row):
        control = self.controls.get(row, None)
        if control==None:
            if   row==' ':                   return "<div class='field' ></div>"
            if   row.startswith('empty:'):   return "<div class='field {0} wide' ></div>".format(row[6:])
            elif row.startswith('h1:'):      return "<h1 class='field' >{0}</h1>".format(row[3:])
            elif row.startswith('h1-right:'):return "<h1 class='ui right aligned header field' >{0}</h1>".format(row[9:])
            elif row.startswith('h2:'):      return "<h2 class='field' >{0}</h2>".format(row[3:])
            elif row.startswith('h2-right:'):return "<h2 class='ui right aligned header field' >{0}</h2>".format(row[9:])
            elif row.startswith('h3:'):      return "<h3 class='field' >{0}</h3>".format(row[3:])
            elif row.startswith('h3-right:'):return "<h3 class='ui right aligned header field' >{0}</h3>".format(row[9:])
            elif row.startswith('h4:'):      return "<h4 class='field' >{0}</h4>".format(row[3:])
            elif row.startswith('h4-right:'):return "<h4 class='ui right aligned header field' >{0}</h4>".format(row[9:])
            elif row.startswith('h5:'):      return "<h5 class='field' >{0}</h5>".format(row[3:])
            elif row.startswith('h5-right:'):return "<h5 class='ui right aligned header field' >{0}</h5>".format(row[9:])
            elif row.startswith('info:'):    return "<div class='ui info visible message'>{0}</div>".format(row[5:])
            elif row.startswith('warning:'): return "<div class='ui warning visible message'>{0}</div>".format(row[8:])
            elif row.startswith('alert:'):   return "<div class='ui error visible message'>{0}</div>".format(row[6:])
            elif row.startswith('msg:'):     return "<div class='ui message'>{0}</div>".format(row[4:])
            elif row.startswith('text:'):    return "<div class='field'>{0}</div>".format(row[5:])
            elif row == '-':                 return "<div class='ui clearing divider'></div>"
            else:                            return row
        else:
            return str(control)


    def generate_panel(self, formset):
        """  
        Generate a panel for the application form with all the controls: 
        
        :param list formset: formset configuration, used to generate the panel.
        
        **Example:**

        .. code-block:: python
            
           [
                no_columns('_toggle_btn','_copy_btn', '_css_btn'),
                ' ',
                ('empty:twelve','_input'),
                '_text',
                {
                    'a:Free text': [
                        'h1:Header 1',
                        'h2:Header 2',
                        'h3:Header 3',
                        'h4:Header 4',
                        'h5:Header 5',
                        'h1-right:Header 1',
                        'h2-right:Header 2',
                        'h3-right:Header 3',
                        'h4-right:Header 4',
                        'h5-right:Header 5',
                        '-',
                        'Free text here',
                        'msg:Message text',
                        'info:Info message',
                        'warning:Warning message',
                        'alert:Alert message'
                    ],
                    'b:Segments': [
                        'The next example has a segment',
                        segment(
                            '_combo',
                            '_check',
                            css='secondary'
                        ),
                        '_list',
                        '_label'
                    ]
                }
           ]

        - **tuple**: displays the controls horizontally.

        - **list**: displays the controls vertically.   

        - **dict**: displays the controls in Tabs.  

            - Use [a:,b:,c:] prefix to sort the tabs.

        - **'-'**: Draw a vertical line.

        - **' '**: Empty column.

        - **Empty column**: Use ' ', or the prefix 'empty:' + size of the column (ex: one, two, ..., sixteen) to add a empty column.

        - **segment**: Wraps the formset around a segment (Semantic UI segment).
            
            - Call the parameter **css**, to add extra classes to the segment.

        - **no_columns**: Do not apply the fields columns alignments.

        - **Free text**: Do not apply the fields columns alignments.

        - **Message**: By using the prefixes [msg:,info:,warning:,alert:] you will wrap a free message on message box.

        - **Headers**: Use the prefixes [h1:,h2:,h3:,h4:,h5:,h1-right:,h2-right:,h3-right:,h4-right:,h5-right:] on free text.
        
        """
        if formset is None:
            return ''
        elif '=' in formset:
            index = list( formset ).index('=')
            return "<div id='{splitter_id}' class='horizontalSplitter' ><div>{top}</div><div>{bottom}</div></div>".format(
                splitter_id = uuid.uuid4(),
                top         = self.generate_panel(formset[0:index]),
                bottom      = self.generate_panel(formset[index+1:])
            )
        elif '||' in formset:
            index = list( formset ).index('||')
            return "<div id='{splitter_id}' class='verticalSplitter' ><div>{left}</div><div>{right}</div></div>".format(
                splitter_id = uuid.uuid4(),
                left        = self.generate_panel(formset[0:index]),
                right       = self.generate_panel(formset[index+1:])
            )
        elif isinstance(formset, tuple ):
            layout  = "<div class='row fields {0}' >".format(self.__get_fields_class(formset))
            for row in formset:
                layout += self.generate_panel( row )
            return layout+"</div>"

        elif isinstance(formset, no_columns ):
            return self.generate_nocolumns(formset)

        elif isinstance(formset, segment):
            return self.generate_segment(formset)

        elif isinstance(formset, list):
            layout  = ""
            for row in formset:
                if row == ' ': 
                    layout += "<div class='field-empty-space' ></div>"
                else:
                    layout += self.generate_panel( row )
            return layout

        elif isinstance(formset, dict ):
            return self.generate_tabs(formset)

        else:
            return self.generate_control(formset)
  


    
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
        Write a simple message.

        :param str msg: Message to show.
        :param str title: Message title.
        :param str msg_type: Message box css class.
        """
        msg = { 'type': msg_type if msg_type else '', 'messages':msg if isinstance(msg, list) else [msg], 'title':title }
        self._messages.append(msg)
        self.mark_to_update_client()
    def success(self,   msg, title=None):
        """
        Write a success message
        
        :param str msg: Message to show.
        :param str title: Message title.
        """
        self.message(msg, title, msg_type='success')
    def info(self,      msg, title=None):
        """
        Write a info message
        
        :param str msg: Message to show.
        :param str title: Message title.
        """
        self.message(msg, title, msg_type='info')
    def warning(self,   msg, title=None):
        """
        Write a warning message
        
        :param str msg: Message to show.
        :param str title: Message title.
        """
        self.message(msg, title, msg_type='warning');
    def alert(self,     msg, title=None):
        """
        Write a alert message
        
        :param str msg: Message to show.
        :param str title: Message title.
        """
        self.message(msg, title, msg_type='error')

    def message_popup(self, msg, title='', buttons=None, handler=None, msg_type='success'):
        """
        Show a popup message window
        
        :param str msg: Message to show.
        :param str title: Message title.
        :param list(str) buttons: List of buttons labels to create in the popup window.
        :param str msg_type: Message box css class.
        :param method handler: Method that will handle the press of the buttons.
    
        .. code:: python
           
           # Handler
           def button_pressed_btn(popup=[Popup instance], button=[Label of the pressed button]):
                ...

        """
        self._active_popup_msg = PopupWindow(title, msg, buttons, handler, msg_type='success', parent_win=self)
        return self._active_popup_msg
    def success_popup(self, msg, title='', buttons=None, handler=None):
        """
        Show a popup success message window
        
        :param str msg: Message to show.
        :param str title: Message title.
        :param list(str) buttons: List of buttons labels to create in the popup window.
        :param method handler: Method that will handle the press of the buttons.
        """
        return self.message_popup(msg, title, buttons, handler, msg_type='success')
    def info_popup(self, msg, title='', buttons=None, handler=None):
        """
        Show a popup info message window
        
        :param str msg: Message to show.
        :param str title: Message title.
        :param list(str) buttons: List of buttons labels to create in the popup window.
        :param method handler: Method that will handle the press of the buttons.
        """
        return self.message_popup(msg, title, buttons, handler, msg_type='info')
    def warning_popup(self, msg, title='', buttons=None, handler=None):
        """
        Show a popup warning message window
        
        :param str msg: Message to show.
        :param str title: Message title.
        :param list(str) buttons: List of buttons labels to create in the popup window.
        :param method handler: Method that will handle the press of the buttons.
        """
        return self.message_popup(msg, title, buttons, handler, msg_type='warning')
    def alert_popup(self, msg, title='', buttons=None, handler=None):
        """
        Show a popup alert message window
        
        :param str msg: Message to show.
        :param str title: Message title.
        :param list(str) buttons: List of buttons labels to create in the popup window.
        :param method handler: Method that will handle the press of the buttons.
        """
        return self.message_popup(msg, title, buttons, handler, msg_type='alert')

    
    ##########################################################################
    ############ WEB functions ###############################################
    ##########################################################################
    

    def __get_fields_class(self, row):
        """
        Get the css class to be used on the controls organization
        """
        if isinstance(row, no_columns): return 'no-alignment'

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

        lock = filelock.FileLock(conf.PYFORMS_WEB_LOCKFILE)
        with lock.acquire(timeout=4):
            with open(app_path, 'wb') as f: 
                dill.dump(self, f)

    def execute_js(self, code):
        """
        This function executes a javascript remotely on the client side.
        
        :param str code: Javascript code to execute.
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

    def deserialize_form(self, params):
        """
        Load the json parameters sent by the client side
        
        :param dict params: Data to load.
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
        Serialize the Form to a control.

        Returns:
            dict: Data representings the current state of the application.
        """
        res = {
            'uid':              self.uid, 
            'layout_position':  self.LAYOUT_POSITION if hasattr(self, 'LAYOUT_POSITION') else 5,
            'title':            self.title,
            'close_widget':     self._close_widget,
            'js-code':          list(self._js_code2execute),
            'refresh_timeout':  self.refresh_timeout
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
        
        :param User params: User to availuate the permissions.
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
        
        :param User params: User to availuate the permissions.
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
        Event called every X time defined by REFRESH_TIMEOUT variable.
        """
        pass



    ############################################################################
    ############ Properties ####################################################
    ############################################################################

    
    @property
    def controls(self):
        """
        Returns all the form controls from the the module
        """
        result = {}
        for name, var in vars(self).items():
            if isinstance(var, ControlBase):
                var._name   = name
                var.parent  = self
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
        Return and set the controls organization in the form
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

    @property
    def refresh_timeout(self):
        """
        Return a boolean indicating if the form is visible or not 
        """
        return self._refresh_timeout

    @refresh_timeout.setter
    def refresh_timeout(self, value): self._refresh_timeout = value

    

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
    LAYOUT_POSITION = conf.LAYOUT_NEW_WINDOW

    def __init__(self, title, msg, buttons, handler, msg_type, parent_win=None):
        BaseWidget.__init__(self, title, parent_win=parent_win)
        
        self._label = ControlLabel(default=msg)
        #self._label.css = msg_type
       
        if buttons:
            buttons_formset = []
            for i, b in enumerate(buttons):
                name = 'button_{0}'.format(i)
                setattr(self, name, ControlButton(b))
                getattr(self, name ).value = make_lambda_func(handler, popup=self, button=b)
                buttons_formset.append(name)
    
        self.formset = ['_label'] + [no_columns(buttons_formset)]
       