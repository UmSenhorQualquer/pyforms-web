class ControlTemplate extends ControlBase{

	////////////////////////////////////////////////////////////////////////////////

	init_control(){
		var html = "<div id='"+this.place_id()+"' class='field control ControlTemplate' ><div id='"+this.control_id()+"' ></div></div>";
		this.jquery_place().replaceWith(html);

		this.set_value(this.properties.value);
	};

	////////////////////////////////////////////////////////////////////////////////


	set_value(value){
		var html = Base64.decode(value);

		if(html){
			this.jquery().html(html);
			this.set_actions();
		}
		else
			this.jquery().html(''); 
	};

	////////////////////////////////////////////////////////////////////////////////

	set_actions(){
		this.properties.action_param = undefined;
		var self = this;
		
		this.jquery().find('[action]').click(function(){
			var action 					 = $(this).attr('action');
			var action_param 			 = $(this).attr('action-param');
			self.properties.action_param = action_param;
			self.basewidget.fire_event( 'self', action );
		});
	};


	update_server(){
		return this.properties.action_param != undefined;
	};

}