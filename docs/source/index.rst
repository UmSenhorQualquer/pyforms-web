Pyforms Web documentation!
===========================

**Pyforms Web** is Python 3 framework to create single-page web applications.

The framework aims the boost the development productivity by providing an API in Python that generates HTML Forms amd manages all the client\server forms communications.

Developers do not require to write any HTML or Javascript code, all the code is done in Python 3.

Source code
   https://github.com/UmSenhorQualquer/pyforms-web

The next code produces the next web application.

.. image:: /_static/imgs/basewidget.png
    :width: 700px
    :align: center

.. code::
 
   class DefaultApp(BaseWidget):

     TITLE = 'Demo app'

     def __init__(self, *args, **kwargs):
       super(DefaultApp, self).__init__(*args, **kwargs)

       self._css_btn    = ControlButton('Toggle css')
       self._toggle_btn = ControlButton('Toggle visibility')
       self._copy_btn   = ControlButton('Copy the text')
       self._input      = ControlText('Type something here and press the copy button')
       self._text       = ControlTextArea('Result')
       self._combo      = ControlCombo('Combo')
       self._check      = ControlCheckBox('Check box')
       self._list       = ControlList('List')
       self._label      = ControlLabel('Label', default='Use the label for a dynamic text')

       self.formset = [
         no_columns('_toggle_btn','_copy_btn', '_css_btn'),
         ' ',
         '_input',
         '_text',
         {
           'Free text': [],
           'Segments': [
             'The next example has a segment',
             segment(
               '_combo',
               '_check',
               css='secondary'
             ),
             '_list',
             '_label'
           ]
         }
       ]

.. note:: 

   This framework is a software layer part of the Pyforms framework.

   Pyforms
      https://pyforms.readthedocs.io

   .. image:: /_static/imgs/pyforms-layers-web.svg
      





.. toctree::
   :maxdepth: 4
   :caption: PyForms web

   overview
   getting-started/quick-start
   getting-started/installing

.. toctree::
   :maxdepth: 4
   :caption: Learn
   
   getting-started/first-app
   getting-started/db-apps
   getting-started/formset
   getting-started/apps-permissions
   getting-started/apps-inheritance
   getting-started/advance-db

.. toctree::
   :maxdepth: 4
   :caption: Orquestra

   orquestra/index
   
.. toctree::
   :maxdepth: 4
   :caption: API

   api-reference/overview
   api-reference/python/index
   api-reference/javascript/index

.. toctree::
   :maxdepth: 4
   :caption: More docs
   
   Pyforms <https://pyforms.readthedocs.io>
   Pyforms-GUI <https://pyforms-gui.readthedocs.io>
   Pyforms-TERMINAL <https://pyforms-terminal.readthedocs.io>

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

