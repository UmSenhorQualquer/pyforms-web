class ControlLineChart extends ControlBase {

    ////////////////////////////////////////////////////////////////////////////////

    init_control() {
        this.update_it = false;

        var html = "<div id='" + this.place_id() + "' class='field control ControlLineChart' >";
        if (this.properties.label_visible) html += "<label for='" + this.control_id() + "'>" + this.properties.label + "</label>";
        html += "<div id='" + this.control_id() + "' title='" + this.properties.help + "' style='margin-left: 20px' ></div>";
        html += "</div>";
        this.jquery_place().replaceWith(html);

        if (this.properties.value) {
            this.set_value(this.properties.value);
        }

        if (this.properties.required) this.set_required();
    };


    ////////////////////////////////////////////////////////////////////////////////

    set_value(data) {
        if( !this.jquery( ).length ) return;

        if (this.chart) {
            this.chart.destroy();
        }

        var legend = this.properties.legend;

        if (!data || data.length == 0 || data[0].length == 0) {
            data = [[[0, 0]]];
        }

        console.debug(data);
        console.debug(this.properties);

        this.chart = $.jqplot(this.control_id(), data, {
            height: this.properties.height,
            width: this.properties.width,
            seriesColors: [
                '#f2711c', '#fbbd08', '#b5cc18', '#21ba45', '#00b5ad',
                '#2185d0', '#6435c9', '#a333c8', '#e03997', '#a5673f',
                '#767676', '#1b1c1d', '#DB2828'
            ],
            grid: {
                borderColor: 'transparent',
                shadow: false,
                drawBorder: false,
                shadowColor: 'transparent',
                background: 'transparent'
            },
            title: this.label,
            seriesDefaults: {
                showMarker: this.properties.show_marker, 
                showLine: true, 
                lineWidth: 1,
                markerOptions: {size: 4},
                rendererOptions: {
                    smooth: this.properties.smooth
                }
            },
            legend: {
                show: legend.length > 0,
                labels: legend,
                placement: this.properties.legend_placement,
                location: this.properties.legend_location
            },
            axes: {
                xaxis: {
                    renderer: this.properties.x_axis_type==='datetime'?$.jqplot.DateAxisRenderer:$.jqplot.LinearAxisRenderer,
                    tickOptions: {formatString: this.properties.x_axis_format},
                    min: this.properties.xaxis_range? new Date(this.properties.xaxis_range[0]): null,
                    max: this.properties.xaxis_range? new Date(this.properties.xaxis_range[1]): null,
                }
            },
            cursor: {
                style: 'pointer',
                show: true,
                zoom: true,
                tooltipOffset: 10,
                showTooltip: true,
                followMouse: true,
                showTooltipDataPosition: true,
                showVerticalLine: true
            }
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

	
