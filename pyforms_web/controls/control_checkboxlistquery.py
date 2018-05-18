from pyforms_web.controls.control_base         import ControlBase
from pyforms_web.controls.control_checkboxlist import ControlCheckBoxList
from django.apps                                  import apps
import simplejson, collections

class ControlCheckBoxListQuery(ControlCheckBoxList):

    def __init__(self, *args, **kwargs):
        if 'headers' not in kwargs:
            kwargs['headers'] = ['']
        super(ControlCheckBoxListQuery, self).__init__(*args, **kwargs)

        self.obj2list    = kwargs.get('obj2list',    self.obj2list)
        self.add_func    = kwargs.get('add_func',    None)
        self.remove_func = kwargs.get('remove_func', None)
        
        # it can be used for queryset
        self._query    = None
        self._model    = None
        self._app      = None
        self._queryset_query = None
        self._queryset_model = None
        self._queryset_app   = None

        self._checked = {}

    def init_form(self): return "new ControlCheckBoxListQuery('{0}', {1})".format( self._name, simplejson.dumps(self.serialize()) )


    def obj2list(self, row):
        return [False, str(row)]

    def remove_event(self):
        if self.remove_func is not None:
            selected = [v[-1] for v in self.items if v[0]==True]
            query = self.value.filter(pk__in=selected)
            self.remove_func(query)
            self.mark_to_update_client()
     
    def add_event(self):
        if self.add_func is not None:
            self.add_func()
            self.mark_to_update_client()
            
    
    @property
    def queryset(self):
        if self._queryset_app and self._queryset_model and self._queryset_query:
            model    = apps.get_model(self._queryset_app, self._queryset_model)
            qs       = model.objects.all()
            qs.query = self._queryset_query
            return qs
        else:
            return None

    @queryset.setter
    def queryset(self, value):
        if value is not None:
            self._queryset_model = value.model._meta.label.split('.')[-1]
            self._queryset_query = value.query
            self._queryset_app   = value.model._meta.app_label
        else:
            self._queryset_model = None
            self._queryset_query = None
            self._queryset_app   = None

    @property
    def value(self):
        if self._app and self._model and self._query:
            model    = apps.get_model(self._app, self._model)
            qs       = model.objects.all()
            qs.query = self._query
            return qs
        else:
            return None

    @value.setter
    def value(self, value):
        self.mark_to_update_client()

        if value is not None:
            self._model = value.model._meta.label.split('.')[-1]
            self._query = value.query
            self._app   = value.model._meta.app_label
        else:
            self._model = None
            self._query = None
            self._app   = None

    @property
    def items(self):
        for obj in (self.value if self.value else []):
            row    = self.obj2list(obj) + [obj.pk]
            row[0] = self._checked.get(obj.pk, False)
            yield row


    def deserialize(self, properties):
        values = properties.get('value',[])
        new_values    = []
        self._checked = {}
        for v in values:
            pk    = v[-1]
            check = v[0]
            self._checked[pk] = check
            new_values.append( pk )
        
        self.value    = self.queryset.filter(pk__in=new_values)
        self._label   = properties.get('label','')
        self._help    = properties.get('help','')
        self._visible = properties.get('visible',True)


    def serialize(self):
        data = ControlBase.serialize(self)

        values = []
        for obj in (self.value if self.value else []):
            pk  = obj.pk
            row = self.obj2list(obj) + [obj.pk]
            row[0] = self._checked.get(pk, False)
            values.append(row)

        data.update({
            'value':          values,
            'headers':        self.headers,
            'selected_index': self._selected_index,
            'add_button':     self.add_func is not None,
            'remove_button':  self.remove_func is not None
        })
        return data    
    