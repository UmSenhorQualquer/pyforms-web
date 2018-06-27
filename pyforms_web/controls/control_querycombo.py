from pyforms_web.controls.control_base import ControlBase
import simplejson, collections
from django.apps import apps

class ControlQueryCombo(ControlBase):


    def __init__(self, *args, **kwargs):
        super(ControlQueryCombo, self).__init__(*args, **kwargs)

        # these informations is needed to serialize the control to the drive
        self._app   = None
        self._model = None
        self._query = None
        self.allow_none = kwargs.get('allow_none', False)
        self._column = kwargs.get('display_column', 'pk')
        ####################################################################

        self.queryset = kwargs.get('queryset', None)

    def init_form(self): return "new ControlQueryCombo('{0}', {1})".format( self._name, simplejson.dumps(self.serialize()) )
    
    def serialize(self):
        data = ControlBase.serialize(self)
        items = []

        if self.allow_none:
             items.append({'label': '---', 'value': None})

        for obj in self.queryset:
            if self._column:
                items.append({'label': str(getattr(obj,self._column)), 'value': obj.pk })
            else:
                items.append({'label': str(obj), 'value': obj.pk })

        data.update({ 'items': items, 'value': self._value })
        return data

    @property
    def display_column(self): return self._column

    @property
    def display_column(self): return self._column
    
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
            self.value  = None
        else:
            self._model = None
            self._query = None
            self._app   = None


    def deserialize(self, properties):
        """
        Serialize the control data.
        
        :param dict properties: Serialized data to load.
        """
        if properties.get('value','null')=='null':
            properties['value'] = None
        super().deserialize(properties)
