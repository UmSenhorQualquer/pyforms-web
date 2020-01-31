from pyforms.basewidget import BaseWidget
from confapp import conf
from pyforms.controls import ControlButton
from .inheritance_v3 import HeritageV3

class OpenHeritageV3(BaseWidget):

    UID                  = 'app-heritagev3'
    TITLE                = 'Open heritage v3'

    LAYOUT_POSITION      = conf.ORQUESTRA_HOME
    ORQUESTRA_MENU       = 'left'
    ORQUESTRA_MENU_ICON  = 'cog'
    ORQUESTRA_MENU_ORDER = 7

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._btn = ControlButton('Open heritage v3', default=self.btn_evt)

        self.formset = ['_btn']

    def btn_evt(self):
        HeritageV3()