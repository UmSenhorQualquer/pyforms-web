class ControlFloat extends ControlBase{

	
	init_control(){
		var html = "<div id='"+this.place_id()+"' class='field control ControlFloat' ><label>"+this.properties.label+"</label><input placeholder='"+this.properties.label+"' type='text' name='"+this.name+"' id='"+this.control_id()+"' value=\""+this.properties.value+"\" /></div>";
		this.jquery_place().replaceWith(html);

		var self = this;
		this.jquery().change(function(){
			self.basewidget.fire_event( this.name, 'update_control_event' );
		});

		
		if(this.properties.error) this.jquery_place().addClass('error'); else this.jquery_place().removeClass('error'); 
	};

	////////////////////////////////////////////////////////////////////////////////

}

