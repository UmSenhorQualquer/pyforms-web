******************************************
Apps permissions
******************************************

.. note::

    Checkout the :class:`pyforms_web.basewidget.BaseWidget` class for more information.


For some web applications there is the need of implementing several users profiles, with different access to functionalities and data.

On this page we are going to show how the access to Pyforms applications can be restricted.

AUTHORIZED_GROUPS variable
=====================================

This BaseWidget variable can be set with the list of Django groups that has access to the app.

Example:

.. code:: python

    ...

    class EmployeesAdminApp(ModelAdminWidget):

        ...

        AUTHORIZED_GROUPS = ['superuser', 'django-group']

        ...

.. note::

    In the case you want to restrict the access to a **superuser** user then instead of using the name of a Django group you should use the label *'superuser'*.


Overwrite the BaseWidget functions
===================================

The second way of restricting the access to an app is by overwriting the permissions functions from the BaseWidget class.

.. note::

    By overwriting the permissions' methods of the BaseWidget class your are overwriting the functionality of the **AUTHORIZED_GROUPS** variable.

Example:

.. code:: python

    ...

    class EmployeesAdminApp(ModelAdminWidget):

        ...

        @classmethod
        def has_permissions(cls, user):
            """
            This class method, verifies if a user has permissions to execute the application
            """
            return True or False

        def has_session_permissions(self, user):
            """
            It verifies if a user has permissions to execute the application during the runtime.
            """
            return True or False

        ...