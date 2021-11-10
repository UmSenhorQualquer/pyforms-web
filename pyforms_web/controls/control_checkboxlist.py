from pyforms_web.controls.control_base import ControlBase
import simplejson


class ControlCheckBoxList(ControlBase):

    def __init__(self, *args, **kwargs):
        self._headers           = kwargs.get('horizontal_headers',[])
        self._headers           = kwargs.get('headers', self._headers)
        self._select_entire_row = kwargs.get('select_entire_row',True)
        self._read_only         = kwargs.get('readonly',True)
        self._selected_index    = kwargs.get('selected_row_index',-1)
        self._columns_sizes = kwargs.get('columns_sizes', None)

        if 'row_double_click_event' in kwargs:
            self.row_double_click_event = kwargs['row_double_click_event']
        if 'item_selection_changed_event' in kwargs:
            self.item_selection_changed_event = kwargs['item_selection_changed_event']

        super().__init__(*args, **kwargs)


    def init_form(self):
        return "new ControlCheckBoxList('{0}', {1})".format( self._name, simplejson.dumps(self.serialize()) )

    def item_selection_changed_event(self): pass

    def item_selection_changed_client_event(self):
        self.mark_to_update_client()  # what are the implications of enabling this???
        self.item_selection_changed_event()

    @property
    def headers(self): return self._headers

    @headers.setter
    def headers(self, value):
        self.mark_to_update_client()
        self._headers = value

    @property
    def rows_count(self):
        if not isinstance(self._value, list): return 0
        return len(self._value)

    @property
    def columns_styles(self):
        return self._columns_sizes

    @columns_styles.setter
    def columns_styles(self, value):
        self.mark_to_update_client()
        self._columns_sizes = value

    @property
    def columns_align(self):
        return self._columns_align

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
    def value(self):
        """
        Sets and gets the values.

        The values should have the
        """
        return ControlBase.value.fget(self)

    @value.setter
    def value(self, value):
        self._selected_index = -1
        ControlBase.value.fset(self, value)

    def serialize(self):
        data = super().serialize()

        data.update({
            'columns_styles':   self.columns_styles,
            'headers':        self.headers,
            'selected_index': self._selected_index,
        })
        return data

    def deserialize(self, properties):
        super().deserialize(properties)
        self._selected_index = properties['selected_index']
