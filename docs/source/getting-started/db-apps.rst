******************************
Database Widgets
******************************

These examples shows how to build quick forms to manage Django models.

.. note::
    
    Not all the configurations are explained on this page. Please take a look to the classes bellow
    to find more information.

        * :class:`pyforms_web.widgets.django.modeladmin.ModelAdminWidget`

        * :class:`pyforms_web.widgets.django.modelform.ModelFormWidget`

        * :class:`pyforms_web.widgets.django.modelviewform.ModelViewFormWidget`

    


Prepare the django app
_______________________

Create a empty django app folder with the next directory structure inside:


.. code:: bash

    my_dbmodule_name
    ├── pyforms_apps
    │   └── __init__.py
    ├── models.py
    └── __init__.py


Add the next code to the *models.py* file.

.. code:: python

   from django.db import models

   class Supplier(models.Model):
        supplier_id = models.AutoField(primary_key=True)  #: Pk ID
        supplier_name = models.CharField('Name', max_length=200) #: Name
        supplier_nif = models.CharField('NIF Number',max_length=50, blank=True, null=True) #: NIF number
        supplier_keywords = models.CharField('Keywords', max_length=200, blank=True, null=True) #: Free text Keywords
        supplier_contact = models.CharField('Contact Person', max_length=200, blank=True, null=True) #: The mani contact person of a supplier
        supplier_phone = models.CharField('Phone Number', max_length=200, blank=True, null=True) #: Phone number of a supplier
        supplier_mail = models.CharField('Email', max_length=200, blank=True, null=True) #: Email address of a supplier
        supplier_discounts = models.CharField('Discounts', max_length=200, blank=True, null=True) #: Free text Discounts

        country = models.ForeignKey('Country', blank=True, null=True, on_delete=models.CASCADE) #: Fk Supplier's operation country
        category = models.ManyToManyField('Catproduct', blank=True)  #: category of the supplied product


   def __str__(self):
        return self.supplier_name

Add the application to the settings.py

.. code:: python

    INSTALLED_APPS = [
        'my_dbmodule_name',
        ...
    ]

Commit the new model to the database. 

.. code:: python

    python manage.py migrate


Model admin
______________________________________________

To create an app to manage a Django model inherit your App from the ModelAdminWidget class.

Create the file **my_dbmodule_name/pyforms_apps/post_app.py** and add the next code to it.

.. code:: python

    from confapp import conf                           
    from pyforms_web.widgets.django import ModelAdminWidget
    from pyforms_web.organizers import segment
    
    from my_dbmodule_name.models import Supplier

    class SupplierApp(ModelAdminWidget):

        # Default id of the application.
        # Optional when the app is not to be shown in the menu.
        # When used on the menu the UID will used to generate
        # the url for the app: http://[server]/app/[UID]/
        UID = 'supplier-app' 

        # Django model to manage.
        MODEL = Supplier
        
        # Title of the application.
        TITLE = 'Supplier app'
        
        # Position on HTML where the app should run.
        LAYOUT_POSITION = conf.ORQUESTRA_HOME

        # Optional: used to add the app to the menu.
        # Orquestra environment configuration.
        ORQUESTRA_MENU = 'left'        # Add the application to the left menu.
        ORQUESTRA_MENU_ICON = 'users'  # Icon menu.
        ORQUESTRA_MENU_ORDER = 0       # Order where the application should be shown in the menu.
        ####################################################

        # Optional: django model fields to be used in the search field.
        SEARCH_FIELDS = ['supplier_name__icontains']

        # Optional: used to organize the Controls for the model edition form.
        FIELDSETS = [
            (
                segment(
                    ('supplier_name','supplier_nif'),
                    ('supplier_mail','supplier_contact'),
                    ('country','supplier_phone'),
                    ('_category','_addcategory_btn')
                ),
                segment(
                    'supplier_keywords',
                    'supplier_discounts',
                    'category',
                )
            )
        ]

        ...

Access to http://localhost:8000 using your browser and visualize your application.

.. image:: /_static/imgs/db-apps-1.png
    :width: 100%
    :align: center

.. image:: /_static/imgs/db-apps-2.png
    :width: 100%
    :align: center


.. note::

    You set the apps that will work as edition or creation forms, 
    by using the variables **ModelAdminWidget.EDITFORM_CLASS**
    and **ModelAdminWidget.ADDFORM_CLASS**.

    .. code:: python

        ...

        class SupplierApp(ModelAdminWidget):

            ...

            EDITFORM_CLASS  = ...
            ADDFORM_CLASS   = ...

        ...


Model form
___________


To create an app to edit a Django model register, inherit from the ModelFormWidget class.

Add to the beginning of the file **my_dbmodule_name/apps/post_app.py** the next code.

.. code:: python

    from confapp import conf                           
    from pyforms_web.widgets.django import ModelFormWidget
    from pyforms_web.organizers import segment
    
    from my_dbmodule_name.models import Supplier

    class SupplierFormAdmin(ModelFormWidget):

        MODEL = Supplier  # Model to manage.
        TITLE = 'Suppliers' # Title of the application.

        #formset of the edit form
        FIELDSETS = [
            (
                segment(
                    ('supplier_name','supplier_nif'),
                    ('supplier_mail','supplier_contact'),
                    ('country','supplier_phone'),
                ),
                segment(
                    'supplier_keywords',
                    'supplier_discounts',
                    'category',
                    ('_category','_addcategory_btn')
                )
            )
        ]

        ...


To call the app to edit a register use the parameter **pk**.

.. code:: python

    obj = SupplierFormAdmin(pk=1)

    # or to create an empty register.

    obj = SupplierFormAdmin()


Access to http://localhost:8000 using your browser and visualize your application.

.. image:: /_static/imgs/db-apps-2.png
    :width: 100%
    :align: center


Model view form
_________________

Use the ModelViewFormWidget widget to create a view only form.

.. code:: python

    from confapp import conf                           
    from pyforms_web.widgets.django import ModelViewFormWidget
    from pyforms_web.organizers import segment
    
    from my_dbmodule_name.models import Supplier

    class SupplierViewFormAdmin(ModelViewFormWidget):

        MODEL = Supplier  # Model to manage.
        TITLE = 'Suppliers' # Title of the application.

        #formset of the edit form
        FIELDSETS = [
            (
                segment(
                    ('supplier_name','supplier_nif'),
                    ('supplier_mail','supplier_contact'),
                    ('country','supplier_phone'),
                ),
                segment(
                    'supplier_keywords',
                    'supplier_discounts',
                    'category',
                    ('_category','_addcategory_btn')
                )
            )
        ]

        ...



Object access permissions
______________________________________

It is possible to restrict the objects a user has access in the widgets above using the Models Queryset manager.
The idea here is to define the access rules in the Model side, instead of defining the rules in the Visualization side. These way the Model can be ported from application to application maintaining the access rules.

Example: 

.. code:: python

    from django.db import models
    
    class OrderQuerySet(models.QuerySet):
        """
        ORDER QUERYSET MANAGER DEFINITION
        """

        def list_permissions(self, user):
            """
            The function filters the queryset to return only the objects the user has permissions to list.
            """
            ...
            return self

        def has_add_permissions(self, user):
            """
            The function returns a Boolean indicating if the user can add or not a new object.
            """
            ...
            return True

        def has_view_permissions(self, user):
            """
            The function returns a boolean indicating if the user has view permissions to the current queryset.
            """
            ...
            return self

        def has_update_permissions(self, user):
            """
            The function filters the queryset to return only the objects the user has permissions to update.
            """
            ...
            return self

        def has_remove_permissions(self, user):
            """
            The function filters the queryset to return only the objects the user has permissions to remove.
            """
            ...
            return self



    
    class Order(models.Model):
        """
        MODEL DEFINITION
        """
        ...

        objects = OrderQuerySet.as_manager()