******************
First application
******************

.. note::

    More documentation to read about this example at:

        * :class:`pyforms_web.basewidget.BaseWidget`

        * :class:`pyforms_web.controls.control_base.ControlBase`




Here it is shown how to create the first pyforms app for a django project.

.. note:: The instructions on this page assumes you know how the `Django framework <https://www.djangoproject.com/>`_ works.

Prepare the django app
_______________________

Create a empty django app folder with the next directory structure inside:


.. code:: bash

    my_module_name
    ├── apps
    │   └── __init__.py
    └── __init__.py


Add the application to the settings.py

.. code:: python

    INSTALLED_APPS = [
        'my_module_name',
        ...
    ]


Create the first app
____________________

Create the file **my_module_name/apps/site_crawl.py** and add the next code to it.

.. code:: python

    from pyforms.basewidget import BaseWidget
    from confapp import conf

    class SiteCrawlApp(BaseWidget):

        UID                  = 'site-crawl-app'
        TITLE                = 'Site crawl'

        LAYOUT_POSITION      = conf.ORQUESTRA_HOME

        ORQUESTRA_MENU       = 'left'
        ORQUESTRA_MENU_ICON  = 'browser'
        ORQUESTRA_MENU_ORDER = 0

In the **my_module_name/apps/__init__.py** add the next code:

.. code:: python

    from .site_crawl import SiteCrawlApp


You have created the most basic application. Access to http://localhost:8000 using your browser and visualize it.

Now update the **SiteCrawlApp** application with the next code:

.. code:: python

    from pyforms.basewidget import BaseWidget
    from confapp import conf

    from pyforms.controls import ControlButton
    from pyforms.controls import ControlText
    from pyforms.controls import ControlList

    class SiteCrawlApp(BaseWidget):

        UID                  = 'site-crawl-app'
        TITLE                = 'Site crawl'

        LAYOUT_POSITION      = conf.ORQUESTRA_HOME

        ORQUESTRA_MENU       = 'left'
        ORQUESTRA_MENU_ICON  = 'browser'
        ORQUESTRA_MENU_ORDER = 0


        def __init__(self, *args, **kwargs):
        
            super(SiteCrawlApp, self).__init__(*args, **kwargs)

            self._url          = ControlText('Page url')
            self._getlinks_btn = ControlButton('Get links', default=self.___getlinks_btn_evt, label_visible=False)

            self._links_list   = ControlList('Links list', horizontal_headers=['Found links'])

            self.formset = ['_url', '_getlinks_btn', '_links_list']


        def ___getlinks_btn_evt(self):

            self._links_list.value = [
                ['Link1'],
                ['Link2']
            ]



Restart your django project to visualize the updates. 

Press the button to see what happens.

.. image:: /_static/imgs/first-app.png
    :width: 100%
    :align: center

