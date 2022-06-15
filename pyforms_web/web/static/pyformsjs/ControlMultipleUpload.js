class ControlMultipleUpload extends ControlBase {

    init_control() {
        var html = "<div class='field control ControlMultipleUpload' id='" + this.place_id() + "' ><label for='" + this.control_id() + "'>" + this.properties.label + "</label>";
        html += '<input type="file" name="' + this.name + '" id="' + this.control_id() + '" placeholder="' + this.properties.label + '" >';
        html += "</div>";

        this.modified = false;

        this.jquery_place().replaceWith(html);

        this.properties.new_value = [];
        this.files = [];

        this.jquery().filer({
            uploadFile: {
                url: PYFORMS_SERVER_URL + '/pyforms/upload-files/',
                data: {app_id: this.app_id(), control_id: this.name},
                type: 'POST',
                enctype: 'multipart/form-data', //Request enctype {String}
                synchron: false, //Upload synchron the files
                /*beforeSend: function () {
                    //self.basewidget.loading();
                }, //A pre-request callback function {Function}*/
                success: (data, itemEl, listEl, boxEl, newInputEl, inputEl, id) => {
                    this.files.push(data.metas[0]);
                },
                onComplete: (listEl, parentEl, newInputEl, inputEl, jqXHR, textStatus) => {
                    //const filerKit = self.jquery().prop("jFiler");
                    this.modified = true;
                    this.properties.new_value = this.files.map(x => {
                        return x.file;
                    });
                    console.debug('--', this.properties.new_value);
                    this.basewidget.fire_event(this.name, 'update_control_event');
                    //self.basewidget.not_loading();
                },
                error: null, //A function to be called if the request fails {Function}
                statusCode: null, //An object of numeric HTTP codes {Object}
                onProgress: null, //A function called while uploading file with progress percentage {Function}
            },
            showThumbs: true,
            addMore: true,
            allowDuplicates: false,
            onRemove: (itemEl, file, id, listEl, boxEl, newInputEl, inputEl) => {
                this.modified = true;

                this.properties.new_value = this.properties.value.filter(x => {
                    return x.localeCompare(file.file) !== 0;
                });
                console.debug(this.properties.value, file.file, this.properties.new_value)
                this.basewidget.fire_event(this.name, 'update_control_event');
            },
        });

        if (this.properties.file_data) {
            var filerKit = this.jquery().prop("jFiler");
            if (this.properties.file_data) {
                this.properties.file_data.forEach(x => {
                    filerKit.append(x);
                });
            }
        }
        ;

        if (this.properties.error) this.jquery_place().addClass('error'); else this.jquery_place().removeClass('error');
        if (this.properties.required) this.set_required();

    };

    update_server() {
        return this.modified;
    }

    get_value() {
        if (this.properties.new_value === undefined) return this.properties.value;
        return this.properties.new_value;
    };

    ////////////////////////////////////////////////////////////////////////////////

    set_value(value) {
        var filerKit = this.jquery().prop("jFiler");
        filerKit.reset();
        if (this.properties.file_data) {
            this.properties.file_data.forEach(x => {
                filerKit.append(x);
            });
        }
        ;
    };

    ////////////////////////////////////////////////////////////////////////////////

    serialize() {
        const data = super.serialize();
        this.modified = false;
        return data
    }

    deserialize(data) {
        this.properties.file_data = undefined;
        this.properties.new_value = undefined;
        this.properties = $.extend(this.properties, data);
        this.set_value(this.properties.value);

        if (this.properties.error) this.jquery_place().addClass('error'); else this.jquery_place().removeClass('error');
    };
}
	