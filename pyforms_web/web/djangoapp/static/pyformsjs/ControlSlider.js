class ControlSlider extends ControlBase{

	
	////////////////////////////////////////////////////////////////////////////////

	get_value(){ 
		return this.jquery().val();
	};

	////////////////////////////////////////////////////////////////////////////////

	set_value(value){
		this.jquery().val(value);
		$( "#value"+this.name ).html( value );
	};

	////////////////////////////////////////////////////////////////////////////////

	init_control(){
		var html = 	"<div id='"+this.place_id()+"' class='field ControlSlider' title='"+this.properties.help+"' >";
		html += 	"<label>"+this.properties.label;
		html += 	" <div id='value"+this.control_id()+"' class='ui basic label'>"+this.properties.value+"</div>";
		html += 	"</label>";
		html += 	"<input style='width:100%;' type='range' name='"+this.name+"' value='"+this.properties.value+"' id='"+this.control_id()+"' min='"+this.properties.min+"' max='"+this.properties.max+"'>";
		html += 	"</div>";

		this.jquery_place().replaceWith(html);
		//this.jquery().on('input', function () {$(this).trigger('change');});
		var self = this;
		this.jquery().change(function(){ 
			$( "#value"+self.control_id() ).html( $(this).val() ); 
			self.basewidget.fire_event( self.name, 'changed_event' );
		});

		if(!this.properties.visible) this.hide();
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
