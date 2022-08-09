class ControlTemplate extends ControlBase {

    ////////////////////////////////////////////////////////////////////////////////

    init_control() {
        var html = "<div id='" + this.place_id() + "' class='field control ControlTemplate' ><div id='" + this.control_id() + "' ></div></div>";
        this.jquery_place().replaceWith(html);

        this.set_value(this.properties.value);
        if (this.properties.required) this.set_required();
    };

    ////////////////////////////////////////////////////////////////////////////////


    set_value(value) {
        var html = Base64.decode(value);

        if (html) {
            this.jquery().html(html);
            this.set_actions();
        } else
            this.jquery().html('');
    };

    ////////////////////////////////////////////////////////////////////////////////

    set_actions() {
        this.properties.action_param = undefined;
        const self = this;

        this.jquery().find('[action]').click(function () {
            const action = $(this).attr('action');
            const action_param = $(this).attr('action-param');
            self.properties.action_param = action_param;
            self.basewidget.fire_event('self', action);
        });

        this.jquery().find('[submit-action]').click(function() {
            const action = $(this).attr('submit-action');
            const values = {};
            self.jquery().find('[submit-action-name]').each(function(){
                const name = $(this).attr('submit-action-name')
                const value = $(this).is(":checked");
                values[name] = value;
            });
            self.properties.submit_action_data = values;
            self.basewidget.fire_event('self', action);
        });
    };


    update_server() {
        return (this.properties.action_param != undefined) ||
            (this.properties.submit_action_data != undefined);
    };

}