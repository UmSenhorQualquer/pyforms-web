from confapp import conf
from pyforms_web.basewidget import BaseWidget
from pyforms_web.controls.control_autocomplete import ControlAutoComplete
from pyforms_web.controls.control_barschart import ControlBarsChart
from pyforms_web.controls.control_boundingslider import ControlBoundingSlider
from pyforms_web.controls.control_breadcrumb import ControlBreadcrumb
from pyforms_web.controls.control_button import ControlButton
from pyforms_web.controls.control_checkbox import ControlCheckBox
from pyforms_web.controls.control_checkboxlist import ControlCheckBoxList
from pyforms_web.controls.control_checkboxlistquery import ControlCheckBoxListQuery
from pyforms_web.controls.control_combo import ControlCombo
from pyforms_web.controls.control_date import ControlDate
from pyforms_web.controls.control_datetime import ControlDateTime
from pyforms_web.controls.control_decimal import ControlDecimal
from pyforms_web.controls.control_email import ControlEmail
from pyforms_web.controls.control_emptywidget import ControlEmptyWidget
from pyforms_web.controls.control_file import ControlFile
from pyforms_web.controls.control_fileupload import ControlFileUpload
from pyforms_web.controls.control_float import ControlFloat
from pyforms_web.controls.control_html import ControlHtml
from pyforms_web.controls.control_image import ControlImage
from pyforms_web.controls.control_img import ControlImg
from pyforms_web.controls.control_integer import ControlInteger
from pyforms_web.controls.control_label import ControlLabel
from pyforms_web.controls.control_linechart import ControlLineChart
from pyforms_web.controls.control_list import ControlList
from pyforms_web.controls.control_multiplechecks import ControlMultipleChecks
from pyforms_web.controls.control_multipleselection import ControlMultipleSelection
from pyforms_web.controls.control_multipleupload import ControlMultipleUpload
from pyforms_web.controls.control_password import ControlPassword
from pyforms_web.controls.control_piechart import ControlPieChart
from pyforms_web.controls.control_progress import ControlProgress
from pyforms_web.controls.control_querylist import ControlQueryList
from pyforms_web.controls.control_simplelabel import ControlSimpleLabel
from pyforms_web.controls.control_slider import ControlSlider
from pyforms_web.controls.control_spacer import ControlSpacer
from pyforms_web.controls.control_template import ControlTemplate
from pyforms_web.controls.control_text import ControlText
from pyforms_web.controls.control_textarea import ControlTextArea
from pyforms_web.controls.control_time import ControlTime
from pyforms_web_tests.models import Test


class TestControls(BaseWidget):
    UID = 'pyforms-web-test'
    TITLE = 'Test Controls'

    LAYOUT_POSITION = conf.ORQUESTRA_HOME

    ORQUESTRA_MENU = 'left'
    ORQUESTRA_MENU_ICON = 'browser'
    ORQUESTRA_MENU_ORDER = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._control_text = ControlText('ControlText', default='Some text')
        self._control_autocomplete = ControlAutoComplete('ControlAutoComplete', queryset=Test.objects.all())
        self._control_boundingslider = ControlBoundingSlider('ControlBoundingSlider', min=0, max=100, default=[0, 20])
        self._control_breadcrumb = ControlBreadcrumb(
            'ControlBreadcrumb',
            default=[('ControlBreadcrumb', 'http://go-some-where.pt'), ('Test page', 'http://go-some-where.pt'), ('Current page', None)]
        )
        self._control_button = ControlButton('ControlButton')
        self._control_barschart = ControlBarsChart('ControlBarsChart')
        self._control_checkbox = ControlCheckBox('ControlCheckBox')
        self._control_checkboxlist = ControlCheckBoxList('ControlCheckBoxList', horizontal_headers=['', 'Name'],
                                                         default=[(False, 'A1'), (True, 'A2'), (True, 'A3')])
        self._control_checkboxlistquery = ControlCheckBoxListQuery('ControlCheckBoxListQuery', horizontal_headers=['', 'Name'], default=Test.objects.all())
        self._control_combo = ControlCombo('ControlCombo')
        self._control_date = ControlDate('ControlDate')
        self._control_dateTime = ControlDateTime('ControlDateTime')
        self._control_decimal = ControlDecimal('ControlDecimal')
        self._control_email = ControlEmail('ControlEmail')
        self._control_emptywidget = ControlEmptyWidget('ControlEmptyWidget')
        self._control_file = ControlFile('ControlFile', path='/Users')
        self._control_fileupload = ControlFileUpload('ControlFileUpload')
        self._control_float = ControlFloat('ControlFloat')
        self._control_html = ControlHtml('ControlHtml', default='<b>Add any html code</b> with the <big>ControlHtml</big>')
        self._control_integer = ControlInteger('ControlInteger')
        self._control_label = ControlLabel('ControlLabel')
        self._control_linechart = ControlLineChart('ControlLineChart')
        self._control_simplelabel = ControlSimpleLabel('ControlSimpleLabel')
        self._control_list = ControlList('ControlList', horizontal_headers=['Column 1', 'Column 2'], default=[('R1C1', 'R1C2'), ('R2C1', 'R2C2')])
        self._control_multiplechecks = ControlMultipleChecks('ControlMultipleChecks', items=[('A1', 1), ('A2', 2), ('A3', 3)])
        self._control_multipleselection = ControlMultipleSelection('ControlMultipleSelection', items=[('A1', 1), ('A2', 2), ('A3', 3)])
        self._control_password = ControlPassword('ControlPassword')
        self._control_piechart = ControlPieChart('ControlPieChart')
        self._control_progress = ControlProgress('ControlProgress')
        self._control_querylist = ControlQueryList('ControlQueryList', default=Test.objects.all())
        self._control_slider = ControlSlider('ControlSlider', min=0, max=100, default=100)
        self._control_template = ControlTemplate('ControlTemplate')
        self._control_text = ControlText('ControlText')
        self._control_textarea = ControlTextArea('ControlTextArea')
        self._control_img = ControlImg('ControlImg', default='https://pyforms.readthedocs.io/projects/Pyforms-WEB/en/dev/_static/pyforms-web-small.jpg')
        self._control_time = ControlTime('ControlTime')
        self._control_spacer = ControlSpacer('ControlSpacer')
        self._control_multipleupload = ControlMultipleUpload('ControlMultipleUpload')
        self._control_image = ControlImage('ControlImage', default='https://pyforms.readthedocs.io/projects/Pyforms-WEB/en/dev/_static/pyforms-web-small.jpg')

        self.formset = [
            '_control_breadcrumb',
            '_control_text',
            '_control_autocomplete',
            '_control_boundingslider',
            '_control_button',
            '_control_barschart',
            '_control_checkbox',
            '_control_checkboxlist',
            '_control_checkboxlistquery',
            '_control_combo',
            '_control_date',
            '_control_dateTime',
            '_control_decimal',
            '_control_email',
            '_control_emptywidget',
            '_control_float',
            '_control_html',
            '_control_integer',
            '_control_label',
            '_control_linechart',
            '_control_simplelabel',
            '_control_list',
            '_control_multiplechecks',
            '_control_multipleselection',
            '_control_password',
            '_control_piechart',
            '_control_progress',
            '_control_querylist',
            '_control_slider',
            '_control_template',
            '_control_text',
            '_control_textarea',
            '_control_img',
            '_control_time',
            '_control_spacer',
            '_control_image',
            '_control_multipleupload',
            '_control_fileupload',
            '_control_file'
        ]
