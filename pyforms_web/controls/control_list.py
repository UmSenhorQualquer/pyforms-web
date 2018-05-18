from pyforms_web.controls.control_base import ControlBase
import simplejson
class ControlList(ControlBase):

    def __init__(self, *args, **kwargs):
        self._titles            = kwargs.get('horizontal_headers',[])
        self._select_entire_row = kwargs.get('select_entire_row',True)
        self._read_only         = kwargs.get('readonly',True)
        self._selected_index    = kwargs.get('selected_row_index',-1)

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
            'horizontal_headers':   self.horizontal_headers,
            'read_only':            1 if self._read_only else 0,
            'selected_index':       self._selected_index,
            'select_entire_row':    1 if self._select_entire_row else 0,
        })
        return data

    def deserialize(self, properties):
        ControlBase.deserialize(self,properties)

        self.horizontal_headers = properties['horizontal_headers']
        self._read_only         = properties['read_only']==1
        self._selected_index    = properties['selected_index']
        self._select_entire_row = properties['select_entire_row']==1
