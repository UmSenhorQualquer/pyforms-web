from pyforms_web.basewidget                         import BaseWidget
from pyforms_web.controls.ControlTextArea           import ControlTextArea
from pyforms_web.controls.ControlText               import ControlText
from pyforms_web.controls.ControlInteger            import ControlInteger
from pyforms_web.controls.ControlFloat              import ControlFloat
from pyforms_web.controls.ControlCombo              import ControlCombo
from pyforms_web.controls.ControlDate               import ControlDate
from pyforms_web.controls.ControlDateTime           import ControlDateTime
from pyforms_web.controls.ControlButton             import ControlButton
from pyforms_web.controls.ControlQueryList          import ControlQueryList
from pyforms_web.controls.ControlMultipleSelection  import ControlMultipleSelection
from pyforms_web.controls.ControlEmptyWidget        import ControlEmptyWidget
from pyforms_web.controls.ControlFileUpload         import ControlFileUpload
from pyforms_web.controls.ControlCheckBox           import ControlCheckBox
from pyforms_web.controls.ControlLabel          import ControlLabel

from django.core.exceptions import ValidationError, FieldDoesNotExist
from .utils import get_fieldsets_strings
import traceback
from django.conf import settings
from django.db import models
import os

from .editform_admin import EditFormAdmin

class ViewFormAdmin(EditFormAdmin):

    def __init__(self, *args, **kwargs):
        """
        Parameters:
            title  - Title of the app.
            model  - Model with the App will represent.
            parent - Variable with the content [model, foreign key id]. It is used to transform the App in an inline App
        """

        super(ViewFormAdmin, self).__init__(*args, **kwargs)
        
        for field in self.edit_buttons:
            field.hide()
        

    def create_model_formfields(self):
        self.readonly = self.get_visible_fields_names()
        super(ViewFormAdmin, self).create_model_formfields()

    def create_newobject(self):
        pass

    def save_event(self):
        pass

    def delete_event(self):
        pass

    def get_buttons_row(self):
        return []