from pyforms_web.basewidget                         import BaseWidget
from pyforms_web.controls.control_textarea           import ControlTextArea
from pyforms_web.controls.control_text               import ControlText
from pyforms_web.controls.control_integer            import ControlInteger
from pyforms_web.controls.control_float              import ControlFloat
from pyforms_web.controls.control_combo              import ControlCombo
from pyforms_web.controls.control_date               import ControlDate
from pyforms_web.controls.control_datetime           import ControlDateTime
from pyforms_web.controls.control_button             import ControlButton
from pyforms_web.controls.control_querylist          import ControlQueryList
from pyforms_web.controls.control_multipleselection  import ControlMultipleSelection
from pyforms_web.controls.control_emptywidget        import ControlEmptyWidget
from pyforms_web.controls.control_fileupload         import ControlFileUpload
from pyforms_web.controls.control_checkbox           import ControlCheckBox
from pyforms_web.controls.control_label          import ControlLabel

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