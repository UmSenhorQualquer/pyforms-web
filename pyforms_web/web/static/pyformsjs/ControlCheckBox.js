class ControlCheckBox extends ControlBase{

	set_value(value){
		if(value)
			this.jquery().prop('checked', true);
		else
			this.jquery().prop('checked', false);

	};

	////////////////////////////////////////////////////////////////////////////////

	get_value(){
		if(this.jquery().length==0) return this.properties.value;
		return this.jquery().is(':checked');
	};

	////////////////////////////////////////////////////////////////////////////////

	init_control(){
		var html = "<div class='field control ControlCheckBox' id='"+this.place_id()+"' >";
		if(this.properties.label_visible)
			html += "<div style='height: 31px' ></div>";
		else
			html += "<div style='height: 3px' ></div>";
		html += "<div class='ui toggle checkbox' title='"+this.properties.help+"' >";
		html += "<input name='"+this.name+"' id='"+this.control_id()+"' type='checkbox' value='true' class='hidden' />";
		html += "<label for='"+this.control_id()+"'>"+this.properties.label+"</label>";
		html += "</div></div>";
		this.jquery_place().replaceWith(html);
		
		if( this.properties.value)
			this.jquery().prop('checked', true);
		else
			this.jquery().prop('checked', false);

		
		var self = this;
		this.jquery().click(function(){ self.basewidget.fire_event( self.name, 'update_control_event' ); });

		if(!this.properties.visible) this.hide(undefined, true);
		if(this.properties.error) this.jquery_place().addClass('error'); else this.jquery_place().removeClass('error'); 
	};

	////////////////////////////////////////////////////////////////////////////////



}
