class BaseWidget {
    /**
     BaseWidget class handles the communication with the server python application.
     @param {string} widget_id - BaseWidget id.
     @param {string} widget_name - BaseWidget name.
     @param {list(ControlBase)} controls - List of the BaseWidget controls.
     @param {string} parent_id - Parent widget id.
     @param {object} data - Object instance with the application data.
     */
    constructor(widget_id, widget_name, controls, parent_id, data) {
        this.name = widget_name;
        this.widget_id = widget_id;
        this.controls = controls;
        this.events_queue = [];
        this.parent_id = parent_id;
        this.layout_position = data.layout_position;
        this.timeouts_loops = [];
        this.xmlhttp = undefined;
        this.stream_length = 0;
        this.keydown_codes = data['keydown_codes'];
        this.keydown_keycode = undefined;

        // variables used to verify if the loading layer needs to be shown or not
        this.loading_begin = undefined;
        this.loading_counter = 0;

        for (var index = 0; index < controls.length; index++) {
            const control = controls[index];
            control.basewidget = this;
            control.init_control();
        }

        for (var index = 0; index < controls.length; index++) {
            controls[index].after_init_control()
        }

        if (data.messages != undefined)
            for (var i = 0; i < data.messages.length; i++) {
                var msg = data.messages[i];
                if (msg.type != '') this.jquery().addClass(msg.type);

                var html = '<div class="ui ' + msg.type + ' message">';
                html += '<i class="close icon"></i>';
                if (msg.title) html += '<div class="header">' + msg.title + '</div>';
                if (msg.messages.length == 1) {
                    html += '<p>' + msg.messages[0] + '</p>';
                } else {
                    html += '<ul class="list">';
                    for (var i = 0; i < msg.messages.length; i++) html += '<li>' + msg.messages[i] + '</li>';
                    html += '</ul>';
                }

                $(html).prependTo(this.jquery()).find('.close').on('click', function () {
                    $(this).closest('.message').transition({
                        animation: 'fade', onComplete: function () {
                            $(this).remove();
                        }
                    });
                });
            }
        ;

        //add auto refresh
        if (data.refresh_timeout) {
            var self = this;
            this.refresh_timeout = data.refresh_timeout;
            this.timeout_loop = setInterval(function () {
                self.refresh_timeout_event();
            }, data.refresh_timeout);
        }

        $('#' + this.app_id()).click(() => {
            pyforms.active_app = this;
        });
    }

    ////////////////////////////////////////////////////////////

    /**
     Function called when the key is pressed.
     */
    key_pressed(evt) {
        if (this.keydown_codes && this.keydown_codes.indexOf(evt.keyCode) !== -1) {
            this.keydown_keycode = evt.keyCode;
            this.fire_event('self', 'keydown_event');
        }
    }

    ////////////////////////////////////////////////////////////

    /**
     Function used to call the server refresh_event.
     */
    refresh_timeout_event() {
        this.fire_event('self', 'refresh_event');
    }

    ////////////////////////////////////////////////////////////

    /**
     Returns the parent BaseWidget.
     @returns {BaseWidget}
     */
    parent_widget() {
        //if(this.parent!==undefined) return this.parent;
        if (this.parent_id !== undefined) {
            var parent = pyforms.find_app(this.parent_id);
            //if(parent!==undefined) this.parent = parent;
            return parent;
        } else
            return undefined;
    }

    ////////////////////////////////////////////////////////////

    /**
     Returns a control.
     @param {string} name - Control name.
     @returns {ControlBase}
     */
    find_control(name) {
        for (var index = 0; index < this.controls.length; index++)
            if (this.controls[index].name == name)
                return this.controls[index];

        return undefined;
    }

    ////////////////////////////////////////////////////////////

    /**
     Returns the App id.
     @returns {string}
     */
    app_id(name) {
        return 'app-' + this.widget_id;
    }

    ////////////////////////////////////////////////////////////

    /**
     Returns the BaseWidget id.
     @returns {string}
     */
    control_id(name) {
        return this.widget_id + '-' + name;
    }

    ////////////////////////////////////////////////////////////

    /**
     Fire an application event.
     @param {string} dom_id - Python object name.
     @param {string} event - Event name.
     @param {bool} show_loading - Flag to activate the loading.
     */
    fire_event(dom_in, event, show_loading) {

        var data = {event: {control: dom_in, event: event}};
        this.events_queue.push(data)

        if (this.parent_id === undefined)
            pyforms.query_server(this, this.events_queue.pop(0), show_loading);
        else {
            pyforms.query_server(this, undefined, show_loading);
        }
        ;
    }

    ////////////////////////////////////////////////////////////

    /**
     Update controls with the values from the server.
     */
    update_controls() {
        pyforms.query_server(this, {});
    }

    ////////////////////////////////////////////////////////////

    /**
     Deserializes the application from the data sent by the server.
     @param {object} data - Data to deserialize.
     */
    deserialize(data) {

        var js_code2excute = data['js-code'];
        if (js_code2excute && js_code2excute.length > 0)
            for (var i = 0; i < js_code2excute.length; i++)
                eval(js_code2excute[i]);


        for (var index = 0; index < this.controls.length; index++) {
            var control = this.controls[index];
            if (data[control.name]) {
                control.deserialize(data[control.name]);
                control.apply_deserialization()
            }
            ;
        }
        ;

        if (data.messages != undefined)
            for (var i = 0; i < data.messages.length; i++) {
                var msg = data.messages[i];
                if (msg.type != '') this.jquery().addClass(msg.type);

                var html = '<div class="ui ' + msg.type + ' message">';
                html += '<i class="close icon"></i>';
                if (msg.title) html += '<div class="header">' + msg.title + '</div>';
                if (msg.messages.length == 1)
                    html += '<p>' + msg.messages[0] + '</p>';
                else {
                    html += '<ul class="list">';
                    for (var i = 0; i < msg.messages.length; i++) html += '<li>' + msg.messages[i] + '</li>';
                    html += '</ul>';
                }
                ;

                var destination = this.jquery().find('.notifications-area');
                if (destination.length == 0)
                    destination = this.jquery()

                $(html).prependTo(destination).find('.close').on('click', function () {
                    $(this).closest('.message').transition({
                        animation: 'fade', onComplete: function () {
                            $(this).remove();
                        }
                    });
                });
            }
        ;


        if (data['close_widget']) {
            pyforms.close_layout_place(data);
            pyforms.remove_app(data['uid']);
        }

        //add auto refresh
        if (data['refresh_timeout'] != null) {
            if (this.refresh_timeout != data['refresh_timeout']) {
                var self = this;
                if (this.timeout_loop) {
                    clearInterval(this.timeout_loop);
                }
                this.refresh_timeout = data['refresh_timeout'];
                this.timeout_loop = setInterval(function () {
                    self.refresh_timeout_event();
                }, data['refresh_timeout']);
            }
        } else {
            if (this.timeout_loop) {
                clearInterval(this.timeout_loop);
                this.timeout_loop = null;
            }
        }
        ;

        //add auto refresh
        var timeouts = data['timeouts'];
        if (timeouts.length > 0) {
            for (var i = 0; i < timeouts.length; i++) {
                var self = this;
                var milliseconds = timeouts[i][0];
                var evt_name = timeouts[i][1];
                this.timeouts_loops.push(
                    setTimeout(function () {
                        self.fire_event('self', evt_name)
                    }, milliseconds)
                );
            }
        }

        // streaming
        if (data['abort_streaming']) {
            if (this.xmlhttp) {
                this.xmlhttp.abort()
                this.stream_length = 0;
            }
            this.xmlhttp = undefined;
        }
        if (data['start_streaming']) {
            const source = new EventSource(`/pyforms/app-stream/${this.widget_id}/`);
            source.onmessage = (evt) => {
                if (evt.data === 'STOP') {
                    source.close();
                } else {
                    this.stream_update(evt);
                }
            }
        }
    }

    ////////////////////////////////////////////////////////////

    stream_end() {
        this.stream_length = 0;
    }

    stream_update(oEvent) {
        this.deserialize(JSON.parse(oEvent.data));
    }

    ////////////////////////////////////////////////////////////
    /**
     Serializes the application to send to the server.
     @returns {object}.
     */
    serialize() {
        var data = undefined;
        if (this.events_queue.length > 0)
            data = this.events_queue.pop(0)
        else
            data = {};

        for (var index = 0; index < this.controls.length; index++) {
            var name = this.controls[index].name;
            data[name] = this.controls[index].serialize();
        }
        ;
        return data;
    }

    ////////////////////////////////////////////////////////////

    /**
     Serializes the application to send to the server.
     @returns {object}.
     */
    serialize_data(data) {
        for (var index = 0; index < this.controls.length; index++) {
            var control = this.controls[index];
            if (control.update_server()) {
                var name = control.name;
                data[name] = control.serialize();
            }
            ;
        }
        ;
        data['uid'] = this.widget_id;
        data['keydown_keycode'] = this.keydown_keycode;
        return data;
    }

    ////////////////////////////////////////////////////////////

    /**
     Event that check if the loading event should be on or off.
     @returns {bool}.
     */
    activate_load_event() {
        if (this.loading_counter <= 0) {
            this.jquery().removeClass('loading');
            return false; //exit the checker
        }

        if (this.loading_begin != undefined && (Date.now() - this.loading_begin) > PYFORMS_CHECKER_LOOP_INTERVAL && !this.jquery().hasClass('loading'))
            this.jquery().addClass('loading')

        return true;
    }

    /**
     Activate the load.
     */
    loading() {
        //console.debug('loading');
        //this.jquery().addClass('loading');
        if (this.loading_begin == undefined) this.loading_begin = Date.now();
        this.loading_counter++;
        if (this.loading_counter == 1) {
            var self = this;
            pyforms.register_checkloop(function () {
                return self.activate_load_event()
            });
        }
    }

    ////////////////////////////////////////////////////////////

    /**
     Deactivate the loading.
     */
    not_loading() {
        //console.debug('not_loading');
        //this.jquery().removeClass('loading');

        this.loading_counter--;
        pyforms.checker_loop();
    }

    ////////////////////////////////////////////////////////////

    /**
     Close child apps
     */
    close_sub_apps() {

        for (var index = 0; index < this.controls.length; index++) {
            if (this.controls[index].properties.child_widget_id !== undefined)
                pyforms.remove_app(this.controls[index].properties.child_widget_id);
        }
        ;
    }

    ////////////////////////////////////////////////////////////

    /**
     Query the server.
     @returns {object}.
     */
    query_server(params) {
        pyforms.query_server(this, params);
    }


    ////////////////////////////////////////////////////////////

    /**
     Get the jquery object.
     @returns {jquery}.
     */
    jquery() {
        return $("#app-" + this.widget_id);
    }

    ////////////////////////////////////////////////////////////

    /**
     Close the app.
     */
    close() {
        clearTimeout(this.timeout_loop);
        for (var i = 0; i < this.timeouts_loops.length; i++)
            clearTimeout(this.timeouts_loops[i]);
        this.close_sub_apps();
        this.jquery().remove();
    }

}