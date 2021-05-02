import pyforms_web
from confapp import conf
from django import template

register = template.Library()


@register.inclusion_tag('pyforms-dependencies.html')
def pyforms_dependencies():
    cssfiles = conf.CSSFILES
    jsfiles = conf.JSFILES + (
        [f"/static/pyformsjs/{x}" for x in conf.PYFORMS_JSFILES_DEBUG] if conf.PYFORMS_DEBUG else conf.PYFORMS_JSFILES_PROD
    )

    return {
        'cssfiles': [x + f'?={pyforms_web.__version__}' for x in cssfiles],
        'jsfiles':  [x + f'?={pyforms_web.__version__}' for x in jsfiles]
    }
