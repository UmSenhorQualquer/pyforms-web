from pyforms_web.web.controls.ControlBase import ControlBase
import simplejson

class ControlCheckBox(ControlBase):

	def init_form(self): return "new ControlCheckBox('{0}', {1})".format( self._name, simplejson.dumps(self.serialize()) )

