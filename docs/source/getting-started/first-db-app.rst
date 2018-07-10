******************************
First database application
******************************

This example shows how to build quick forms to manage Django models.

.. note::

    The example is based on the functionalities next classes:

        * :class:`pyforms_web.widgets.django.modeladmin.ModelAdminWidget`

        * :class:`pyforms_web.widgets.django.modelform.ModelFormWidget`

        * :class:`pyforms_web.widgets.django.modelviewform.ModelViewFormWidget`


Prepare the django app
_______________________

Create a empty django app folder with the next directory structure inside:


.. code:: bash

    my_dbmodule_name
    ├── apps
    │   └── __init__.py
    ├── models.py
    └── __init__.py


Add the next code to the *models.py* file.

.. code:: python

    from django.db import models
    
    class Post(models.Model):
        title = models.CharField('Title', max_length=200)
        text  = models.TextField('Text')
        created = models.DateTimeField('Created on')
        published = models.DateTimeField('Published on', blank=True, null=True)

Add the application to the settings.py

.. code:: python

    INSTALLED_APPS = [
        'my_dbmodule_name',
        ...
    ]

Commit the new model to the database. 

.. code:: python

    python manage.py migrate


Create the first app
____________________

Create the file **my_dbmodule_name/apps/post_app.py** and add the next code to it.

.. code:: python

    from confapp import conf                           
    from pyforms_web.widgets.django import ModelAdminWidget
    
    from my_dbmodule_name.models import Post

    class PostApp(ModelAdminWidget):

        UID   = 'post-app'
        MODEL = Post
        
        TITLE = 'Posts app'
        
        LAYOUT_POSITION      = conf.ORQUESTRA_HOME

        ORQUESTRA_MENU       = 'left'
        ORQUESTRA_MENU_ICON  = 'browser'
        ORQUESTRA_MENU_ORDER = 0


Run your django project to visualize the next screen.

.. image:: /_static/imgs/first-app-empty.png
    :width: 100%
    :align: center

Override the Edit form application
________________________________________

.. code:: python

    from orquestra.plugins import LayoutPositions
    from pyforms_web.basewidget import BaseWidget

    from pyforms_web.controls.ControlButton import ControlButton
    from pyforms_web.controls.ControlText   import ControlText
    from pyforms_web.controls.ControlList   import ControlList

    class SiteCrawlApp(BaseWidget):
        
        UID                  = 'site-crawl-app'
        TITLE                = 'Site crawl'
        
        LAYOUT_POSITION      = LayoutPositions.HOME

        ORQUESTRA_MENU       = 'left'
        ORQUESTRA_MENU_ICON  = 'browser'
        ORQUESTRA_MENU_ORDER = 0

        def __init__(self, *args, **kwargs):
            super(SiteCrawlApp, self).__init__(*args, **kwargs)

            self._url     = ControlText('Page url')
            self._getlinks_btn = ControlButton('Get links', default=self.___getlinks_btn_evt, label_visible=False)

            self._links_list = ControlList('Links list', horizontal_headers=['Found links'])

            

            self.formset = ['_url', '_getlinks_btn', '_links_list']


        def ___getlinks_btn_evt(self):
            self._links_list.value = [
                ['Link1'], 
                ['Link2']
            ]



Restart your django project to visualize the updates.

.. image:: /_static/imgs/first-app.png
    :width: 100%
    :align: center


Create a View form application
________________________________________
