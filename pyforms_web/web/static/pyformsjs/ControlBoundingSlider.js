class ControlBoundingSlider extends ControlBase{


	////////////////////////////////////////////////////////////////////////////////

	set_value(value){
		this.jquery().slider({values:val})
		$("#value-"+this.control_id() ).html( val );
	};

	////////////////////////////////////////////////////////////////////////////////

	get_value(){
		return { value: this.jquery().slider("values"), max: this.properties.max, min: this.properties.min }
	};

	////////////////////////////////////////////////////////////////////////////////

	init_control(){
		var html =	"<div class='ControlSlider field control' id='"+this.place_id()+"' title='"+this.properties.help+"'   >";
		html +=		"<label style='margin-right: 20px;' for='"+this.control_id()+"'>"+this.properties.label+": <small id='value-"+this.control_id()+"' style='color:red' >"+this.properties.value+"</small></label>";
		html += 	"<div style='width:100%;' class='slider' name='"+this.name+"' id='"+this.control_id()+"' ></div>";
		html += 	"</div>";
		this.jquery_place().replaceWith(html);

		var self = this;
		this.jquery().slider({ 
			range: true,
			slide: function( event, ui ) { $( "#value-"+self.control_id() ).html( ui.value ); },
			stop:  function(){ self.basewidget.fire_event( self.name, 'update_control_event' )}, 
			min: this.properties.min, max: this.properties.max, values: this.properties.value 
		});	
	};

	////////////////////////////////////////////////////////////////////////////////


	
}

