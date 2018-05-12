class ControlVisVis extends ControlBase{

	
	////////////////////////////////////////////////////////////////////////////////

	init_control(){
		var html =  "<div id='"+this.place_id()+"' class='field control ControlVisVis' >";
		html += 	"<div id='chart-container-"+this.control_id()+"' title='"+this.properties.help+"'   >";
		html += 	"<div id='"+this.control_id()+"' ></div>";
		html += 	"</div>";
		html += 	"</div>";
		this.jquery_place().replaceWith(html);
		var self = this;
		var legend = self.properties.legend;
		var data   = self.properties.value;

		if(data.length==0 || data[0].length==0 ){ 
			data = [[[0,0]]];
		};
		var chart = $.jqplot(this.control_id(), data, {
			grid:{ borderColor: 'transparent', shadow: false, drawBorder: false, shadowColor: 'transparent', background: 'transparent'},
	 		title:self.label,
	 		seriesDefaults:{
				showMarker:false, showLine:true, lineWidth:1,
				markerOptions:{ size: 6 }
			},
			legend: {
				show: legend.length>0,				
				labels: legend,
				placement: "outside",
				location: 'e'
			},
			axes:{
				xaxis:{
					renderer: 		$.jqplot.DateAxisRenderer, 
					labelRenderer: 	$.jqplot.CanvasAxisLabelRenderer,
					tickRenderer: 	$.jqplot.CanvasAxisTickRenderer,
					tickOptions: {angle: -45}
				}
			},
			cursor:{
				show: true, 
				zoom: true
			}
		});

		this.chart = chart;

		
	};


	////////////////////////////////////////////////////////////////////////////////

	set_value(value){
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
		this.chart.replot(options);
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

	
