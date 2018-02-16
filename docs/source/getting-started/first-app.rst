******************************
First application
******************************

Here it is shown how to create the first pyforms app for a django project.

.. note:: The instructions on this page assumes you know how the `Django framework <https://www.djangoproject.com/>`_ works.

Prepare the django app
_______________________

Create a empty django app folder with the next directory structure inside:


.. code:: bash

    my_app_name
    ├── setup.py
    └── my_module_name
        ├── apps
        │   └── __init__.py
        └── __init__.py


Install the django app and add it to the settings.py

.. code:: bash
    
    pip install . --upgrade


.. code:: python

    INSTALLED_APPS = [
        'my_module_name',
        ...
    ]


Create the first app
____________________

Create the file **my_module_name/apps/site_crawl.py** and add the next code to it.

.. code:: python

    from orquestra.plugins import LayoutPositions
    from pyforms_web.web.basewidget import BaseWidget

    class SiteCrawlApp(BaseWidget):
        
        UID                  = 'site-crawl-app'
        TITLE                = 'Site crawl'
        
        LAYOUT_POSITION      = LayoutPositions.HOME

        ORQUESTRA_MENU       = 'left'
        ORQUESTRA_MENU_ICON  = 'browser'
        ORQUESTRA_MENU_ORDER = 0

Run your django project to visualize the next screen.

.. image:: /_static/imgs/first-app-empty.png
    :width: 100%
    :align: center

Now update the **SiteCrawlApp** application with the next code.

.. code:: python

    from orquestra.plugins import LayoutPositions
    from pyforms_web.web.basewidget import BaseWidget

    from pyforms_web.web.Controls.ControlButton import ControlButton
    from pyforms_web.web.Controls.ControlText   import ControlText
    from pyforms_web.web.Controls.ControlList   import ControlList

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