class ControlMap extends ControlBase {

    ////////////////////////////////////////////////////////////////////////////////
    init_control() {
        super.init_control();
        this.map_objects = {};

        this.jquery_place().replaceWith(
            `<div id='${this.place_id()}' class='field control ControlMap' >
                ${this.properties.label_visible ? `<label for="${this.control_id()}">${this.properties.label}</label>` : ''}
                <div style="min-height: ${this.properties.min_height}px;" id='${this.control_id()}' placeholder='${this.properties.placeholder}' />
            </div>`
        );

        if (this.properties.error)
            this.jquery_place().addClass('error');
        else
            this.jquery_place().removeClass('error');

        if (this.properties.required) this.set_required();


        // Delay the map initialization for rendering proposes.
        setTimeout(() => {
            this.initMap();
        }, 500);
    };

    ////////////////////////////////////////////////////////////////////////////////

    initMap() {
        this.map = L.map(this.control_id()).setView(
            this.properties.center,
            this.properties.zoom
        );
        this.initEditPolygon();
        this.process_commands();
    }

    initEditPolygon() {
        this.editableLayers = new L.FeatureGroup();
        this.map.addLayer(this.editableLayers);

        let options = {
            position: 'topleft',
            draw: {
                polyline: this.properties.edit_polyline,
                polygon: this.properties.edit_polygon,
                marker: this.properties.edit_marker,
                circlemarker: this.properties.edit_circlemarker,
                circle: this.properties.edit_circle,
                rectangle: this.properties.edit_rectangle
            }
        };

        if (
            this.properties.edit_polyline ||
            this.properties.edit_polygon ||
            this.properties.edit_marker ||
            this.properties.edit_circlemarker ||
            this.properties.edit_circle ||
            this.properties.edit_rectangle
        ) {
            options.edit = { featureGroup: this.editableLayers, remove: true };
        }

        this.drawControl = new L.Control.Draw(options);
        this.map.addControl(this.drawControl);

        this.map.on(L.Draw.Event.CREATED, e => {
            this.editableLayers.addLayer(e.layer);
            this.basewidget.fire_event(this.name, 'update_control_event');
        });

        this.map.on(L.Draw.Event.EDITED, e => {
            this.basewidget.fire_event(this.name, 'update_control_event');
        });

        this.map.on(L.Draw.Event.DELETED, e => {
            this.basewidget.fire_event(this.name, 'update_control_event');
        });
    }

    process_commands() {

        if (this.properties.add_markers) {
            this.properties.add_markers.forEach((m, idx) => {
                const marker = L.marker(m.coordinate, m);
                this.editableLayers.addLayer(marker);
            });
        }

        if (this.properties.commands) {
            this.properties.commands.forEach(c => {                
                switch (c.command) {
                    case 'clearLayers':
                        for (const key in this.map_objects)
                            if (key.startsWith('layer-')) {
                                this.map_objects[key].removeFrom(this.map);
                                delete this.map_objects[key];
                            }
                        break;
                    case 'fitBounds':
                        this.map.fitBounds(c.bounds)
                        break;
                    case 'addLayer':
                        this.map_objects[`layer-${c.name}`] = L.tileLayer(c.url, c.options).addTo(this.map);
                        break;
                    case 'removeLayer':
                        this.map_objects[`layer-${c.name}`].removeFrom(this.map);
                        delete this.map_objects[`layer-${c.name}`];
                        break;
                    case 'setZIndex':
                        this.map_objects[`layer-${c.name}`].setZIndex(c.z_index);
                        break;
                    case 'setOpacity':
                        this.map_objects[`layer-${c.name}`].setOpacity(c.opacity);
                        break;

                    case 'clearMarkers':
                        for (const key in this.map_objects)
                            if (key.startsWith('marker-')) {
                                this.map_objects[key].removeFrom(this.map);
                                delete this.map_objects[key];
                            }
                        break;
                    case 'addMarker':
                        
                        if(c.iconUrl !== undefined || c.iconUrl !== null){
                            console.debug('addMarker', c);
                            c.options.icon = L.icon({
                                iconUrl: c.iconUrl,
                                iconSize: [25, 25]
                            });
                        }
                        console.debug('-addMarker', c);
                        this.map_objects[`marker-${c.name}`] = L.marker(c.coordinate, c.options).addTo(this.map);
                        break;
                    case 'removeMarker':
                        this.map_objects[`marker-${c.name}`].removeFrom(this.map);
                        delete this.map_objects[`marker-${c.name}`];
                        break;


                    case 'addEditableMarker':
                        const marker = L.marker(c.coordinate, c.options);
                        this.editableLayers.addLayer(marker);
                        this.map_objects[`editable-marker-${c.name}`] = marker;
                        break;
                    case 'addPolyline':
                        this.map_objects[`polyline-${c.name}`] = L.polyline(c.coordinates, c.options).addTo(this.map);
                        break;
                    case 'removePolyline':
                        this.map_objects[`polyline-${c.name}`].removeFrom(this.map);
                        delete this.map_objects[`polyline-${c.name}`];
                        break;
                    case 'clearPolylines':
                        for (const key in this.map_objects)
                            if (key.startsWith('polyline-')) {
                                this.map_objects[key].removeFrom(this.map);
                                delete this.map_objects[key];
                            }
                        break;
                    case 'addPolygon':
                        this.map_objects[`polygon-${c.name}`] = L.polygon(c.coordinates, c.options).addTo(this.map);
                        break;
                    case 'removePolygon':
                        this.map_objects[`polygon-${c.name}`].removeFrom(this.map);
                        delete this.map_objects[`polygon-${c.name}`];
                        break;

                    case 'addEditablePolygon':
                        const poly = L.polygon(c.coordinates, c.options);
                        this.editableLayers.addLayer(poly);
                        this.map_objects[`editable-polygon-${c.name}`] = poly;
                        break;

                        ß
                }
            });
        }
        this.properties.commands = [];

    }

    serialize() {
        const polygons = [];
        const markers = [];
        this.map.eachLayer(l => {
            if (l instanceof L.Polygon) {
                polygons.push(l.toGeoJSON())
            } else if (l instanceof L.Marker && l.options && l.options.pane === "markerPane") {
                markers.push(l.toGeoJSON())
            }
        });

        this.properties.polygons = polygons;
        this.properties.markers = markers;

        return super.serialize();
    }

    deserialize(data) {
        super.deserialize(data);
        if (this.map) {
            this.process_commands();
        }
    }

}
