class ControlInteger extends ControlBase{

	////////////////////////////////////////////////////////////////////////////////

	init_control(){
		var html = "<div id='"+this.place_id()+"' class='field control ControlInteger' ><label>"+this.properties.label+"</label><input placeholder='"+this.properties.label+"' type='text' name='"+this.name+"' id='"+this.control_id()+"' /></div>";
		this.jquery_place().replaceWith(html);
		this.set_value(this.properties.value);

		var self = this;
		this.jquery().change(function(){
			self.basewidget.fire_event( this.name, 'update_control_event' );
		});

		if(this.properties.error) this.jquery_place().addClass('error'); else this.jquery_place().removeClass('error'); 
	};

	////////////////////////////////////////////////////////////////////////////////


	get_value(){ 
		if(this.jquery().length==0) return this.properties.value;
		var value = this.jquery().val();
		if(value=='null' || value=='') return null;
		else return value;
	};


	////////////////////////////////////////////////////////////////////////////////

}

