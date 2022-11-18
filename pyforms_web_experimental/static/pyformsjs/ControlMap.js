class ControlMap extends ControlBase {

    ////////////////////////////////////////////////////////////////////////////////
    init_control() {
        super.init_control();
        this.layers = {};

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

        var options = {
            position: 'topleft',
            draw: {
                polyline: this.properties.edit_polyline,
                polygon: this.properties.edit_polygon,
                marker: this.properties.edit_marker,
                circlemarker: this.properties.edit_circlemarker,
                circle: this.properties.edit_circle,
                rectangle: this.properties.edit_rectangle
            },
            edit: {
                featureGroup: this.editableLayers, //REQUIRED!!
                remove: true
            }
        };

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

        if (this.properties.add_polygons) {
            this.properties.add_polygons.forEach(p => {
                const poly = L.polygon(p.coordinates, p);
                this.editableLayers.addLayer(poly);
            });
        }

        if (this.properties.commands) {
            this.properties.commands.forEach(c => {
                switch (c.command) {
                    case 'setOpacity':
                        this.layers[c.layer_url].setOpacity(c.opacity);
                        break;
                    case 'addLayer':
                        this.layers[c.layer_url] = L.tileLayer(c.layer_url, c.options).addTo(this.map);
                        break;
                    case 'setZIndex':
                        this.layers[c.layer_url].setZIndex(c.zindex);
                        break;
                    case 'removeLayer':
                        this.layers[c.layer_url].removeFrom(this.map);
                        break;
                    case 'fitBounds':
                        this.map.fitBounds(c.bounds)
                        console.debug(c)
                        break;
                }
            });
        }

        this.properties.add_markers = [];
        this.properties.add_polygons = [];
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

    /*
        enable() {
            this.drawControl.enable();
        }

        disable() {
            this.drawControl.disable();
        }
        */
}
