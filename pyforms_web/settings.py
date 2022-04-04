PYFORMS_APPS_IN_MEMORY = False # Between the user requests to the server, the app is stored in memory instead of the disk

PYFORMS_APPS = {}

LAYOUT_NEW_WINDOW = 2

PYFORMS_DEBUG = False

PYFORMS_VERBOSE = False

try:
	import os
	from django.conf import settings

	PYFORMS_WEB_APPS_CACHE_DIR = os.path.join(str(settings.BASE_DIR) ,'apps-cache')
	PYFORMS_WEB_LOCKFILE 	   = os.path.join(str(settings.BASE_DIR) ,'lockfile.txt')
except:
	PYFORMS_WEB_APPS_CACHE_DIR = 'apps-cache'
	PYFORMS_WEB_LOCKFILE 	   = 'lockfile.txt'

PYFORMS_JSFILES_DEBUG = [
    #"MultiInheritance.js",
    "ControlBase.js",
    "BaseControlStreaming.js",
    "ControlAutoComplete.js",
    "ControlText.js",
    "ControlTextArea.js",
    "ControlBreadcrumb.js",
    "ControlButton.js",
    "ControlBarsChart.js",
    "ControlFile.js",
    "ControlMultipleUpload.js",
    "ControlFileUpload.js",
    "ControlDir.js",
    "ControlMultipleChecks.js",
    "ControlMultipleSelection.js",
    "ControlSlider.js",
    "ControlCheckBox.js",
    "ControlCheckBoxList.js",
    "ControlCheckBoxListQuery.js",
    "ControlTemplate.js",
    "ControlCombo.js",
    "ControlInteger.js",
    "ControlFloat.js",
    "ControlCalendar.js",
    "ControlPieChart.js",
    "ControlDate.js",
    "ControlDateTime.js",
    "ControlImage.js",
    "ControlImg.js",
    "ControlDrawInImg.js",
    "ControlHtml.js",
    "ControlEmail.js",
    "ControlItemsList.js",
    "ControlList.js",
    "ControlLineChart.js",
    "ControlQueryCombo.js",
    "ControlQueryList.js",
    "ControlFeed.js",
    "ControlQueryCards.js",
    "ControlPassword.js",
    "ControlPlayer.js",
    "ControlPlayerJs.js",
    "ControlProgress.js",
    "ControlBoundingSlider.js",
    "ControlVisVis.js",
    "ControlLabel.js",
    "ControlSimpleLabel.js",
    "ControlTimeout.js",
    "ControlEmptyWidget.js",
    "ControlMenu.js",
    "ControlTree.js",
    "ControlTime.js",
    "ControlOrganogram.js",
    "ControlWorkflow.js",
    "ControlSearch.js",
    "ControlCodeMirror.js",
    "ControlHighlightText.js",
    "ControlThumbnailSelection.js",
    "ControlImgViewer.js",
    "BaseWidget.js",
    "pyforms.js",
    "pyforms-hub.js",
]

PYFORMS_JSFILES_PROD  = [
    "/static/pyforms.min.js",
]

CSSFILES = [
	"/static/treant/Treant.css",
	"/static/jquery.flowchart/jquery.flowchart.min.css",
	"/static/datetimepicker/jquery.datetimepicker.min.css",
	"/static/jqplot/jquery.jqplot.css",
	"/static/filer/css/jquery.filer.css",
	"/static/filer/css/jquery.filer-dragdropbox-theme.css",
	"/static/semantic-ui/semantic.css",
	"/static/jquery-ui/jquery-ui.min.css",
	"/static/codemirror/codemirror.css",
	"/static/zoomist/zoomist.min.css",
	"/static/pyforms.css",
]

JSFILES = [
	"/static/jquery.min.js",
	"/static/jquery.json-2.4.min.js",
	"/static/jquery.flowchart/jquery.panzoom.min.js",
	"/static/jquery.flowchart/jquery.mousewheel.min.js",
	"/static/jquery.flowchart/jquery.flowchart.min.js",
	"/static/datetimepicker/jquery.datetimepicker.full.min.js",
	"/static/base64.js",
	"/static/gmaps.min.js",
	"/static/treant/Treant.js",
	"/static/timeline/timeline.js",
	"/static/timeline/track.js",
	"/static/timeline/event.js",
	"/static/timeline/graph.js",
	"/static/canvas-video-player.js",
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
	"/static/filer/js/jquery.filer.js",
	"/static/jquery-ui/jquery-ui.min.js",
	"/static/semantic-ui/semantic.min.js",
	"/static/codemirror/codemirror.js",
	"/static/codemirror/xml.js",
	"/static/codemirror/css.js",
	"/static/codemirror/javascript.js",
	"/static/codemirror/htmlmixed.js",
	"/static/codemirror/autorefresh.js",
	"/static/jquery.selection.js",
    '/static/TextHighlighter.min.js',
	"/static/zoomist/zoomist.min.js",
]
