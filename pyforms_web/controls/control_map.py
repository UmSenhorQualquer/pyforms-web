import simplejson

from pyforms_web.controls.control_base import ControlBase


class ControlMap(ControlBase):

    def __init__(self, *args, **kwargs):
        """
        :param function on_enter_event: Event called when the Enter key is pressed.
        """
        super().__init__(*args, **kwargs)

        self.on_enter_event = kwargs.get('on_enter_event', self.on_enter_event)

        self._edit_polyline = kwargs.get('edit_polyline', False)
        self._edit_polygon = kwargs.get('edit_polygon', False)
        self._edit_marker = kwargs.get('edit_marker', False)
        self._edit_circlemarker = kwargs.get('edit_circlemarker', False)
        self._edit_circle = kwargs.get('edit_circle', False)
        self._edit_rectangle = kwargs.get('edit_rectangle', False)

        self._min_height = kwargs.get('min_height', 180);

        self.center = kwargs.get('center', [51.505, -0.09])
        self.zoom = kwargs.get('zoom', 10)
        self.fitBounds = kwargs.get('fitBounds', False)

        self._remove_layers = []
        self._add_layers = []
        self._add_markers = []
        self._add_polygons = []
        self.layers = {}
        self.markers = []
        self.polygons = []

    def init_form(self):
        return """new ControlMap('{0}', {1})""".format(
            self._name,
            simplejson.dumps(self.serialize())
        )

    def on_enter_event(self):
        """
        Event called when the Enter key is pressed
        """
        pass

    def clear_layers(self):
        self._remove_layers = [l for l in self.layers.values()]
        self.layers = {}
        self.mark_to_update_client()

    def add_layer(self, layer_url, options=None):

        if layer_url in self.layers:
            return

        layer = {'url': layer_url}
        if options:
            layer.update({'options': options})

        self._add_layers.append(layer)
        self.layers[layer_url] = layer
        self.mark_to_update_client()

    def remove_layer(self, layer):
        self._remove_layers.append(layer)
        self.layers.pop(layer['url'])
        self.mark_to_update_client()

    def add_mark(self, lat, long, **kwargs):
        marker = {'coordinate': [lat, long]}
        marker.update(**kwargs)
        self._add_markers.append(marker)
        self.markers.append(marker)

    def add_polygon(self, coordinates, **kwargs):
        polygon = {'coordinates': coordinates}
        polygon.update(**kwargs)
        self._add_polygons.append(polygon)
        self.polygons.append(polygon)

    def deserialize(self, properties):

        self.polygons = []
        for p in properties.get('polygons', []):
            poly = [(lat, long) for (long, lat) in p['geometry']['coordinates'][0]]
            self.polygons.append(poly)

        self.markers = []
        for m in properties.get('markers', []):
            coord =m['geometry']['coordinates']
            self.markers.append([coord[1], coord[0]])

        return super().deserialize(properties)

    def serialize(self):
        res = super().serialize()
        res.update({
            'center': self.center,
            'zoom': self.zoom,
            'fitBounds': self.fitBounds,
            'min_height': self._min_height,

            'add_markers': self._add_markers,
            'add_polygons': self._add_polygons,

            'add_layers': self._add_layers,
            'remove_layers': self._remove_layers,

            'edit_polyline': self._edit_polyline,
            'edit_polygon': self._edit_polygon,
            'edit_marker': self._edit_marker,
            'edit_circlemarker': self._edit_circlemarker,
            'edit_circle': self._edit_circle,
            'edit_rectangle': self._edit_rectangle,
        })
        self._add_markers = []
        self._add_polygons = []
        self._add_layers = []
        self._remove_layers = []

        self.fitBounds = False
        return res

