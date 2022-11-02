import simplejson

from pyforms_web.controls.control_base import ControlBase


class ControlImgViewer(ControlBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fill = kwargs.get('fill', 'none')
        self.min_height = kwargs.get('min_height', 200)

    def init_form(self):
        return """new ControlImgViewer('{0}', {1})""".format(
            self._name,
            simplejson.dumps(self.serialize())
        )

    def clear(self):
        self._value = ''
        self.mark_to_update_client()

    def serialize(self):
        res = super().serialize()

        res.update({
            'min_height': self.min_height,
            'fill': self.fill
        })

        if self.value is None:
            res.update({'value': ''})
        else:
            res.update({'value': str(self.value)})

        return res

    def deserialize(self, properties):
        pass