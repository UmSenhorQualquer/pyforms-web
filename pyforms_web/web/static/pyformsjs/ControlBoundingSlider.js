class ControlBoundingSlider extends ControlBase{

	////////////////////////////////////////////////////////////////////////////////


	set_label(value){
		const values = this.jquery().slider('option', 'values');

        $( `#${this.place_id()} label[for='${this.control_id()}']` ).first().html(
			`${this.properties.label}: <small id='value-${this.control_id()}' style='color:red' >${values}</small>`
		);
    }

	////////////////////////////////////////////////////////////////////////////////

	set_value(val){
		console.debug(val)
		this.jquery().slider({values:val['value']})
		console.debug(String(val['value']))
		$("#value-"+this.control_id() ).html( String(val['value']));
	};

	////////////////////////////////////////////////////////////////////////////////

	get_value(){
		return { value: this.jquery().slider("values"), max: this.properties.max, min: this.properties.min }
	};

	////////////////////////////////////////////////////////////////////////////////

	init_control(){
		var html =	"<div class='ControlBoundingSlider field control' id='"+this.place_id()+"' title='"+this.properties.help+"'   >";
		html +=		"<label style='margin-right: 20px;' for='"+this.control_id()+"'>"+this.properties.label+": <small id='value-"+this.control_id()+"' style='color:red' >"+this.properties.value+"</small></label>";
		html += 	"<div style='width:100%;' class='slider' name='"+this.name+"' id='"+this.control_id()+"' ></div>";
		html += 	"</div>";
		this.jquery_place().replaceWith(html);

		var self = this;
		this.jquery().slider({ 
			range: true,
			stop:  function(event, ui){
				self.basewidget.fire_event( self.name, 'update_control_event' );
			},
			min: self.properties.min,
			max: self.properties.max,
			values: self.properties.value
		});

		if(this.properties.required) this.set_required();
	};

	////////////////////////////////////////////////////////////////////////////////


	
}

