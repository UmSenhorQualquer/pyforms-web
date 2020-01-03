from pyforms_web.controls.control_base import ControlBase
import simplejson

class ControlList(ControlBase):

    def __init__(self, *args, **kwargs):
        """
        :param str label: Control label.
        :param str default: Set the value. Default = None.
        :param bool visible: Set the control visible or hidden. Default = True.
        :param bool error: Mark the control as having and error. Default = False.
        :param str css: Extra css classes to add to the control.
        :param str field_css: Extra css classes to add to the field dive that encapsulates the control.
        :param str style: Extra style to add to the control.
        :param str field_style: Extra style to add to the field div that encapsulates the control.
        :param bool enabled: Set the control enabled or disabled. Default = True.
        :param bool readonly: Set the control as read only. Default = True.

        :param list(str) horizontal_headers: List of headers.
        :param bool select_entire_row: Flag to select the entire row or individual cells. Default = False.
        :param int selected_row_index: Default selected row. Default = -1.
        :param list(str) columns_size: List of css with the size value of each column. Default = None.
        :param list(str) columns_align: List of css alignment values for each column. Default = [].

        :param function row_double_click_event: Reference to a function called when the row is double clicked.
        :param function item_selection_changed_event: Reference to a function called when the selection of an item change.

        """
        self._titles            = kwargs.get('horizontal_headers',[])
        self._select_entire_row = kwargs.get('select_entire_row',True)
        self._read_only         = kwargs.get('readonly',True)
        self._selected_index    = kwargs.get('selected_row_index',-1)
        self._columns_size      = kwargs.get('columns_size', None)
        self._columns_align     = kwargs.get('columns_align', [])

        if 'row_double_click_event' in kwargs:
            self.row_double_click_event = kwargs['row_double_click_event']
        if 'item_selection_changed_event' in kwargs:
            self.item_selection_changed_event = kwargs['item_selection_changed_event']

        super(ControlList, self).__init__(*args, **kwargs)


    def init_form(self): return "new ControlList('{0}', {1})".format( self._name, simplejson.dumps(self.serialize()) )

    def item_selection_changed_event(self): pass

    def row_double_click_event(self): pass

    @property
    def horizontal_headers(self): return self._titles

    @horizontal_headers.setter
    def horizontal_headers(self, value):
        self.mark_to_update_client()
        self._titles = value

    @property
    def rows_count(self):
        if not isinstance(self._value, list): return 0
        return len(self._value)


    @property
    def select_entire_row(self): return self._select_entire_row

    @select_entire_row.setter
    def select_entire_row(self, value):
        self.mark_to_update_client()
        self._select_entire_row = value

    @property
    def readonly(self): return self._read_only

    @readonly.setter
    def readonly(self, value):
        self.mark_to_update_client()
        self._read_only = value

    @property
    def columns_size(self): return self._columns_size

    @columns_size.setter
    def columns_size(self, value):
        self.mark_to_update_client()
        self._columns_size = value

    @property
    def columns_align(self): return self._columns_align

    @columns_align.setter
    def columns_align(self, value):
        self.mark_to_update_client()
        self._columns_align = value

    @property
    def selected_row_index(self): return self._selected_index

    @selected_row_index.setter
    def selected_row_index(self, value):
        self.mark_to_update_client()
        self._selected_index = value


    @property
    def value(self): return ControlBase.value.fget(self)

    @value.setter
    def value(self, value):
        self._selected_index = -1
        ControlBase.value.fset(self, value)

    def serialize(self):
        data = ControlBase.serialize(self)

        data.update({
            'columns_align':        self.columns_align,
            'columns_size':         self.columns_size,
            'horizontal_headers':   self.horizontal_headers,
            'read_only':            1 if self._read_only else 0,
            'selected_index':       self._selected_index,
            'select_entire_row':    1 if self._select_entire_row else 0,
        })
        return data

    def deserialize(self, properties):
        self._selected_index = properties['selected_index']
        