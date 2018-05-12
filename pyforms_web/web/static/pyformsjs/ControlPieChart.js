class ControlPieChart extends ControlBase{

    
    ////////////////////////////////////////////////////////////////////////////////

    init_control(){
        var html =  "<div id='"+this.place_id()+"' class='field control ControlPieChart' >";
        html +=     "<div id='chart-container-"+this.control_id()+"' title='"+this.properties.help+"'   >";
        html +=     "<div id='"+this.control_id()+"' ></div>";
        html +=     "</div>";
        html +=     "</div>";
        this.jquery_place().replaceWith(html);
        var self   = this;
        var legend = self.properties.legend;
        var data   = self.properties.value;

        if(data.length==0 || data[0].length==0 ){ 
            data = [[[0,0]]];
        };

        var chart = jQuery.jqplot(this.control_id(), data, 
            { 
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
                        numberRows: 6
                    }, 
                    location: 'e'
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

        
    };


    ////////////////////////////////////////////////////////////////////////////////

    set_value(value){/*
        var self = this;
        var options = {
            data: value,
            legend: {
                show: self.properties.legend.length>0,
                labels: self.properties.legend,
                showLabels: true,
                showSwatch: true
            }
        };
        this.chart.replot(options);*/
    };

    ////////////////////////////////////////////////////////////////////////////////

    get_value(){ 
        return this.properties.value; 
    };

    ////////////////////////////////////////////////////////////////////////////////

    deserialize(data){
        this.properties = $.extend(this.properties, data);
        this.set_value(this.properties.value);
    };

    ////////////////////////////////////////////////////////////////////////////////

    serialize(){
        this.properties.value = this.get_value();
        return this.properties; 
    };
}

    
