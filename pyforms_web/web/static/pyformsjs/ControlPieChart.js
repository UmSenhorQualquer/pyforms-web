class ControlPieChart extends ControlBase{

    
    ////////////////////////////////////////////////////////////////////////////////

    init_control(){
        var html =  "<div id='"+this.place_id()+"' class='field control ControlPieChart' >";
        if(this.properties.label_visible) html += "<label for='"+this.control_id()+"'>"+this.properties.label+"</label>";
		html +=     "<div id='chart-container-"+this.control_id()+"' title='"+this.properties.help+"'   >";
        html +=     "<div id='"+this.control_id()+"' ></div>";
        html +=     "</div>";
        html +=     "</div>";
        this.jquery_place().replaceWith(html);
        var self   = this;
        var legend = true;
        var data   = this.properties.value;

        if(!data || data.length==0){ 
            data = [['Empty',0]];
        };

        var chart = jQuery.jqplot(this.control_id(), [data], 
            {
                seriesColors:['#f2711c', '#fbbd08', '#b5cc18', '#21ba45', '#00b5ad',
                    '#2185d0', '#6435c9', '#a333c8', '#e03997', '#a5673f', '#767676', '#1b1c1d', '#DB2828'],
                seriesDefaults: {
                    // Make this a pie chart.
                    renderer: jQuery.jqplot.PieRenderer, 
                    rendererOptions: {
                        // Put data labels on the pie slices.
                        // By default, labels show the percentage of the slice.
                        showDataLabels: true
                    }
                }, 
                legend: { 
                    show: true,
                    rendererOptions: {
                        numberRows: data.length/3
                    },
                    placement: this.properties.legend_placement,
                    location: this.properties.legend_location
                }
            }
        );

        this.chart = chart;

        var temp = {
            seriesStyles: {
                shadow: false,
                gridBorderWidth: 0,
                color: 'white'
            },
            grid: {
                backgroundColor: 'white',
                borderWidth: 0,
                gridLineColor: 'white',
                gridLineWidth: 0,
                borderColor: 'white',
                shadow: false
            },
            legend: {
                background: 'white',
                textColor: '#CCC',
                border: '0px solid white'
            }
        };
    
        chart.themeEngine.newTheme('simple', temp);
        chart.activateTheme('simple');
		if(this.properties.required) this.set_required();
    };


    ////////////////////////////////////////////////////////////////////////////////

    set_value(value){
        var options = {
            data: [value],
            legend: { 
                show: true,
                rendererOptions: {
                    numberRows: value.length/3
                }, 
                placement: "outside",
                location: 's'
            }
    };
        this.chart.replot(options);
    };

    ////////////////////////////////////////////////////////////////////////////////

    get_value(){ 
        return this.properties.value; 
    };

    ////////////////////////////////////////////////////////////////////////////////
    /*
    deserialize(data){
        this.properties = $.extend(this.properties, data);
        this.set_value(this.properties.value);
    };

    ////////////////////////////////////////////////////////////////////////////////

    serialize(){
        this.properties.value = this.get_value();
        return this.properties; 
    };*/
}

    
