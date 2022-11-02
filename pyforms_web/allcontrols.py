from .controls.control_autocomplete           import ControlAutoComplete
from .controls.control_base                   import ControlBase
from .controls.control_boundingslider         import ControlBoundingSlider
from .controls.control_breadcrumb             import ControlBreadcrumb
from .controls.control_button                 import ControlButton
from .controls.control_barschart              import ControlBarsChart
from .controls.control_checkbox               import ControlCheckBox
from .controls.control_checkboxlist           import ControlCheckBoxList
from .controls.control_checkboxlistquery      import ControlCheckBoxListQuery
from .controls.control_combo                  import ControlCombo
from .controls.control_date                   import ControlDate
from .controls.control_datetime               import ControlDateTime
from .controls.control_decimal                import ControlDecimal
from .controls.control_email                  import ControlEmail
from .controls.control_emptywidget            import ControlEmptyWidget
from .controls.control_file                   import ControlFile
from .controls.control_fileupload             import ControlFileUpload
from .controls.control_float                  import ControlFloat
from .controls.control_html                   import ControlHtml
from .controls.control_integer                import ControlInteger
from .controls.control_label                  import ControlLabel
from .controls.control_linechart              import ControlLineChart
from .controls.control_simplelabel            import ControlSimpleLabel
from .controls.control_list                   import ControlList
from .controls.control_multiplechecks         import ControlMultipleChecks
from .controls.control_multipleselection      import ControlMultipleSelection
from .controls.control_password               import ControlPassword
from .controls.control_piechart               import ControlPieChart
from .controls.control_progress               import ControlProgress
from .controls.control_querylist              import ControlQueryList
from .controls.control_slider                 import ControlSlider
from .controls.control_template               import ControlTemplate
from .controls.control_text                   import ControlText
from .controls.control_textarea               import ControlTextArea
from .controls.control_img                    import ControlImg
from .controls.control_time                   import ControlTime
from .controls.control_spacer                 import ControlSpacer
from .controls.control_multipleupload import ControlMultipleUpload

try:
    from .controls.control_image import ControlImage
except:
    pass
