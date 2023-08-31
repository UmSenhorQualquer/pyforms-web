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

        self._layers = {}

        self._commands = []

        for layer in self.value:
            self.add_layer(layer['name'], layer['url'], options=layer['options'])

    def init_form(self):
        """
        Initialize the form
        """
        return """new ControlMap('{0}', {1})""".format(
            self._name,
            simplejson.dumps(self.serialize())
        )
    
    @property
    def layers(self):
        """
        Return the layers
        """
        return self._layers

    def on_enter_event(self):
        """
        Event called when the Enter key is pressed
        """
        pass

    def clear_layers(self):
        """
        Clear all layers from the map
        """
        self._commands.append({'command': 'clearLayers'})
        self._layers = {}
        self.mark_to_update_client()

    def fit_bounds(self, bounds):
        """
        Fit the map to the given bounds
        """
        self._commands.append({'command': 'fitBounds', 'bounds': bounds})
        self.mark_to_update_client()

    def add_layer(self, name, url, options=None):
        """
        Add a layer to the map
        """
        self._commands.append({'command': 'addLayer', 'url': url, 'name': name, 'options': options})
        self._layers[name] = url
        self.mark_to_update_client()

    def remove_layer(self, name):
        """
        Remove a layer from the map
        """
        self._commands.append({'command': 'removeLayer', 'name': name})
        self._layers.pop(name)
        self.mark_to_update_client()

    def set_z_index(self, name, z_index):
        """
        Set the z-index of a layer
        """
        self._commands.append({'command': 'setZIndex', 'name': name, 'z_index': z_index})
        self.mark_to_update_client()

    def set_layer_opacity(self, name, opacity):
        """
        Set the opacity of a layer
        """
        self._commands.append({'command': 'setOpacity', 'name': name, 'opacity': opacity})
        self.mark_to_update_client()



    def clear_markers(self):
        """
        Clear a markers from the map
        """
        self._commands.append({'command': 'clearMarkers'})
        self.mark_to_update_client()

    def add_marker(self, name, lat, long, icon=None, **kwargs):
        """
        Add a marker to the map
        """
        self._commands.append({
            'command': 'addMarker', 'coordinate': [lat, long], 'name': name,
            'iconUrl': icon,
            'options': kwargs
            })
        self.mark_to_update_client()

    def remove_marker(self, name):
        """
        Remove a marker from the map
        """
        self._commands.append({'command': 'removeMarker', 'name': name})
        self.mark_to_update_client()



    def add_editable_marker(self, name, lat, long, **kwargs):
        """
        Add a marker to the map
        """
        self._commands.append({'command': 'addEditableMarker', 'coordinate': [lat, long], 'name': name, 'options': kwargs})
        self.mark_to_update_client()

    def add_polyline(self, name, coordinates, **kwargs):
        """
        Add a polyline to the map
        """
        self._commands.append({'command': 'addPolyline', 'coordinates': coordinates, 'name': name, 'options': kwargs})
        self.mark_to_update_client()

    def remove_polyline(self, name):
        """
        Remove a polyline from the map
        """
        self._commands.append({'command': 'removePolyline', 'name': name})
        self.mark_to_update_client()

    def clear_polylines(self):
        """
        Clear a polylines from the map
        """
        self._commands.append({'command': 'clearPolylines'})
        self.mark_to_update_client()

    def add_polygon(self, name, coordinates, **kwargs):
        """
        Add a polygon to the map
        """
        self._commands.append({'command': 'addPolygon', 'coordinates': coordinates, 'name': name, 'options': kwargs})
        self.mark_to_update_client()

    def remove_polygon(self, name):
        """
        Remove a polygon from the map
        """
        self._commands.append({'command': 'removePolygon', 'name': name})
        self.mark_to_update_client()

   
    def add_editable_polygon(self, name, coordinates, **kwargs):
        """
        Add a editable polygon to the map
        """
        self._commands.append({'command': 'addEditablePolygon', 'coordinates': coordinates, 'name': name, 'options': kwargs})
        self.mark_to_update_client()

    def deserialize(self, properties):
        """
        Deserialize the properties
        """

        self.polygons = []
        for p in properties.get('polygons', []):
            poly = [(lat, long) for (long, lat) in p['geometry']['coordinates'][0]]
            self.polygons.append(poly)

        self.markers = []
        for m in properties.get('markers', []):
            coord = m['geometry']['coordinates']
            self.markers.append([coord[1], coord[0]])

        return super().deserialize(properties)

    def serialize(self):
        """
        Serialize the properties
        """

        res = super().serialize()
        res.update({
            'center': self.center,
            'zoom': self.zoom,
            'min_height': self._min_height,
            'commands': self._commands,
            'edit_polyline': self._edit_polyline,
            'edit_polygon': self._edit_polygon,
            'edit_marker': self._edit_marker,
            'edit_circlemarker': self._edit_circlemarker,
            'edit_circle': self._edit_circle,
            'edit_rectangle': self._edit_rectangle,
        })
        self._commands = []

        return res
