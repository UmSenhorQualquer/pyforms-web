from pyforms.controls import ControlButton
from .inheritance import Heritage

class HeritageV2(Heritage):

    UID                  = 'heritage-v2'
    TITLE                = 'Heritage v2'

    ORQUESTRA_MENU_ORDER = 5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._togglebtn = ControlButton('Hide / Show', default=self.__togglebnt_evt, css='yellow')

        self.formset = [
            ('_ndata', ' '),
            ('_btn', '_togglebtn'),
            '_table'
        ]

    def __togglebnt_evt(self):
        if self._table.visible:
            self._table.hide()
        else:
            self._table.show()