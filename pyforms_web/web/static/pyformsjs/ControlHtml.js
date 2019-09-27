class ControlHtml extends ControlBase{

	////////////////////////////////////////////////////////////////////////////////

	init_control(){
		var html = '<div id="'+this.place_id()+'" class="field control ControlHtml">'
		if(this.properties.label_visible) html += '<label for=\'"+this.control_id()+"\'>'+this.properties.label+'</label>';
		html += '<div id="'+this.control_id()+'"></div>';
		html += "</div>";

		this.jquery_place().replaceWith(html);

		if(this.properties.value)
			this.jquery().html(this.properties.value); 
		else
			this.jquery().html(''); 

		if(this.properties.required) this.set_required();

	};

	////////////////////////////////////////////////////////////////////////////////

	set_value(value){
		if(this.properties.value)
			this.jquery().html(this.properties.value); 
		else
			this.jquery().html(''); 
	};

}

