from pyforms_web.controls.control_base import ControlBase
import simplejson, collections

class ValueNotSet: pass

class ControlCombo(ControlBase):


    def __init__(self, *args, **kwargs):
        self._init_form_called = False
        
        self._items = collections.OrderedDict()
        items = kwargs.get('items', [])
        for item in items:
            self.add_item(*item)

        super(ControlCombo, self).__init__(*args, **kwargs)
        
    def init_form(self): 
        self._init_form_called = True
        return "new ControlCombo('{0}', {1})".format( self._name, simplejson.dumps(self.serialize()) )
    
    def add_item(self, label, value=ValueNotSet):
        if self._items==None: self._items=collections.OrderedDict()
        
        # The value for the item was not set, so it will use the label as a value 
        if isinstance(value, ValueNotSet):
            self._items[label] = label
        else:
            self._items[label] = str(value)

        if hasattr(self, '_parent'):
            self.mark_to_update_client()

    def __add__(self, val):
        if isinstance( val, tuple ):
            self.add_item(val[0], val[1])
        else:
            self.add_item(val)
        
        return self


    def clear_items(self):
        self._items = collections.OrderedDict()
        self._value = None

        self.mark_to_update_client()

    @property
    def items(self): return self._items.values()

    @property
    def values(self): return self._items.items()

    @property
    def value(self): return self._value

    @value.setter
    def value(self, value):
        for key, val in self._items.items():
            if str(value)==str(val):
                if str(self._value)!=str(value): 
                    self._value = str(val)
                    self.mark_to_update_client()
                    if self._init_form_called:
                        
                        self.changed_event()
                
        
    @property
    def text(self): return ""

    @text.setter
    def text(self, value):
        for key, val in self._items.items():
            self.mark_to_update_client()
            if value == key:
                self.value = val
                break
    

    def serialize(self):
        data = ControlBase.serialize(self)
        items = []
        for key, value in self._items.items():
            items.append({'text': key, 'value': value, 'name': key }) 
        
        value = self._value
        if value==True:  value = 'true'
        if value==False: value = 'false'
        if value==None:  value = 'null'
        
        data.update({ 'items': items, 'value': value })
        return data
        

