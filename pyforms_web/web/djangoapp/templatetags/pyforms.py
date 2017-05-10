from django 				import template
from django.template.loader import render_to_string
from django.conf 			import settings
from django.utils.safestring import mark_safe
from pyforms_web.web.djangoapp.middleware import PyFormsMiddleware
from pyforms_web.web.djangoapp 		import ApplicationsLoader

register = template.Library()

@register.simple_tag
def renderPyFormsAppHTML(app): return mark_safe( app.html )
