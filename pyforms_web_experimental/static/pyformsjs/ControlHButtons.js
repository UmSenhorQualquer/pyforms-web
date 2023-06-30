class ControlHButtons extends ControlBase {


    ////////////////////////////////////////////////////////////////////////////////

    init_control() {
        var html = `<div class='field control ControlHButtons' id='${this.place_id()}'>
        <div id='${this.control_id()}'></div>`;
        this.jquery_place().replaceWith(html);
        this.build_buttons();

        if (this.properties.required) this.set_required();
    };

    build_buttons() {
        const items = this.properties.items;


        if (items.length) {
            let html = '<div class="ui pagination menu tiny">';

            if (this.properties.first_page > 0) {
                html += `<a first-page-idx="${this.properties.first_page - 1}" class="icon item" ><i class="left chevron icon"></i></a>`;
            }

            for (var i = 0; i < items.length; i++) {
                html += `<a current-page-idx="${items[i].page_idx}" val="${items[i].value}" class="item ${items[i].page_idx == this.properties.current_page ? 'active' : ''}">${items[i].text}</a>`;
            }

            if ((this.properties.first_page + items.length) < this.properties.total_items) {
                html += `<a first-page-idx="${this.properties.first_page + 1}" class="icon item"><i class="right chevron icon"></i></a>`;
            }
            html += '</div></div>';
            this.jquery().html(html);

            let self = this;
            $(`#${this.control_id()} .item`).click(function () {
                if (!$(this).hasClass('active')) {
                    self.update_server_flag = true;

                    const current_page_idx = $(this).attr('current-page-idx');
                    if (current_page_idx) {
                        self.properties.current_page = parseInt(current_page_idx);
                        self.properties.value = $(this).attr('val');
                    }

                    const first_page_idx = $(this).attr('first-page-idx');
                    if (first_page_idx) {
                        self.properties.first_page = parseInt(first_page_idx);
                    }
                    self.basewidget.fire_event(self.name, 'page_changed_event');
                }
            });
        } else {
            this.jquery().html(this.properties.default_text);
        }
    }

    ////////////////////////////////////////////////////////////////////////////////

    get_value() {
        return this.properties.value;
    };

    update_server() {
        return this.update_server_flag;
    }

    serialize() {
        this.update_server_flag = false;
        return super.serialize();
    }

    ////////////////////////////////////////////////////////////////////////////////

    deserialize(data) {
        $.extend(this.properties, data);
        this.build_buttons()
        this.set_value(this.properties.value);

        if (this.properties.error) this.jquery_place().addClass('error'); else this.jquery_place().removeClass('error');
    };

}