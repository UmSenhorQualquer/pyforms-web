from django.contrib.auth.models import User
from pyforms.basewidget import segment
from pyforms_web.widgets.django_admin.users.edit_user import UserEditWidget


class UserAddWidget(UserEditWidget):

    MODEL = User

    FIELDSETS = [
        ('is_staff', 'is_superuser', 'is_active', ' '),
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
        )
    ]

    READ_ONLY = []


    def capitalize_fields(self):
        self.is_staff.label = self.is_staff.label.capitalize()
        self.is_superuser.label = self.is_superuser.label.capitalize()
        self.is_active.label = self.is_active.label.capitalize()
        self.username.label = self.username.label.capitalize()
        self.email.label = self.email.label.capitalize()
        self.first_name.label = self.first_name.label.capitalize()
        self.last_name.label = self.last_name.label.capitalize()
