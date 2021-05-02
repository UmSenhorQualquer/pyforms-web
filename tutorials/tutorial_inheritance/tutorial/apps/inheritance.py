from pyforms.controls import ControlTextArea
from .app_one import AppOne

class Heritage(AppOne):

    UID                  = 'heritage'
    TITLE                = 'Heritage'

    ORQUESTRA_MENU_ORDER = 4

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._table = ControlTextArea('Values')
