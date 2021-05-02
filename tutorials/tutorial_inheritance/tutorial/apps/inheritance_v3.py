from .inheritance_v2 import HeritageV2
from confapp import conf

class HeritageV3(HeritageV2):

    UID = 'heritage-v3'
    TITLE = 'Heritage v3'

    ORQUESTRA_MENU_ORDER = 6

    LAYOUT_POSITION = conf.ORQUESTRA_NEW_WINDOW