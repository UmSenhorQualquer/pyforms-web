from pyforms_web.controls.control_querylist import ControlQueryList
from django.apps import apps
from django.db.models.constants import LOOKUP_SEP
from django.core.exceptions import FieldDoesNotExist
from django.utils.encoding import force_text
import simplejson


class ControlQueryCards(ControlQueryList):


	def init_form(self): return "new ControlQueryCards('{0}', {1})".format( self._name, simplejson.dumps(self.serialize()) )
