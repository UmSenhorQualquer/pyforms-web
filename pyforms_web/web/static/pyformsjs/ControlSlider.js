class ControlSlider extends ControlBase{

	
	////////////////////////////////////////////////////////////////////////////////

	get_value(){ 
		return this.jquery().val();
	};

	////////////////////////////////////////////////////////////////////////////////

	set_value(value){
		this.jquery().val(value);
		$( "#value"+this.name ).html( value );
		this.jquery().attr('max', this.properties.max);
		this.jquery().attr('min', this.properties.min);
	};

	////////////////////////////////////////////////////////////////////////////////

	init_control(){

		this.jquery_place().replaceWith(
			`<div id='${this.place_id()}' class='field control ControlSlider' title='${this.properties.help}' >
				<label for='${this.control_id()}'>${this.properties.label} (<span id='value${this.control_id()}'>${this.properties.value}</span>)</label>
				
				<input type='range' style='width: 100%' name='${this.name}' value='${this.properties.value}' id='${this.control_id()}' min='${this.properties.min}' max='${this.properties.max}'>
			</div>`);

		//this.jquery().on('input', function () {$(this).trigger('change');});
		var self = this;
		this.jquery().change(function(){ 
			$( "#value"+self.control_id() ).html( $(this).val() ); 
			self.basewidget.fire_event( self.name, 'update_control_event' );
		});
		if(this.properties.required) this.set_required();
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

	////////////////////////////////////////////////////////////////////////////////
}
