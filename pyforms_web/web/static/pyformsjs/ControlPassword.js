class ControlPassword extends ControlBase{



	////////////////////////////////////////////////////////////////////////////////

	init_control(){
		var html = "<div id='"+this.place_id()+"' class='field control ControlPassword' ><label>"+this.properties.label+"</label><input placeholder='"+this.properties.label+"' type='password' name='"+this.name+"' id='"+this.control_id()+"' /></div>";
		this.jquery_place().replaceWith(html);

		var self = this;
		this.jquery().change(function(){
			self.basewidget.fire_event( this.name, 'update_control_event' );
		});


		
		if(this.properties.error) this.jquery_place().addClass('error'); else this.jquery_place().removeClass('error'); 
	};

	////////////////////////////////////////////////////////////////////////////////

}