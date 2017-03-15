
from pyforms_web.web.Controls.ControlBase import ControlBase
from pyforms_web.web.Controls.ControlFile import ControlFile
from pyforms_web.web.Controls.ControlSlider import ControlSlider
from pyforms_web.web.Controls.ControlText import ControlText
from pyforms_web.web.Controls.ControlCheckBox import ControlCheckBox
try:
	from pyforms_web.web.Controls.ControlPlayer import ControlPlayer
except:
	print "ControlPlayer is not available"
from pyforms_web.web.Controls.ControlButton import ControlButton
from pyforms_web.web.djangoapp.Applications import ApplicationsLoader
from pyforms_web.web.djangoapp.middleware import PyFormsMiddleware
import uuid, os, shutil, base64, inspect
import base64, dill, StringIO, simplejson
from pysettings import conf
from django.template.loader import render_to_string

class BaseWidget(object):

	refresh_timeout = 120000

	def __init__(self, title, parent_win=None):
		self._formset 		= None
		self._splitters     = []
		self._title         = title
		self._formLoaded    = False
		self._controls      = []
		self._html          = ''
		self._js            = ''
		if not hasattr(self, '_uid'): self._uid = str(uuid.uuid4())

		self._messages = []

		self._parent_window = parent_win
		self.is_new_app = True

		PyFormsMiddleware.add(self)

		

	############################################################################
	############ Module functions  #############################################
	############################################################################

	def init_form(self, parent=None):
		"""
		Generate the module Form
		"""
		#for c in self.controls.values(): c.parent = parent

		self._html = ''
		self._js = ''
		self._controls = [c.init_form() for c in self.controls.values()]
		if self._formset != None: 
			self._html += self.generate_panel(self._formset, add_field_class=False)
			#self._js = '[{0}]'.format(",".join(self._controls))


		parent_code = 'undefined'
		if parent: parent_code = "'{0}'".format(parent.uid)

		extra_data = {'refresh_timeout': self.refresh_timeout}

		self._js = '[{0}]'.format(",".join(self._controls))
		self._html += """
		<script type="text/javascript">pyforms.add_app( new BaseWidget('{2}', '{0}', {1}, {3}, {4}) );</script>
		""".format(self.modulename, self._js, self.uid, parent_code, simplejson.dumps(extra_data))
		self._formLoaded = True

		return { 'code': self._html, 'title': self._title, 'app_id':self.uid, 'refresh_timeout':  self.refresh_timeout }
		

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

	def generate_segments(self, formsetdict):
		
		html = ''
		for key, item in sorted(formsetdict.items()):
			if item==True: continue
			
			html += "<h2 class='ui header' >{0}</h2>".format(key[key.find(':')+1:])
			html += "<div class='ui segment pyforms-segment' >"
			html += self.generate_panel(item, add_field_class=False)
			html += "</div>"
		return html

	def __get_fields_class(self, row):

		if 	 len(row)==2: return 'two'
		elif len(row)==3: return 'three'
		elif len(row)==4: return 'four'
		elif len(row)==5: return 'five'
		elif len(row)==6: return 'six'
		elif len(row)==7: return 'seven'
		elif len(row)==8: return 'eight'
		elif len(row)==9: return 'nine'
		elif len(row)==10: return 'ten'
		elif len(row)==11: return 'eleven'
		else: return ''

	def generate_panel(self, formset, add_field_class=True):
		"""
		Generate a panel for the module form with all the controls
		formset format example: [('_video', '_arenas', '_run'), {"Player":['_threshold', "_player", "=", "_results", "_query"], "Background image":[(' ', '_selectBackground', '_paintBackground'), '_image']}, "_progress"]
		tuple: will display the controls in the same horizontal line
		list: will display the controls in the same vertical line
		dict: will display the controls in a tab widget
		'||': will plit the controls in a horizontal line
		'=': will plit the controls in a vertical line
		@param formset: Form configuration
		@type formset: list
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
						if row.startswith('info:'): layout += "<pre class='info' >%s</pre>" % row[5:]
						elif row.startswith('h1:'): layout += "<h1>%s</h1>" % row[3:]
						elif row.startswith('h2:'): layout += "<h2>%s</h2>" % row[3:]
						elif row.startswith('h3:'): layout += "<h3>%s</h3>" % row[3:]
						elif row.startswith('h4:'): layout += "<h4>%s</h4>" % row[3:]
						elif row.startswith('h5:'): layout += "<h5>%s</h5>" % row[3:]
						elif row.startswith('warning:'): layout += "<div class='ui warning visible  message'>%s</div>" % row[8:]
						elif row.startswith('alert:'): 	 layout += "<div class='ui alert message'>%s</div>" % row[6:]
						else: layout += "<div class='ui message'>%s</div>" % row
					else:
						#self._controls.append( control.init_form() )
						layout += "%s" % control
		elif type(formset) is list:
			for row in formset:
				if isinstance(row, tuple):
					panel 	= self.generate_panel( row )
					layout += "<div class='row fields {1}' >{0}</div>".format(panel, self.__get_fields_class(row))
				elif isinstance(row, list):
					panel 	= self.generate_panel( row )
					layout += "<div class='row fields' >{0}</div>".format(panel)
				elif row == " ":
					layout += "<div class='field-empty-space' ></div>"
				elif type(row) is dict and row.get('is-segment', False):
					seg = self.generate_segments(row)
					layout += seg
				elif type(row) is dict:
					tabs 	= self.generate_tabs(row)
					layout += tabs
				else:
					control = self.controls.get(row, None)
					if control==None:
						if row.startswith('info:'): layout += "<pre class='info' >%s</pre>" % row[5:]
						elif row.startswith('h1:'): layout += "<h1>%s</h1>" % row[3:]
						elif row.startswith('h2:'): layout += "<h2>%s</h2>" % row[3:]
						elif row.startswith('h3:'): layout += "<h3>%s</h3>" % row[3:]
						elif row.startswith('h4:'): layout += "<h4>%s</h4>" % row[3:]
						elif row.startswith('h5:'): layout += "<h5>%s</h5>" % row[3:]
						elif row.startswith('warning:'): 	layout += "<div class='ui warning visible  message'>%s</div>" % row[8:]
						elif row.startswith('alert:'): 		layout += "<div class='ui alert error message'>%s</div>" % row[6:]
						else: layout += "<div class='ui message'>%s</div>" % row
						
					else:
						#self._controls.append( control.init_form() )
						layout += str(control)
		
		return layout



	def load_serialized_form(self, params):
		widgets = []

		"""
		for var_name, base64data in params.get('children-windows', []):
			serialized_win = base64.b64decode(base64data)
			win = dill.loads(serialized_win)
			win.parent_win = self
			setattr(self, var_name, win)			
		"""


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
		
		res = {
			'uid':				self.uid, 
			'layout_position': 	self.layout_position if hasattr(self, 'layout_position') else 5,
			'title': 			self.title
		}

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

	def commit(self):
		for key, item in self.controls.items(): item.commit()

		user = PyFormsMiddleware.user()
		# save the modifications
		userpath = os.path.join(
			conf.PYFORMS_WEB_APPS_CACHE_DIR,
			'{0}-{1}'.format(user.pk, user.username) 
		)
		if not os.path.exists(userpath): os.makedirs(userpath)

		app_path = os.path.join(userpath, "{0}.app".format(self.uid) )
		with open(app_path, 'wb') as f: 
			dill.dump(self, f)
		


	############################################################################
	############ Parent class functions reemplementation #######################
	############################################################################

	def show(self): pass

	############################################################################
	############ Properties ####################################################
	############################################################################

	@property
	def children_windows(self):
		"""
		Return all the form controls from the the module
		"""
		result = {}
		for name, var in vars(self).items():
			if isinstance(var, BaseWidget):
				var._name 		= name
				result[name]	= var
		return result
	
	@property
	def controls(self):
		"""
		Return all the form controls from the the module
		"""
		result = {}
		for name, var in vars(self).items():
			if isinstance(var, ControlBase):
				var.parent 	= self
				var._name 	= name
				result[name]= var

		return result

	def message(self, msg, title=None, msg_type=None):
		msg = { 'type': msg_type if msg_type else '', 'messages':msg if isinstance(msg, list) else [msg], 'title':title }
		self._messages.append(msg)
	def success(self,	msg, title=None):	self.message(msg, title, msg_type='success')
	def info(self, 		msg, title=None):	self.message(msg, title, msg_type='info')
	def warning(self, 	msg, title=None):	self.message(msg, title, msg_type='warning')
	def alert(self, 	msg, title=None):	self.message(msg, title, msg_type='error')


	@classmethod
	def has_permissions(cls, user):
		if hasattr(cls, 'groups'):
			if user.is_superuser and 'superuser' in cls.groups: 
				return True
			if user.groups.filter(name__in=cls.groups).exists():
				return True
		else:
			return True

		return False


	#### Variable connected to the Storage manager of the corrent user
	@property
	def storage(self):
		if hasattr(self, '_storage'):
			return self._storage
		else:
			return conf.MAESTRO_STORAGE_MANAGER.get(self.http_request.user)
	@storage.setter 
	def storage(self, value): self._storage = value

	#######################################################



	#### This variable has the current http request #######
	@property
	def http_request(self): return PyFormsMiddleware.get_request()

	#######################################################


	@property
	def form(self): 
		return render_to_string( 
			os.path.join('pyforms', 'basewidget-template.html'), 
			{'application_html': self._html, 'application_id': self.uid}
		)
		
	@property
	def js(self): return self._js
	
	@property
	def uid(self): return self._uid
	@uid.setter
	def uid(self, value): self._uid = value
	
	@property
	def title(self): return self._title

	@title.setter
	def title(self, value): self._title = value

	@property
	def modulename(self):
		return inspect.getmodule(self).__name__ + '.' + self.__class__.__name__
	


	@property
	def formset(self): return self._formset

	@formset.setter
	def formset(self, value): self._formset = value