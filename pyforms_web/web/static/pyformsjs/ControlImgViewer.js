class ControlImgViewer extends ControlBase {


    ////////////////////////////////////////////////////////////////////////////////
    init_control() {
        var html = `<div id='${this.place_id()}' class='field control ControlImgViewer' >`;
        if (this.properties.label_visible)
            html += `<label for='${this.control_id()}'>${this.properties.label}</label>`;
        html += `<div id='${this.control_id()}'></div>`;

        this.jquery_place().replaceWith(html);

        if (this.properties.value) {
            this.set_value(this.properties.value);
        }
        if (this.properties.required) this.set_required();
    };

    ////////////////////////////////////////////////////////////////////////////////

    set_value(value) {
        if (this.zoomist) {
            this.zoomist.destroy();
            this.zoomist = undefined;
        }
        if (value !== undefined && value !== '') {
            this.jquery().attr('data-zoomist-src', value);
            this.zoomist = new Zoomist('#' + this.control_id(), {
                slider: {
                    direction: 'vertical'
                }
            });
        }
    };
}