class ControlImage extends ControlBase{


	////////////////////////////////////////////////////////////////////////////////

	get_value(){ 
		return this.jquery().attr('src');
	};

	////////////////////////////////////////////////////////////////////////////////

	set_value(value){
		if(value.base64){
			this.jquery().attr("src", "data:image/png;base64,"+value.base64);
		}else{
			this.jquery().attr("src", value.url);
		}

		var width = this.jquery().width();
		this.jquery().css('width', width+"px");
	};

	////////////////////////////////////////////////////////////////////////////////

	init_control(){
		var html = "<div id='"+this.place_id()+"' class='field control ControlImage' >";
		html += "<div class='ui card' id='card"+this.control_id()+"' >";
		html += "<div class='image'>";
		html += "<img style='width:100%;' class='image' src='' id='"+this.control_id()+"' />";
		html += "</div>";
		html += "</div>";
		html += "</div>";
		this.jquery_place().replaceWith(html);
		if(this.properties.required) this.set_required();
	};

	////////////////////////////////////////////////////////////////////////////////


}
