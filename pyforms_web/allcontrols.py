from .controls.control_autocomplete           import ControlAutoComplete
from .controls.control_base                   import ControlBase
from .controls.control_boundingslider         import ControlBoundingSlider
from .controls.control_breadcrumb             import ControlBreadcrumb
from .controls.control_button                 import ControlButton
from .controls.control_calendar               import ControlCalendar
from .controls.control_checkbox               import ControlCheckBox
from .controls.control_checkboxlist           import ControlCheckBoxList
from .controls.control_checkboxlistquery      import ControlCheckBoxListQuery
from .controls.control_combo                  import ControlCombo
from .controls.control_date                   import ControlDate
from .controls.control_datetime               import ControlDateTime
from .controls.control_dir                    import ControlDir
from .controls.control_email                  import ControlEmail
from .controls.control_emptywidget            import ControlEmptyWidget
from .controls.control_feed                   import ControlFeed
from .controls.control_file                   import ControlFile
from .controls.control_fileupload             import ControlFileUpload
from .controls.control_float                  import ControlFloat
from .controls.control_html                   import ControlHtml
from .controls.control_integer                import ControlInteger
from .controls.control_itemslist              import ControlItemsList
from .controls.control_label                  import ControlLabel
from .controls.control_simplelabel            import ControlSimpleLabel
from .controls.control_list                   import ControlList
from .controls.control_menu                   import ControlMenu
from .controls.control_multiplechecks         import ControlMultipleChecks
from .controls.control_multipleselection      import ControlMultipleSelection
from .controls.control_multipleselectionquery import ControlMultipleSelectionQuery
from .controls.control_password               import ControlPassword
from .controls.control_piechart               import ControlPieChart
from .controls.control_progress               import ControlProgress
from .controls.control_querycards             import ControlQueryCards
from .controls.control_querycombo             import ControlQueryCombo
from .controls.control_queryitem             import ControlQueryItem
from .controls.control_querylist              import ControlQueryList
from .controls.control_slider                 import ControlSlider
from .controls.control_template               import ControlTemplate
from .controls.control_text                   import ControlText
from .controls.control_textarea               import ControlTextArea
from .controls.control_timeout                import ControlTimeout
from .controls.control_visvis                 import ControlVisVis
from .controls.control_workflow               import ControlWorkflow 
from .controls.control_img                    import ControlImg

try:
    from .controls.control_image              import ControlImage
except:
    pass

try:
    from .controls.control_player             import ControlPlayer
except:
    pass