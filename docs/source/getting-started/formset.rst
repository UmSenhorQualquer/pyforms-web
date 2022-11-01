****************
Widget formset
****************

On this page it is shown examples of Widgets formsets configurations.

**Example:**

.. code-block:: python
    
   [
        no_columns('_toggle_btn','_copy_btn', '_css_btn'),
        ' ',
        ('empty:twelve','_input'),
        '_text',
        {
            'a:Free text': [
                'h1:Header 1',
                'h2:Header 2',
                'h3:Header 3',
                'h4:Header 4',
                'h5:Header 5',
                'h1-right:Header 1',
                'h2-right:Header 2',
                'h3-right:Header 3',
                'h4-right:Header 4',
                'h5-right:Header 5',
                '-',
                'Free text here',
                'msg:Message text',
                'info:Info message',
                'warning:Warning message',
                'alert:Alert message'
            ],
            'b:Segments': [
                'The next example has a segment',
                segment(
                    '_combo',
                    '_check',
                    css='secondary'
                ),
                '_list',
                '_label'
            ]
        },
        'notifications-area'
   ]

Configuration options
########################

tuple
************

Displays the controls horizontally.

list
************

Displays the controls vertically.   

dict
************

Displays the controls in Tabs.  
Use [a:,b:,c:] prefix to sort the tabs.

'-'
************

Draw a vertical line.


Empty column
************

Use ' ', or the prefix 'empty:' + size of the column (ex: one, two, ..., sixteen) to add a empty column.

.. code:: python
   
   ...
   ('empty:twelve', ...),
   ...

segment
************ 

Wraps the formset around a segment `(Semantic UI segment) 
<https://semantic-ui.com/elements/segment.html>`_.
  
   - Use the parameter **css**, to add extra CSS classes to the segment.
   - Use the parameter **field_css**, to add CSS classes to the div.field containing the segment.

.. code:: python
   
   segment(
        ('person_first', 'person_middle', 'person_last'),
        ('person_gender', 'person_birthday'),
        ('degree', 'scientificarea'),
        ('person_cv', 'person_web'),
        'person_bio',
        css='inverted',
        field_css='fourteen wide',
    ),


no_columns
************

Do not apply the fields columns alignments.

Free text
************

Do not apply the fields columns alignments.

Message
************

By using the prefixes [msg:,info:,warning:,alert:] you will wrap a free message on message box.

Headers
************

Use the prefixes [h1:,h2:,h3:,h4:,h5:,h1-right:,h2-right:,h3-right:,h4-right:,h5-right:] on free text.

.. code:: python
  
   [
       ... ,
       'h3:PERSONAL INFORMATION',
       ...
   ]


Notifications area
**********************
By default the application's messages are shown on the top of each application, but it is possible to define
a new position to these messages by including the code 'notifications-area' on the formset.


2 segments side by side
########################


.. image:: /_static/imgs/formsets-segment-sidebyside.png
    :width: 100%
    :align: center


.. code:: python

    class PeopleFormWidget(BaseWidget):

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            ... # fields definition

            # Use the field_style to align the checkbox to the middle.

            self.person_active.field_style = 'text-align: right;margin-top:5px;'
            self.person_active.field_css   = 'two wide'

            self._rotimg_btn = ControlButton(
                '<i class="icon undo" ></i>Rotate',
                default=self.__rotimg_evt,
                label_visible=False,   # Remove all the labels from the fields to make the row thinner.
                style='margin-top:5px;',
                field_style='text-align: right;',
                css='mini'
            )

           ...

           self.formset = [
                no_columns('_privateinfo_btn', '_proposals_btn', '_contracts_btn', 'person_active'),
                'h3:PERSONAL INFORMATION',
                ( # Use the tupple to display the segments side by side.
                    segment(
                        ('person_first', 'person_middle', 'person_last'),
                        ('person_gender', 'person_birthday'),
                        ('degree', 'scientificarea'),
                        ('person_cv', 'person_web'),
                        'person_bio',
                        field_css='fourteen wide', # Use the argument to resize the segment on the left.
                    ),
                    segment(
                        '_img',
                        '_rotimg_btn',
                        'person_img',
                        field_style='max-width:330px;' # Use the argument to define the style of the div.field wrapping the Control.
                    )
                ),
           ]

Customize fields css classes and styles
############################################

Use the constructor parameters **field_css**, **field_style**, **css**, and **style** to customize the visualization of each field.

Example:

.. code:: python

    self._field_example = ControlText(
        ...,
        style='margin-top:5px;',            # Extra style to add to the control.
        css='mini'                          # Extra css classes to add to the control.
        field_style='text-align: right;',   # Extra style to add to the field div that encapsulates the control.
        field_css='mini'                    # Extra css classes to add to the field dive that encapsulates the control.
    )

.. note::

   Check the PeopleFormWidget example above for more examples.