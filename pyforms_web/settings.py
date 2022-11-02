PYFORMS_APPS_IN_MEMORY = False  # Between the user requests to the server, the app is stored in memory instead of the disk

PYFORMS_APPS = {}

LAYOUT_NEW_WINDOW = 2

PYFORMS_DEBUG = False

PYFORMS_VERBOSE = False

try:
    import os
    from django.conf import settings

    PYFORMS_WEB_APPS_CACHE_DIR = os.path.join(str(settings.BASE_DIR), 'apps-cache')
    PYFORMS_WEB_LOCKFILE = os.path.join(str(settings.BASE_DIR), 'lockfile.txt')
except:
    PYFORMS_WEB_APPS_CACHE_DIR = 'apps-cache'
    PYFORMS_WEB_LOCKFILE = 'lockfile.txt'

PYFORMS_JSFILES_DEBUG = [
    "ControlBase.js",
    "BaseControlStreaming.js",
    "ControlAutoComplete.js",
    "ControlText.js",
    "ControlTextArea.js",
    "ControlBreadcrumb.js",
    "ControlButton.js",
    "ControlBarsChart.js",
    "ControlFile.js",
    "ControlFileUpload.js",
    "ControlMultipleChecks.js",
    "ControlMultipleSelection.js",
    "ControlSlider.js",
    "ControlSpacer.js",
    "ControlCheckBox.js",
    "ControlCheckBoxList.js",
    "ControlCheckBoxListQuery.js",
    "ControlTemplate.js",
    "ControlCombo.js",
    "ControlInteger.js",
    "ControlFloat.js",
    "ControlPieChart.js",
    "ControlDate.js",
    "ControlDateTime.js",
    "ControlImage.js",
    "ControlImg.js",
    "ControlHtml.js",
    "ControlEmail.js",
    "ControlList.js",
    "ControlLineChart.js",
    "ControlQueryList.js",
    "ControlPassword.js",
    "ControlProgress.js",
    "ControlBoundingSlider.js",
    "ControlLabel.js",
    "ControlSimpleLabel.js",
    "ControlEmptyWidget.js",
    "ControlTime.js",
    "ControlMultipleUpload.js",
    "BaseWidget.js",
    "pyforms.js",
    "pyforms-hub.js",
]

PYFORMS_JSFILES_PROD = [
    "/static/pyforms.min.js",
]

CSSFILES = [
    "/static/datetimepicker/jquery.datetimepicker.min.css",
    "/static/jqplot/jquery.jqplot.css",
    "/static/filer/css/jquery.filer.css",
    "/static/filer/css/jquery.filer-dragdropbox-theme.css",
    "/static/semantic-ui/semantic.css",
    "/static/jquery-ui/jquery-ui.min.css",
    "/static/pyforms.css",
]

JSFILES = [
    "/static/jquery.min.js",
    "/static/jquery.json-2.4.min.js",
    "/static/base64.js",
    "/static/datetimepicker/jquery.datetimepicker.full.min.js",
    "/static/jqplot/jquery.jqplot.js",
    "/static/jqplot/plugins/jqplot.cursor.js",
    "/static/jqplot/plugins/jqplot.logAxisRenderer.js",
    "/static/jqplot/plugins/jqplot.canvasTextRenderer.js",
    "/static/jqplot/plugins/jqplot.canvasAxisLabelRenderer.js",
    "/static/jqplot/plugins/jqplot.blockRenderer.js",
    "/static/jqplot/plugins/jqplot.enhancedLegendRenderer.js",
    "/static/jqplot/plugins/jqplot.logAxisRenderer.js",
    "/static/jqplot/plugins/jqplot.dateAxisRenderer.js",
    "/static/jqplot/plugins/jqplot.categoryAxisRenderer.js",
    "/static/jqplot/plugins/jqplot.barRenderer.js",
    "/static/jqplot/plugins/jqplot.pointLabels.js",
    "/static/jqplot/plugins/jqplot.pieRenderer.js",
    "/static/jquery-ui/jquery-ui.min.js",
    "/static/filer/js/jquery.filer.js",
    "/static/jquery.selection.js",

    "/static/semantic-ui/semantic.min.js", # Requirement located in orquestra
]
