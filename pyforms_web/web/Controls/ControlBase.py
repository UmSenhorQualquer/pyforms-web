import uuid
from pysettings import conf
from pyforms_web.web.djangoapp.middleware import PyFormsMiddleware

class ControlBase(object):


	def __init__(self, label = "", defaultValue = None, helptext=''):
		self._name      = ""
		self._help      = helptext
		self._value     = defaultValue
		self._parent    = None
		self._label     = label
		self._visible   = True
		self._error 	= False
		self._css 		= None
		self.uid = uuid.uuid4()
		self._controlHTML = ""

		self._update_client = False

	def init_form(self):
		self._controlHTML = "<div id='id{0}' ><input type='text' id='{1}' /></div>".format( self.uid, self._name )
		return self._controlHTML

	def serialize(self):
		res = { 
			'name':     self.__class__.__name__, 
			'value':    self.value,
			'label':    self._label if self._label else '',
			'help':     self._help if self._help else '',
			'visible':  self._visible,
			'error': 	self._error
		}
		if self._css: res.update({'css':self._css})
		return res

	def deserialize(self, properties):
		self.value    = properties.get('value',None)
		self._label   = properties.get('label','')
		self._help    = properties.get('help','')
		self._visible = properties.get('visible',True)

		
			
	def finish_editing(self): self.update_control()

	def update_control(self): pass

	def changed_event(self): pass

	def load(self, data):
		if 'value' in data: self.value = data['value']

	def save(self, data):
		if self.value: data['value'] = self.value


	def show(self): 
		self.mark_to_update_client()
		self._visible = True

	def hide(self): 
		self.mark_to_update_client()
		self._visible = False

	def commit(self):
		# don't send any apdate to the client
		self._update_client = False

	def mark_to_update_client(self):
		self._update_client = True
		
		if 	self.parent is not None and \
			self.http_request is not None and \
			hasattr(self.http_request,'updated_apps'):

			self.http_request.updated_apps.add_top(self.parent)

	def add_popup_menu_option(self, 
		label, function_action=None, 
		key=None, icon=None, submenu=None
	): pass

	def add_popup_submenu(self, label, submenu=None): pass

	def __repr__(self): return self.value


	def clean_field(self):
		pass

	############################################################################
	############ Properties ####################################################
	############################################################################
	
	@property
	def help(self): return self._help.replace('\n', '&#013;') if self._help else ''


	@property
	def enabled(self): return True
	@enabled.setter
	def enabled(self, value): 
		self.mark_to_update_client()

	############################################################################

	@property
	def value(self): return self._value
	@value.setter
	def value(self, value):
		oldvalue 	= self._value
		self._value = value
		if oldvalue!=value: 
			self.mark_to_update_client()
			self.changed_event()

	############################################################################


	@property
	def name(self): return self._name
	@name.setter
	def name(self, value):
		if self._name!=value: self.mark_to_update_client()
		self._name = value

	############################################################################

	@property
	def label(self): return self._label

	@label.setter
	def label(self, value): 
		if self._label!=value: self.mark_to_update_client()
		self._label = value

	############################################################################

	@property
	def parent(self): return self._parent

	@parent.setter
	def parent(self, value): 
		if self._parent!=value: self.mark_to_update_client()
		self._parent = value



	def __str__(self): return "<span id='place-{0}-{1}' />".format(self.parent.uid, self._name)



	#### Variable connected to the Storage manager of the corrent user
	@property
	def storage(self): 
		user = self.http_request.user
		return conf.MAESTRO_STORAGE_MANAGER.get(user)
	#######################################################

	#### This variable has the current http request #######
	@property
	def http_request(self): return PyFormsMiddleware.get_request()
	#######################################################

	@property
	def was_updated(self): return self._update_client

	@property
	def error(self): return self._error
	@error.setter
	def error(self, value): 
		if value!=self._error: self.mark_to_update_client()
		self._error = value

	@property
	def css(self): return self._css
	@css.setter
	def css(self, value): 
		if value: self.mark_to_update_client()
		self._css = value