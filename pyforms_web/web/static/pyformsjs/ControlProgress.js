class ControlProgress extends ControlBase{

	init_control(){
		this.jquery_place().replaceWith("<div title='"+this.properties.help+"' id='"+this.control_id()+"' class='progressbar control' ></div>");
	};
}