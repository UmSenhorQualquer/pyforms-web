from pyforms.basewidget import BaseWidget
from confapp import conf
from pyforms.controls import ControlDecimal
from pyforms.controls import ControlButton
from pyforms.controls import ControlList
import random, time
from decimal import Decimal

class AppOne(BaseWidget):

    UID                  = 'app-one'
    TITLE                = 'App one'

    LAYOUT_POSITION      = conf.ORQUESTRA_HOME
    ORQUESTRA_MENU       = 'left'
    ORQUESTRA_MENU_ICON  = 'cog'
    ORQUESTRA_MENU_ORDER = 0

    def __init__(self, *args, **kwargs):
        self._table = ControlList('Values')

        super().__init__(*args, **kwargs)

        self._ndata = ControlDecimal('Number of values to generate', default=Decimal(3))
        self._btn   = ControlButton('Generate', default=self.btn_evt)

        self.formset = ['_ndata', '_btn', '_table']

    def generate(self):
        data = []
        n = int(self._ndata.value)
        for i in range(n):
            data.append( (str(i), random.randint(0,1000)) )
        return data

    def btn_evt(self):
        self._table.value = self.generate()
        time.sleep(3)
