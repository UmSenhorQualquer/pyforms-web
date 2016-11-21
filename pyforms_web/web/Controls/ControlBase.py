import uuid

class ControlBase(object):


	def __init__(self, label = "", defaultValue = "", helptext=''):
		self._name      = ""
		self._help      = helptext
		self._value     = defaultValue
		self._parent    = None
		self._label     = label
		self._visible   = True
		self.uid = uuid.uuid4()
		self._controlHTML = ""

		self._update_client = False

	def init_form(self):
		self._controlHTML = "<div id='id{0}' ><input type='text' id='{1}' /></div>".format( self.uid, self._name )
		return self._controlHTML

	def serialize(self):
		return { 
			'name':     str(self.__class__.__name__), 
			'value':    self.value,
			'label':    str(self._label if self._label else ''),
			'help':     str(self._help if self._help else ''),
			'visible':  int(self._visible)
		}

	def deserialize(self, properties):
		
		self.value    = properties.get('value',None)
		self._label   = properties.get('label','')
		self._help    = properties.get('help','')
		self._visible = properties.get('visible',True)
		
			
	def finishEditing(self): self.updateControl()

	def updateControl(self): pass

	def changed_event(self): pass

	def load(self, data):
		if 'value' in data: self.value = data['value']

	def save(self, data):
		if self.value: data['value'] = self.value

	def valueUpdated(self, value): pass

	def show(self): 
		self._update_client = True
		self._visible = True

	def hide(self): 
		self._update_client = True
		self._visible = False

	def commit(self): self._update_client = False


	def openPopupMenu(self, position): pass

	def addPopupSubMenuOption(self, label, options): pass

	def addPopupMenuOption(self, label, functionAction = None): pass

	def __repr__(self): return str(self.value)

	############################################################################
	############ Properties ####################################################
	############################################################################
	
	@property
	def help(self): return self._help.replace('\n', '&#013;') if self._help else ''


	@property
	def enabled(self): return True
	@enabled.setter
	def enabled(self, value): 
		self._update_client = True

	############################################################################

	@property
	def value(self): return self._value
	@value.setter
	def value(self, value):
		oldvalue = self._value
		self._value = value
		if oldvalue!=value: 
			self._update_client = True
			self.changed_event()

	############################################################################


	@property
	def name(self): return self._name
	@name.setter
	def name(self, value):
		if self._name!=value: self._update_client = True
		self._name = value

	############################################################################

	@property
	def label(self): return str(self._label)

	@label.setter
	def label(self, value): 
		if self._label!=value: self._update_client=True
		self._label = value

	############################################################################

	@property
	def parent(self): return self._parent

	@parent.setter
	def parent(self, value): 
		if self._parent!=value: self._update_client=True
		self._parent = value



	def __str__(self): return "<span id='place-{0}-{1}' />".format(self.parent.uid, self._name)



	#### Variable connected to the Storage manager of the corrent user
	@property
	def storage(self): return self._storage

	@storage.setter
	def storage(self, value): self._storage = value
	#######################################################

	#### This variable has the current http request #######
	@property
	def httpRequest(self): return self._httpRequest

	@httpRequest.setter
	def httpRequest(self, value): self._httpRequest = value
	#######################################################

	@property
	def was_updated(self): return self._update_client
	