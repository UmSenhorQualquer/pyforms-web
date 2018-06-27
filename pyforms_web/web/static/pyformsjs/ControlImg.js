class ControlImg extends ControlBase{

	////////////////////////////////////////////////////////////////////////////////
	init_control(){
		var html = "<div id='"+this.place_id()+"' class='field control ControlImg' >"
		if(this.properties.label_visible) html += "<label>"+this.properties.label+"</label>";
		html += "<span id='"+this.control_id()+"' ></span></div>";
		this.jquery_place().replaceWith(html);

		this.set_value(this.properties.value);
	};
	////////////////////////////////////////////////////////////////////////////////
		
	get_value(){ 
		return this.properties.value;
	};

	////////////////////////////////////////////////////////////////////////////////

	set_value(value){
		if(value)
			var html = '<img id="'+this.control_id()+'"" class="ui image '+this.properties.css+'" src="'+value+'">';
		else
			var html = "<span id='"+this.control_id()+"' ></span>";
		this.jquery().replaceWith(html);
	};
}