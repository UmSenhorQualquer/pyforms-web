class ControlImage extends ControlBase{


	////////////////////////////////////////////////////////////////////////////////


	get_value(){ 
		return this.jquery().attr('src');
	};

	////////////////////////////////////////////////////////////////////////////////

	set_value(value){
		if(value.image) this.jquery().attr("src", "data:image/png;base64,"+value.image);

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

		
	};

	////////////////////////////////////////////////////////////////////////////////


}
