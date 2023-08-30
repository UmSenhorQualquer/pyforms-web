class ControlChartJsLine extends ControlBase {

    ////////////////////////////////////////////////////////////////////////////////

    init_control() {
        this.update_it = false;

        var html = "<div id='" + this.place_id() + "' class='field control ControlChartJsLine' >";
        if (this.properties.label_visible) html += "<label for='" + this.control_id() + "'>" + this.properties.label + "</label>";
        html += `<canvas id="${this.control_id()}"></canvas>`;
        html += "</div>";
        this.jquery_place().replaceWith(html);

        if (this.properties.value) {
            this.set_value(this.properties.value);
        }

        if (this.properties.required) this.set_required();
    };


    ////////////////////////////////////////////////////////////////////////////////

    set_value(data) {
        if (!this.jquery().length) return;

        if (this.chart) {
            this.chart.destroy();
        }

        var legend = this.properties.legend;

        if (!data || data.length == 0 || data[0].length == 0) {
            data = [[[0, 0]]];
        }

        var ctx = document.getElementById(this.control_id()).getContext('2d');
        var chart = new Chart(ctx, {
            // The type of chart we want to create
            type: 'line',
            // The data for our dataset
            data: {
                labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
                datasets: [{
                    label: 'My First dataset',
                    backgroundColor: 'rgb(255, 99, 132)',
                    borderColor: 'rgb(255, 99, 132)',
                    pointStyle: 'line',
                    lineTension: 0,
                    data: [0, 10, 5, 2, 20, 30, 45]
                }]
            },
            // Configuration options go here
            options: {}
        });

        const self = this;
        this.jquery().bind('jqplotDataClick',
            function (ev, seriesIndex, pointIndex, data) {
                self.properties.selected_series = seriesIndex;
                self.properties.selected_data = data;
                self.update_it = true;
                self.basewidget.fire_event(self.name, 'remote_data_selected_event');
            }
        );

        if (this.properties.visible)
            this.show();
        else
            this.hide();
    };

    ////////////////////////////////////////////////////////////////////////////////

    update_server() {
        return this.get_value() != this.properties.value || this.update_it;
    }

    ////////////////////////////////////////////////////////////////////////////////

    deserialize(data) {
        this.properties = $.extend(this.properties, data);
    };

    apply_deserialization(data) {
        super.apply_deserialization(data);
        this.set_value(this.properties.value);
    }

    ////////////////////////////////////////////////////////////////////////////////

    serialize() {
        this.properties.value = this.get_value();
        return this.properties;
    };
}

	
