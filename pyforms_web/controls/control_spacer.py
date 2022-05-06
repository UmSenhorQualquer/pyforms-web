import simplejson

from pyforms_web.controls.control_base import ControlBase


class ControlSpacer(ControlBase):

    def init_form(self):
        return """new ControlSpacer('{0}', {1})""".format(
            self._name,
            simplejson.dumps(self.serialize())
        )
