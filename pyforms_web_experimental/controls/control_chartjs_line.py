import simplejson
from django.apps import apps
from django.db import models
from pyforms_web.controls.control_base import ControlBase


class ValueNotSet: pass


class ControlChartJsLine(ControlBase):

    def __init__(self, *args, **kwargs):
        if 'css' not in kwargs: kwargs['css'] = 'blue'
        self._labeled = kwargs.get('labeled', False)

        # set the queryset to which the autocomplete will get the values
        self.queryset = kwargs.get('queryset', None)

        self.max_items = kwargs.get('max_items', 3)

        self.item_format = kwargs.get('item_format', self.item_format)

        self.default_text = kwargs.get('default_text', 'No items to display.')

        self.current_page = 0
        self.first_page = 0

        super().__init__(*args, **kwargs)

        self._loaded = True

    def init_form(self):
        return "new ControlChartJsLine('{0}', {1})".format(self._name, simplejson.dumps(self.serialize()))

    @property
    def queryset(self):
        if self._app and self._model and self._query:
            # reconstruct the query ################################
            model = apps.get_model(self._app, self._model)
            qs = model.objects.all()
            qs.query = self._query
            return qs
        else:
            return None

    @queryset.setter
    def queryset(self, value):
        if value is not None:
            self._model = value.model._meta.label.split('.')[-1]
            self._query = value.query
            self._app = value.model._meta.app_label
        else:
            self._model = None
            self._query = None
            self._app = None

        if hasattr(self, '_loaded'):
            self.mark_to_update_client()

    def item_format(self, item):
        return str(item)

    def page_event(self):
        pass

    def page_changed_event(self):
        self.page_event()
        self._selected_row_id = -1
        self.mark_to_update_client()

    def serialize(self):
        data = super().serialize()

        if self._value == models.fields.NOT_PROVIDED:
            self._value = ValueNotSet

        total_items = 0
        queryset = self.queryset
        if queryset:

            queryset = queryset.distinct()
            total_items = queryset.count()
            pages_items = queryset[self.first_page:self.first_page + self.max_items]
            items = [{
                'name': str(o),
                'value': str(o.pk),
                'page_idx': self.first_page + idx,
                'text': self.item_format(o)
            } for idx, o in enumerate(pages_items)]

            if self._value:
                values = self._value if isinstance(self._value, list) else [self._value]
                values = [v for v in values if v if v is not None]
        else:
            items = []

        data.update({
            'items': items,
            'max_items': self.max_items,
            'current_page': self.current_page,
            'first_page': self.first_page,
            'total_items': total_items,
            'default_text': self.default_text,
        })

        return data

    def deserialize(self, properties):
        super().deserialize(properties)

        self.current_page = properties.get('current_page', self.current_page)
        self.first_page = properties.get('first_page', self.first_page)

        if self.current_page < self.first_page:
            self.current_page = self.first_page

        if self.current_page >= self.first_page+self.max_items:
            self.current_page = self.first_page+self.max_items-1

        if self._value != properties.get('value', self._value):
            self._value = properties.get('value', self._value)
            self.changed_event()
