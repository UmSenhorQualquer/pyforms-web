class ControlText extends ControlBase{

	////////////////////////////////////////////////////////////////////////////////
	init_control(){
		var html = "<div id='"+this.place_id()+"' class='field control ControlText' >"
		if(this.properties.label_visible) html += "<label>"+this.properties.label+"</label>";
		html += "<input placeholder='"+this.properties.label+"' type='text' name='"+this.name+"' id='"+this.control_id()+"' value='' />";
		html += "</div>";
		this.jquery_place().replaceWith(html);

		this.set_value(this.properties.value);

		var self = this;
		this.jquery().change(function(){
			self.basewidget.fire_event( this.name, 'update_control_event' );
		});

		if(this.properties.error) this.jquery_place().addClass('error'); else this.jquery_place().removeClass('error'); 

		
	};
	////////////////////////////////////////////////////////////////////////////////
		
}