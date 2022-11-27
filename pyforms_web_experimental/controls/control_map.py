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

        self._add_markers = []
        self._add_polygons = []
        self._commands = []
        self.layers = []
        self.markers = []
        self.polygons = []

        for layer in self.value:
            self.add_layer(layer['url'], layer['options'])

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
        for l in self.layers:
            self.remove_layer(l)
        self.mark_to_update_client()

    def set_layer_opacity(self, url, opacity):
        self._commands.append({'command': 'setOpacity', 'layer_url': url, 'opacity': opacity})
        self.mark_to_update_client()

    def fit_bounds(self, bounds):
        self._commands.append({'command': 'fitBounds', 'bounds': bounds})
        self.mark_to_update_client()

    def set_z_index(self, url, zindex):
        self._commands.append({'command': 'setZIndex', 'layer_url': url, 'zindex': zindex})
        self.mark_to_update_client()

    def add_layer(self, layer_url, options=None):
        if layer_url in self.layers:
            return
        self._commands.append({'command': 'addLayer', 'layer_url': layer_url, 'options': options})
        self.layers.append(layer_url)
        self.mark_to_update_client()

    def remove_layer(self, layer_url):
        self._commands.append({'command': 'removeLayer', 'layer_url': layer_url})
        self.layers.remove(layer_url)
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
            'min_height': self._min_height,

            'add_markers': self._add_markers,
            'add_polygons': self._add_polygons,

            'commands': self._commands,

            'edit_polyline': self._edit_polyline,
            'edit_polygon': self._edit_polygon,
            'edit_marker': self._edit_marker,
            'edit_circlemarker': self._edit_circlemarker,
            'edit_circle': self._edit_circle,
            'edit_rectangle': self._edit_rectangle,
        })
        self._add_markers = []
        self._add_polygons = []
        self._commands = []

        return res

