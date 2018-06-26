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

from .modelform import ModelFormWidget

class ModelViewFormWidget(ModelFormWidget):
    """
    When a Pyforms application inherit from this class a form for the model ModelViewFormWidget.MODEL is created with
    all the fields in the fieldset in read only mode.

    **Usage example:**

    .. code:: python

       from suppliers.models import Order

       class OrderView(ModelViewFormWidget):
            MODEL =  Order
            TITLE = 'Order in read-only'
            
            FIELDSETS = [
                'h3:General Information',
                ('responsible','order_req'),
                'supplier',
                {'a:Description':['order_desc'], 'b:Notes':['order_notes']},
                ('order_amount', 'currency', 'order_paymethod'),
                ('order_reqnum', 'order_reqdate'),
                ('order_podate', 'order_deldate')
            ]
    """

    def __init__(self, *args, **kwargs):
        """

        :param str title: Title of the app. By default will assume the value in the class variable TITLE.
        :param django.db.models.Model model: Model with the App will represent. By default will assume the value in the class variable MODEL.
        :param list(ModelAdmin) inlines: Sub models to show in the interface
        :param list(str) fieldsets: Organization of the fields
        :param int parent_pk: Parent model key
        :param django.db.models.Model parent_model: Parent model class
        :param int pk: Model register to manage
        """

        super().__init__(*args, **kwargs)
        
        for field in self.edit_buttons:
            field.hide()
        

    def create_model_formfields(self):
        self.readonly = self.get_visible_fields_names()
        super().create_model_formfields()

    def create_newobject(self):
        pass

    def save_event(self):
        pass

    def delete_event(self):
        pass

    def get_buttons_row(self):
        return []