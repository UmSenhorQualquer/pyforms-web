***************************
Play with apps inheritance
***************************

Here it will be shown how flexible Pyforms is, and how this flexible can be used to improve productivity and design Applications.

.. note::

    The examples shown here are based on the folder tutorials/tutorial

Example apps
=============

Consider the next 2 apps

App one
_______

This app has a button that generates a list of random numbers defined in a text control, and display them on a table.

.. code-block:: python

    import random
    from confapp import conf
    from decimal import Decimal
    from pyforms.basewidget import BaseWidget
    from pyforms.controls import ControlDecimal
    from pyforms.controls import ControlButton
    from pyforms.controls import ControlList

    class AppOne(BaseWidget):

        UID                  = 'app-one'
        TITLE                = 'App one'

        LAYOUT_POSITION      = conf.ORQUESTRA_HOME
        ORQUESTRA_MENU       = 'left'
        ORQUESTRA_MENU_ICON  = 'cog'
        ORQUESTRA_MENU_ORDER = 0

        def __init__(self, *args, **kwargs):
            self._table = ControlList('Values')

            super().__init__(*args, **kwargs)

            self._ndata = ControlDecimal('Number of values to generate', default=Decimal(3))
            self._btn   = ControlButton('Generate', default=self.btn_evt)

            self.formset = ['_ndata', '_btn', '_table']

        def generate(self):
            data = []
            n = int(self._ndata.value)
            for i in range(n):
                data.append( (str(i), random.randint(0,1000)) )
            return data

        def btn_evt(self):
            self._table.value = self.generate()


.. image:: /_static/imgs/apps-inheritance/app-one.png
    :width: 100%
    :align: center


App two
_______

This app does nothing, only includes a text field.

.. code-block:: python

    from pyforms.basewidget import BaseWidget
    from confapp import conf
    from pyforms.controls import ControlTextArea

    class AppTwo(BaseWidget):

        UID                  = 'app-two'
        TITLE                = 'App two'

        LAYOUT_POSITION      = conf.ORQUESTRA_HOME

        ORQUESTRA_MENU       = 'left'
        ORQUESTRA_MENU_ICON  = 'browser'
        ORQUESTRA_MENU_ORDER = 1

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self._table = ControlTextArea('Values')

            self.formset = ['_table']


.. image:: /_static/imgs/apps-inheritance/app-two.png
    :width: 100%
    :align: center

Multiple inheritance
========================

Based on the 2 apps above we can combine them on a 3nd app using multiple inheritance.
This new app will display the random numbers on a text area, instead of a table.

.. code-block:: python

    from .app_one import AppOne
    from .app_two import AppTwo

    class MultipleInheritance(AppOne, AppTwo):

        UID   = 'multiple-inheritance'
        TITLE = 'Multiple inheritance'

        ORQUESTRA_MENU_ORDER = 1

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

.. image:: /_static/imgs/apps-inheritance/multiple-inheritance.png
    :width: 100%
    :align: center


Inheritance
================

Example 1
_________

The same of the multiple inheritance example can be done using a simple inheritance.

.. code-block:: python

    from pyforms.controls import ControlTextArea
    from .app_one import AppOne

    class Inheritance(AppOne):

        UID   = 'inheritance'
        TITLE = 'inheritance'

        ORQUESTRA_MENU_ORDER = 4

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self._table = ControlTextArea('Values')

.. image:: /_static/imgs/apps-inheritance/inheritance.png
    :width: 100%
    :align: center


Example 2
__________

Below the app inherits from the example above and an extra button to hide or show the text field.

.. code-block:: python

    from pyforms.controls import ControlButton
    from .inheritance import Inheritance

    class InheritanceV2(Heritage):

        UID                  = 'inheritance-v2'
        TITLE                = 'Inheritance v2'

        ORQUESTRA_MENU_ORDER = 5

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self._togglebtn = ControlButton('Hide / Show', default=self.__togglebnt_evt, css='yellow')

            self.formset = [
                ('_ndata', ' '),
                ('_btn', '_togglebtn'),
                '_table'
            ]

        def __togglebnt_evt(self):
            if self._table.visible:
                self._table.hide()
            else:
                self._table.show()

.. image:: /_static/imgs/apps-inheritance/inheritance_v2.png
    :width: 100%
    :align: center

Example 3
__________

This app inherits all the functionalities of the app above, but it is configured to open on a popup window.

.. code-block:: python

    from .inheritance_v2 import HeritageV2
    from confapp import conf

    class InheritanceV3(InheritanceV2):

        UID = 'inheritance-v3'
        TITLE = 'Inheritance v3'

        ORQUESTRA_MENU_ORDER = 6

        LAYOUT_POSITION = conf.ORQUESTRA_NEW_WINDOW

.. image:: /_static/imgs/apps-inheritance/inheritance_v3.png
    :width: 100%
    :align: center

Example 4
__________

This app opens, is exemplifies how the app above can be executed after the press of a button.

.. code-block:: python

    from pyforms.basewidget import BaseWidget
    from confapp import conf
    from pyforms.controls import ControlButton
    from .inheritance_v3 import InheritanceV3

    class OpenInheritanceV3(BaseWidget):

        UID                  = 'app-inheritancev3'
        TITLE                = 'Open inheritance v3'

        LAYOUT_POSITION      = conf.ORQUESTRA_HOME
        ORQUESTRA_MENU       = 'left'
        ORQUESTRA_MENU_ICON  = 'cog'
        ORQUESTRA_MENU_ORDER = 7

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self._btn = ControlButton('Open inheritance v3', default=self.btn_evt)

            self.formset = ['_btn']

        def btn_evt(self):
            InheritanceV3()
