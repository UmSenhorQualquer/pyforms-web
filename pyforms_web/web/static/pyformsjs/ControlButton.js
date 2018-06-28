class ControlButton extends ControlBase{


	////////////////////////////////////////////////////////////////////////////////

	init_control(){
		var html = "<div class='field control ControlButton' id='"+this.place_id()+"'>";
		if(this.properties.label_visible) html += '<label>&nbsp;</label>';
		html +=(!this.properties.labeled)?"<button type='button'":"<div ";
		html +=" title='"+this.properties.help+"' id='"+this.control_id()+"' class='ui button' >";
		html += this.properties.label;
		html +=(!this.properties.labeled)?"</button>":"</div>";
		html += '</div>';
		
		this.jquery_place().replaceWith(html);

		var self = this;
		this.jquery().click(function(){
			if( self.properties.value )
				eval(self.properties.value);
			else
				self.basewidget.fire_event( self.name, 'pressed' );
		});

	};

	////////////////////////////////////////////////////////////////////////////////

	get_value(){ 
		return this.properties.value;
	};


	////////////////////////////////////////////////////////////////////////////////

	update_server(){
		return false;
	};


	deserialize(data){
		$.extend(this.properties, data);
		this.set_value(this.properties.value);

		this.jquery().html(this.properties.label);
		
		if(this.properties.error) this.jquery_place().addClass('error'); else this.jquery_place().removeClass('error');
	};

}