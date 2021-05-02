from .app_one import AppOne
from .app_two import AppTwo

class MultipleHeritage(AppOne, AppTwo):

    UID                  = 'multiple-heritage'
    TITLE                = 'Multiple heritage'

    ORQUESTRA_MENU_ORDER = 1