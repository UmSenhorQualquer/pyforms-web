from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from pyforms.basewidget import no_columns, segment
from pyforms_web.controls.control_password import ControlPassword
from pyforms_web.widgets.django import ModelFormWidget
from django.contrib.auth.models import User


class UserEditWidget(ModelFormWidget):

    MODEL = User

    FIELDSETS = [
        ('is_staff', 'is_superuser', 'is_active', 'date_joined'),
        (
            segment(
                ('username', 'email'),
                ('first_name', 'last_name'),
            ),
            segment(
                '_newpass',
                '_repeat',
                css='secondary'
            )
        ),
        'groups',
        'user_permissions',

    ]

    READ_ONLY = [
        'date_joined'
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.capitalize_fields()

        self._newpass = ControlPassword('New password')
        self._repeat = ControlPassword("Repeat")

    def capitalize_fields(self):
        self.is_staff.label = self.is_staff.label.capitalize()
        self.is_superuser.label = self.is_superuser.label.capitalize()
        self.is_active.label = self.is_active.label.capitalize()
        self.date_joined.label = self.date_joined.label.capitalize()
        self.username.label = self.username.label.capitalize()
        self.email.label = self.email.label.capitalize()
        self.first_name.label = self.first_name.label.capitalize()
        self.last_name.label = self.last_name.label.capitalize()
        self.groups.label = self.groups.label.capitalize()
        self.user_permissions.label = self.user_permissions.label.capitalize()

    def update_object_fields(self, obj):

        if self._newpass.value or self._repeat.value:

            if self._newpass.value != self._repeat.value:
                self._newpass.error = True
                self._repeat.error = True
                raise ValidationError('The passwords do not match', code='invalid')

            elif validate_password(self._newpass.value, obj) is None:
                obj.set_password(self._newpass.value)

        self._newpass.error = False
        self._repeat.error = False

        return super().update_object_fields(obj)