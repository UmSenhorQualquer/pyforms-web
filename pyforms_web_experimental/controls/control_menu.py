from pyforms_web.controls.control_base import ControlBase
import simplejson
class ControlMenu(ControlBase):

	def init_form(self):
		return """new ControlMenu('{0}', {1})""".format(
			self._name, 
			simplejson.dumps(self.serialize()) 
		)

	def serialize(self):
		res = []
		for menu_label, menu_list in self.value:
			submenu_list = []
			for submenu_label, submenu_func in menu_list:
				submenu_list.append( [submenu_label, submenu_func.__name__] )
			res.append( [menu_label, submenu_list] )
		
		return { 
			'ControlMenu':  str(self.__class__.__name__), 
			'value':    res,
			'label':    str(self._label if self._label else ''),
			'help':     str(self._help if self._help else ''),
			'visible':  int(self._visible)
		}

	def deserialize(self, properties):
		pass