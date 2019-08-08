import os
import httplib2, urllib, sys


FILES = [
    os.path.join("static","pyformsjs","ControlBase.js"),
    os.path.join("static","pyformsjs","ControlAutoComplete.js"),
    os.path.join("static","pyformsjs","ControlText.js"),
    os.path.join("static","pyformsjs","ControlTextArea.js"),
    os.path.join("static","pyformsjs","ControlBreadcrumb.js"),
    os.path.join("static","pyformsjs","ControlButton.js"),
    os.path.join("static","pyformsjs","ControlBarsChart.js"),
    os.path.join("static","pyformsjs","ControlFile.js"),
    os.path.join("static","pyformsjs","ControlFileUpload.js"),
    os.path.join("static","pyformsjs","ControlDir.js"),
    os.path.join("static","pyformsjs","ControlMultipleChecks.js"),
    os.path.join("static","pyformsjs","ControlMultipleSelection.js"),
    os.path.join("static","pyformsjs","ControlSlider.js"),
    os.path.join("static","pyformsjs","ControlCheckBox.js"),
    os.path.join("static","pyformsjs","ControlCheckBoxList.js"),
    os.path.join("static","pyformsjs","ControlCheckBoxListQuery.js"),
    os.path.join("static","pyformsjs","ControlTemplate.js"),
    os.path.join("static","pyformsjs","ControlCombo.js"),
    os.path.join("static","pyformsjs","ControlInteger.js"),
    os.path.join("static","pyformsjs","ControlFloat.js"),
    os.path.join("static","pyformsjs","ControlCalendar.js"),
    os.path.join("static","pyformsjs","ControlPieChart.js"),
    os.path.join("static","pyformsjs","ControlDate.js"),
    os.path.join("static","pyformsjs","ControlDateTime.js"),
    os.path.join("static","pyformsjs","ControlImage.js"),
    os.path.join("static","pyformsjs","ControlImg.js"),
    os.path.join("static","pyformsjs","ControlHtml.js"),
    os.path.join("static","pyformsjs","ControlEmail.js"),
    os.path.join("static","pyformsjs","ControlItemsList.js"),
    os.path.join("static","pyformsjs","ControlList.js"),
    os.path.join("static","pyformsjs","ControlLineChart.js"),
    os.path.join("static","pyformsjs","ControlQueryCombo.js"),
    os.path.join("static","pyformsjs","ControlQueryList.js"),
    os.path.join("static","pyformsjs","ControlFeed.js"),
    os.path.join("static","pyformsjs","ControlQueryCards.js"),
    os.path.join("static","pyformsjs","ControlPassword.js"),
    os.path.join("static","pyformsjs","ControlPlayer.js"),
    os.path.join("static","pyformsjs","ControlPlayerJs.js"),
    os.path.join("static","pyformsjs","ControlProgress.js"),
    os.path.join("static","pyformsjs","ControlBoundingSlider.js"),
    os.path.join("static","pyformsjs","ControlVisVis.js"),
    os.path.join("static","pyformsjs","ControlLabel.js"),
    os.path.join("static","pyformsjs","ControlSimpleLabel.js"),
    os.path.join("static","pyformsjs","ControlTimeout.js"),
    os.path.join("static","pyformsjs","ControlEmptyWidget.js"),
    os.path.join("static","pyformsjs","ControlMenu.js"),
    os.path.join("static","pyformsjs","ControlTree.js"),
    os.path.join("static","pyformsjs","ControlOrganogram.js"),
    os.path.join("static","pyformsjs","ControlWorkflow.js"),
    os.path.join("static","pyformsjs","ControlCodeMirror.js"),
    os.path.join("static","pyformsjs","BaseWidget.js"),
    os.path.join("static","pyformsjs","pyforms.js"),
    os.path.join("static","pyformsjs","pyforms-hub.js"),
]

module_dir  = os.path.dirname(__file__)
basedir     = os.path.join(module_dir, '..')
webdir      = os.path.join(basedir, 'pyforms_web', 'web')
exportfile  = os.path.join(webdir, 'static', 'pyforms.js')

content = ''
for filename in FILES:
    with open(os.path.join(webdir,filename)) as infile:
        content += infile.read() + '\n\n'

#content = js_minify(content).replace(';', ';\n')


from httplib2 import Http
from urllib.parse import urlencode

params = dict([
    ('js_code', content),
    ('compilation_level', 'SIMPLE_OPTIMIZATIONS'),
    ('output_format', 'text'),
    ('output_info', 'compiled_code'),
])
headers = { "Content-type": "application/x-www-form-urlencoded" }

h = Http()
resp, content = h.request(
    "https://closure-compiler.appspot.com/compile", "POST",
    urlencode(params),
    headers=headers
)


with open(exportfile,'wb') as outfile:
    outfile.write(content)
