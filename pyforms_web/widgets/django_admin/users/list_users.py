from pyforms_web.widgets.django import ModelAdminWidget
from django.contrib.auth.models import User
from .edit_user import UserEditWidget
from .add_user import UserAddWidget

class UsersManagementWidget(ModelAdminWidget):

    # Django model to manage.
    MODEL = User

    # Title of the application.
    TITLE = 'Users management'

    LIST_FILTER = []
    SEARCH_FIELDS = ['username__icontains']
    LIST_DISPLAY = ['username', 'is_superuser']

    ADDFORM_CLASS = UserAddWidget
    EDITFORM_CLASS = UserEditWidget