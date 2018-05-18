from pyforms_web.controls.control_base import ControlBase
import simplejson

class ControlDir(ControlBase):

	def init_form(self):
		return "new ControlDir('{0}', {1})".format( self._name, simplejson.dumps(self.serialize()) )
