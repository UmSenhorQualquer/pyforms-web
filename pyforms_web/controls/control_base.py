import uuid
from confapp import conf
from pyforms_web.web.middleware import PyFormsMiddleware

class ControlBase(object):
    """
    Basis class from where all the Controls inherit from.
    """

    def __init__(self, *args, **kwargs):
        """
        :param str label: Control label.
        :param str helptext: Set the help text. Default = None.
        :param str default: Set the value. Default = None.
        :param bool visible: Set the control visible or hidden. Default = True.
        :param bool error: Mark the control as having and error. Default = False.
        :param str css: Extra css classes to add to the control.
        :param str field_css: Extra css classes to add to the field dive that encapsulates the control.
        :param str style: Extra style to add to the control.
        :param str field_style: Extra style to add to the field div that encapsulates the control.
        :param bool enabled: Set the control enabled or disabled. Default = True.
        :param bool readonly: Set the control as read only. Default = False.
        :param bool label_visible: Hide or show the label. Default = True.
        """
        self.uid            = uuid.uuid4()
        self._name          = ""    # variable name. It is updated in runtime
        self._parent        = None  # parent basewidget. It is updated in runtime
        self._update_client = False # flag that indicate if the Control should be updated

        self._help          = kwargs.get('helptext', None)
        self._value         = kwargs.get('default',  None)
        self._label         = kwargs.get('label', args[0] if len(args)>0 else '')
        self._visible       = kwargs.get('visible', True)
        self._error         = kwargs.get('error', False)
        self._css           = kwargs.get('css', None)
        self._field_css     = kwargs.get('field_css', None)
        self._style         = kwargs.get('style', None)
        self._field_style   = kwargs.get('field_style', None)
        self._enabled       = kwargs.get('enabled', True)
        self._enabled       = not kwargs.get('readonly', False)
        self._label_visible = kwargs.get('label_visible', True)
        
        if 'changed_event' in kwargs:
            self.changed_event = kwargs['changed_event']

            

    def __repr__(self): return str(self._value)

    def __str__(self): 
        """
        Return the control html
        """
        return "<span id='place-{0}-{1}' />".format(self.parent.uid if self.parent else '', self._name)


    ##########################################################################
    ############ Functions ####################################################
    ##########################################################################

    def update_control_event(self):
        pass

    def init_form(self):
        """
        Render the control js
        """     
        return ""
        
    def load_form(self, data, path=None):
        """
        Load a value from the dict variable
        @param data: dictionary with the value of the Control
        """
        if 'value' in data: self.value = data['value']

    def save_form(self, data, path=None):
        """
        Save a value to dict variable
        @param data: dictionary with to where the value of the Control will be added
        """
        if self.value: data['value'] = self.value

    def show(self): 
        """
        Show the control
        """
        self.mark_to_update_client()
        self._visible = True

    def hide(self): 
        """
        Hide the control
        """
        self.mark_to_update_client()
        self._visible = False

    def add_popup_submenu(self, label, submenu=None):
        pass

    def add_popup_menu_option(self, label, function_action=None, key=None, icon=None, submenu=None):
        """
        Add an option to the Control popup menu
        @param label:           label of the option.
        @param function_action:  function called when the option is selected.
        @param key:             shortcut key
        @param icon:            icon
        """
        pass

    ##########################################################################
    ############ Funcions for WEB version ####################################
    ##########################################################################

    def serialize(self):
        """
        Serialize the control data.

        Returns:
            dict: Serialized data.
        """
        res = { 
            'name':     self.name, 
            'value':    self.value,
            'label':    str(self._label if self._label else ''),
            'help':     str(self._help if self._help else ''),
            'visible':  self._visible,
            'error':    self._error,
            'enabled':  self._enabled,
            'label_visible': self._label_visible
        }
        if self._css is not None: 
            res.update({'css':self._css})

        if self._field_css is not None: 
            res.update({'field_css':self._field_css})

        if self._style is not None: 
            res.update({'style':self._style})

        if self._field_style is not None: 
            res.update({'field_style':self._field_style})

        return res

    def deserialize(self, properties):
        """
        Serialize the control data.
        
        :param dict properties: Serialized data to load.
        """
        self.value    = properties.get('value',None)
        #self._label   = properties.get('label','')
        #self._help    = properties.get('help','')
        #self._visible = properties.get('visible',True)

    
    def clean_field(self):
        """
        Validate the value of the Control.
        """
        pass
    

    def commit(self):
        # don't send any apdate to the client
        self._update_client = False

    def mark_to_update_client(self):
        """
        Mark the control to update in the client side.
        """
        self._update_client = True
        
        request = PyFormsMiddleware.get_request()
        if  self.parent is not None and \
            request is not None and \
            hasattr(request,'updated_apps'):
            request.updated_apps.add_top(self.parent)

    ##########################################################################
    ############ Events ######################################################
    ##########################################################################

    def changed_event(self):
        """
        Event called when the control value is changed.
        """
        pass

    def about_to_show_contextmenu_event(self): pass

    ############################################################################
    ############ Properties ####################################################
    ############################################################################
    
    ##########################################################################
    # Set the Control enabled or disabled
    
    @property
    def enabled(self):
        """
        Set the control enabled or disabled.
        """
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        if self._enabled!=value:
            self._enabled = value
            self.mark_to_update_client()

    ##########################################################################
    # Return or update the value of the control

    @property
    def value(self):
        """
        Set or return de control value.
        """
        return self._value

    @value.setter
    def value(self, value):
        oldvalue = self._value
        if oldvalue!=value: 
            self._value = value
            self.mark_to_update_client()
            self.changed_event()

    @property
    def name(self):
        """
        Set or return the name of the control.
        """
        return self._name

    @name.setter
    def name(self, value):
        if self._name!=value: self.mark_to_update_client()
        self._name = value

    ##########################################################################
    # Return or update the label of the Control

    @property
    def label(self):
        """
        Set or return the label of the control.
        """
        return self._label

    @label.setter
    def label(self, value): 
        if self._label!=value: self.mark_to_update_client()
        self._label = value

    ##########################################################################
    # Parent window

    @property
    def parent(self):
        """
        Set or return the control window.
        """
        return self._parent

    @parent.setter
    def parent(self, value): 
        if self._parent!=value: self.mark_to_update_client()
        self._parent = value

    ############################################################################

    @property
    def visible(self):
        """
        Set if the control is visible.
        """
        return self._visible
    
    @property
    def help(self): 
        """
        Set or return the help text of the control.
        """
        return self._help.replace('\n', '&#013;') if self._help else ''

    @property
    def error(self):
        """
        Set or return the error of the control.
        """
        return self._error
    @error.setter
    def error(self, value): 
        if value!=self._error: self.mark_to_update_client()
        self._error = value

    @property
    def label_visible(self):
        """
        Set or return the label visibility of the control.
        """
        return self._label_visible

    @label_visible.setter
    def label_visible(self, value):
        if value!=self._label_visible: self.mark_to_update_client()
        self._label_visible = value

    @property
    def readonly(self):
        """
        Set or return the control readonly mode.
        """
        return not self.enabled

    @readonly.setter
    def readonly(self, value): self.enabled = not value

    @property
    def css(self):
        """
        Set or return the extra css of the control.
        """
        return self._css
    @css.setter
    def css(self, value): 
        if value!=self._css: self.mark_to_update_client()
        self._css = value
    @property
    def field_css(self):
        """
        Set or return the extra css of the field div that encapsulates the control.
        """
        return self._field_css
    @field_css.setter
    def field_css(self, value): 
        if value!=self._css: self.mark_to_update_client()
        self._field_css = value



    @property
    def style(self):
        """
        Set or return the style of the control.
        """
        return self._style
    @style.setter
    def style(self, value): 
        if value: self.mark_to_update_client()
        self._style = value

    @property
    def field_style(self):
        """
        Set or return the style of the field div that encapsulate the control.
        """
        return self._field_style
    @field_style.setter
    def field_style(self, value): 
        if value: self.mark_to_update_client()
        self._field_style = value


    ##########################################################################
    ############ Properties just for the WEB version #########################
    ##########################################################################

    @property
    def control_id(self):
        """
        Return the control id.
        """
        return "{0}-{1}".format(self._parent.uid, self.name)

    @property
    def place_id(self):
        """
        Return the place control id.
        """
        return 'place-'+self.control_id

    @property
    def was_updated(self):
        """
        Return the if the control is marked as updated.
        """
        return self._update_client
