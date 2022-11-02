from pyforms_web.controls.control_base import ControlBase
import simplejson

class ControlThumbnailSelection(ControlBase):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self._labels = kwargs.get('labels', [])
        self.update_selection_event = kwargs.get('update_selection_event', self.update_selection_event)

    def init_form(self):
        return """new ControlThumbnailSelection('{0}', {1})""".format(
            self._name, 
            simplejson.dumps(self.serialize()) 
        )

    def serialize(self):
        data = super().serialize()
        data.update({
            'labels': self._labels
        })
        return data

    def deserialize(self, properties):
        res = super().deserialize(properties)
        self.selected_label = properties.get('selected_label', None)
        self.selected_pk = properties.get('selected_pk', None)
        return res

    def update_selection_event(self):
        print(
            self.selected_label,
            self.selected_pk
        )