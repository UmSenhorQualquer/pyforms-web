import os
from pyforms_web import settings
from urllib.request import urlopen
from urllib.parse import urlencode


FILES = [os.path.join("static","pyformsjs", x) for x in settings.PYFORMS_JSFILES_DEBUG]

module_dir  = os.path.dirname(__file__)
basedir     = os.path.join(module_dir, '..')
webdir      = os.path.join(basedir, 'pyforms_web', 'web')
exportfile  = os.path.join(webdir, 'static', 'pyforms.min.js')

content = ''
for filename in FILES:
    with open(os.path.join(webdir,filename)) as infile:
        content += infile.read() + '\n\n'

#content = js_minify(content).replace(';', ';\n')

params = dict([
    ('js_code', content),
    ('compilation_level', 'SIMPLE_OPTIMIZATIONS'),
    ('output_format', 'text'),
    ('output_info', 'compiled_code'),
])

print("Closure Compiler Service API ...", end=" ", flush=True)

with urlopen(
    url="https://closure-compiler.appspot.com/compile",
    data=urlencode(params).encode("utf-8"),
) as response:
    print(response.status, response.reason)

    if int(response.getheader('Content-Length', 0)) <= 1:
        exit("ERROR: Check your js source files for syntax errors.")

    content = response.read()

    print("Writing output to '%s'" % exportfile)

    with open(exportfile,'wb') as outfile:
        outfile.write(content)

print("Done")
