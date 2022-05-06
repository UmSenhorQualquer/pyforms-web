class ControlMultipleUpload extends ControlBase {

    init_control() {
        var html = "<div class='field control ControlMultipleUpload' id='" + this.place_id() + "' ><label for='" + this.control_id() + "'>" + this.properties.label + "</label>";
        html += '<input type="file" name="' + this.name + '" id="' + this.control_id() + '" placeholder="' + this.properties.label + '" >';
        html += "</div>";

        this.jquery_place().replaceWith(html);

        this.files = {};

        var self = this;
        this.jquery().filer({
            uploadFile: {
                url: PYFORMS_SERVER_URL + '/pyforms/upload-files/',
                data: {app_id: this.app_id(), control_id: this.name},
                type: 'POST',
                enctype: 'multipart/form-data', //Request enctype {String}
                synchron: false, //Upload synchron the files
                beforeSend: function () {
                    self.basewidget.loading();
                }, //A pre-request callback function {Function}
                success: function(data, itemEl, listEl, boxEl, newInputEl, inputEl, id){
					self.files[data.metas[0].name] = data.metas[0];
				},
				onComplete: function (listEl, parentEl, newInputEl, inputEl, jqXHR, textStatus) {
                    const filerKit = self.jquery().prop("jFiler");
                    self.properties.new_value = filerKit.files_list.map(x => {
                        return self.files[x.file.name].file;
                    });
                    self.basewidget.fire_event(self.name, 'update_control_event');
                    self.basewidget.not_loading();
                },
                error: null, //A function to be called if the request fails {Function}
                statusCode: null, //An object of numeric HTTP codes {Object}
                onProgress: null, //A function called while uploading file with progress percentage {Function}
            },
            showThumbs: true,
            addMore: true,
            allowDuplicates: false,
            onRemove: function (itemEl, file, id, listEl, boxEl, newInputEl, inputEl) {
                self.properties.new_value = '';
                self.basewidget.fire_event(self.name, 'update_control_event');
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
        };
    };

    ////////////////////////////////////////////////////////////////////////////////

    deserialize(data) {
        this.properties.file_data = undefined;
        this.properties.new_value = undefined;
        this.properties = $.extend(this.properties, data);
        this.set_value(this.properties.value);

        if (this.properties.error) this.jquery_place().addClass('error'); else this.jquery_place().removeClass('error');
    };
}
	