from pyforms.basewidget import BaseWidget
from confapp import conf
from pyforms.controls import ControlTextArea

class AppTwo(BaseWidget):

    UID                  = 'app-two'
    TITLE                = 'App two'

    LAYOUT_POSITION      = conf.ORQUESTRA_HOME

    ORQUESTRA_MENU       = 'left'
    ORQUESTRA_MENU_ICON  = 'browser'
    ORQUESTRA_MENU_ORDER = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._table = ControlTextArea('Values')

        self.formset = ['_table']