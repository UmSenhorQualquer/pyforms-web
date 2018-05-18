from pyforms_web.controls.control_base import ControlBase
import simplejson


class ControlCheckBoxList(ControlBase):

    def __init__(self, *args, **kwargs):
        self._headers           = kwargs.get('headers',[])
        self._select_entire_row = kwargs.get('select_entire_row',True)
        self._read_only         = kwargs.get('readonly',True)
        self._selected_index    = kwargs.get('selected_row_index',-1)

        if 'row_double_click_event' in kwargs:
            self.row_double_click_event = kwargs['row_double_click_event']
        if 'item_selection_changed_event' in kwargs:
            self.item_selection_changed_event = kwargs['item_selection_changed_event']

        super(ControlCheckBoxList, self).__init__(*args, **kwargs)


    def init_form(self): 
        return "new ControlCheckBoxList('{0}', {1})".format( self._name, simplejson.dumps(self.serialize()) )

    def item_selection_changed_event(self): pass

    
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
            'headers':        self.headers,
            'selected_index': self._selected_index,
        })
        return data

    def deserialize(self, properties):
        ControlBase.deserialize(self,properties)
        self._selected_index    = properties['selected_index']
        