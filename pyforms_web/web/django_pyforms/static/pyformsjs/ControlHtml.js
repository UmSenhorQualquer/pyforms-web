class ControlHtml extends ControlBase{

	////////////////////////////////////////////////////////////////////////////////

	init_control(){
		var html = "<div id='"+this.place_id()+"' class='field ControlHtml' ><label>"+this.properties.label+"</label><div class='ui segment' id='"+this.control_id()+"' ></div></div>";
		this.jquery_place().replaceWith(html);

		if(this.properties.value)
			this.jquery().html(this.properties.value); 
		else
			this.jquery().html(''); 
		
		if(!this.properties.visible) this.hide();

		if(!this.properties.enabled){
			this.jquery().attr('disabled', '');
		}else{
			this.jquery().removeAttr('disabled');
		};
	};

	////////////////////////////////////////////////////////////////////////////////

	set_value(value){
		if(this.properties.value)
			this.jquery().html(this.properties.value); 
		else
			this.jquery().html(''); 
	};

}

