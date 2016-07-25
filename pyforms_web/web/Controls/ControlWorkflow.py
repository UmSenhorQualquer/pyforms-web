import datetime
from pyforms_web.web.Controls.ControlBase import ControlBase

class ControlWorkflow(ControlBase):

	def initControl(self): return "new ControlWorkflow('{0}', {1})".format( self._name, str(self.serialize()) )
