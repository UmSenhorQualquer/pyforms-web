from pyforms_web.controls.control_base import ControlBase
import simplejson, collections
from django.db.models import Q
from django.apps import apps
from django.db import models

class ValueNotSet: pass


class ControlAutoComplete(ControlBase):

    def __init__(self, *args, **kwargs):
        self._init_form_called = False
        super(ControlAutoComplete, self).__init__(*args, **kwargs)
        
        # configure the Combo to get its items from an URL
        self.items_url = kwargs.get('items_url', None)
        # set the function to query the items in the case we are using the url mode
        self.autocomplete_search = kwargs.get('autocomplete_search', self.autocomplete_search)
        # set the queryset to which the autocomplete will get the values
        self.queryset = kwargs.get('queryset', None)
        # function to filter the queryset
        self.queryset_filter = kwargs.get('queryset_filter', self.queryset_filter)

        # allow multiple choices
        self.multiple = kwargs.get('multiple', False)

    def init_form(self): 
        self._init_form_called = True
        return "new ControlAutoComplete('{0}', {1})".format( self._name, simplejson.dumps(self.serialize()) )

    def queryset_filter(self, qs, keyword, control):
        return qs

    @property
    def queryset(self):
        if self._app and self._model and self._query:
            # reconstruct the query ################################
            model       = apps.get_model(self._app, self._model)
            qs          = model.objects.all()
            qs.query    = self._query
            return qs
        else:
            return None

    @queryset.setter
    def queryset(self, value):
        if value:
            self._model = value.model._meta.label.split('.')[-1]
            self._query = value.query
            self._app   = value.model._meta.app_label
        else:
            self._model = None
            self._query = None
            self._app   = None

    def autocomplete_search(self, keyword):
        queryset = self.queryset

        if queryset:

            queryset = self.queryset_filter(queryset, keyword, self)

            if keyword:
                model = queryset.model
     
                if hasattr(model, 'autocomplete_search_fields'):
                    or_filter = Q()
                    for search_field in model.autocomplete_search_fields():
                        or_filter.add( Q(**{search_field:keyword}), Q.OR)
                    queryset = queryset.filter(or_filter)
                else:
                    queryset = queryset.filter(pk=keyword)

            try:
                # return the results
                return [{'name':str(o), 'value':o.pk, 'text':str(o)} for o in queryset]
            except:
                return []
        else:
            return []

    """
    @property
    def value(self):  return self._value

    @value.setter
    def value(self, value):
        if self._value!=value: self.mark_to_update_client()
        self._value = value
    """
    
    def deserialize(self, data):
        super(ControlAutoComplete,self).deserialize(data)

        value = data.get('value')
        if self.multiple:
            if value is None:
                self.value = []
            else:
                self.value = [(int(v) if v and v.isdigit() else None) for v in value.split(',')]
        else:
            self.value = int(value) if value and value.isdigit() else None

    def serialize(self):
        data = super(ControlAutoComplete,self).serialize()

        if self.multiple:
            if self.value is None:
                data.update({'value': []})
            else:
                data.update({'value': [None if v is None else str(v) for v in self.value]})

        queryset = self.queryset
        if queryset:
            value = self._value if isinstance(self._value, list) else [self._value]
            value = [v for v in value if v if v is not None]

            if value:
                queryset = queryset.filter(pk__in=value).distinct()
                items = [{'name':str(o), 'value':str(o.pk), 'text':str(o)} for o in queryset]
            else:
                items = []

            if not self.multiple:
                items = [{'name':'---', 'value':None, 'text':'---'}] + items
        else:
            items = []

        data.update({'items_url': self.items_url, 'items':items, 'multiple':self.multiple})

        return data
        


    @property
    def parent(self):
        """
        Set or return the control window.
        """
        return self._parent

    @parent.setter
    def parent(self, value): 
        ControlBase.parent.fset(self, value)
        
        if self.items_url is None:
            url = "/pyforms/autocomplete/{app_id}/{field_name}/{{query}}/".format(
                app_id=value.uid, 
                field_name=self.name
            )
            self.items_url = url

        

