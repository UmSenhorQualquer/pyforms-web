from pyforms_web.web.BaseWidget import BaseWidget
from pyforms_web.web.Controls.ControlTextArea import ControlTextArea
from pyforms_web.web.Controls.ControlText import ControlText
from pyforms_web.web.Controls.ControlCombo import ControlCombo
from pyforms_web.web.Controls.ControlDate import ControlDate

from django.db import models

class ModelAdmin(BaseWidget):

	def __init__(self, title, model):
		BaseWidget.__init__(self, title)

		formset = []
		for field in model._meta.get_fields():
			field_name = '{0}'.format(field.name)

			if hasattr(field, 'verbose_name'):
				pyforms_field = None

				if isinstance(field, models.AutoField): continue
				if isinstance(field, models.ForeignKey): 	
					pyforms_field = ControlCombo( field.verbose_name )
					for instance in field.rel.to.objects.all():
						pyforms_field.add_item( str(instance), instance.pk )


				if isinstance(field, models.CharField):  	pyforms_field = ControlText( field.verbose_name )
				if isinstance(field, models.TextField):  	pyforms_field = ControlTextArea( field.verbose_name )
				if isinstance(field, models.DateTimeField): pyforms_field = ControlDate( field.verbose_name )

				if pyforms_field is not None: 
					setattr(self, field_name, pyforms_field)
					formset.append(field_name)

		self.formset = formset