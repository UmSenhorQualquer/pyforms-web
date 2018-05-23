from pyforms_web.controls.control_base               import ControlBase
from pyforms_web.controls.control_multipleselection  import ControlMultipleSelection
from django.apps                                        import apps
import simplejson, collections

class ControlMultipleSelectionQuery(ControlMultipleSelection):

    def __init__(self, *args, **kwargs):
        super(ControlMultipleSelectionQuery, self).__init__(*args, **kwargs)
        
        # it can be used for queryset
        self._query    = None
        self._model    = None
        self._app      = None
        self._queryset_query = None
        self._queryset_model = None
        self._queryset_app   = None

        self.queryset = kwargs.get('queryset', None)

    def init_form(self): return "new ControlMultipleSelection('{0}', {1})".format( self._name, simplejson.dumps(self.serialize()) )

    
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
        
        if value is not None:
            self._model = value.model._meta.label.split('.')[-1]
            self._query = value.query
            self._app   = value.model._meta.app_label
        else:
            self._model = None
            self._query = None
            self._app   = None


    def deserialize(self, properties):
        values = properties.get('value',[])
        
        self.value    = self.queryset.filter(pk__in=values)
        self._label   = properties.get('label','')
        self._help    = properties.get('help','')
        self._visible = properties.get('visible',True)


    def serialize(self):
        data = ControlBase.serialize(self)

        items = []
        for row in (self.queryset if self.queryset else []):
            items.append({
                'text':  str(row),
                'value': str(row.pk),
                'name':  str(row)
            })
        
        if self.value:
            value = list(sorted(map(str,self.value)))
        else:
            value = None


        data.update({ 'items': items, 'value': value, 'mode': self.mode, 'update_items': self._update_items })
        
        self._update_items = False
        return data
        
    