class ControlText extends ControlBase{

	////////////////////////////////////////////////////////////////////////////////
	init_control(){
		var html = "<div id='"+this.place_id()+"' class='field control ControlText' >"
		if(this.properties.label_visible) html += "<label for='"+this.control_id()+"'>"+this.properties.label+"</label>";
		html += "<input type='text' name='"+this.name+"' id='"+this.control_id()+"' placeholder='"+this.properties.placeholder+"' value='' />";
		html += "</div>";
		this.jquery_place().replaceWith(html);

		this.set_value(this.properties.value);

		var self = this;
		this.jquery().change(function(){
			self.basewidget.fire_event( this.name, 'update_control_event' );
		});

		this.jquery().keypress(function(e) {
        	if(e.which == 13)
				self.basewidget.fire_event( this.name, 'on_enter_event' );
		});

		if(this.properties.error) this.jquery_place().addClass('error'); else this.jquery_place().removeClass('error');
		if(this.properties.required) this.set_required();
	};
	////////////////////////////////////////////////////////////////////////////////

}
