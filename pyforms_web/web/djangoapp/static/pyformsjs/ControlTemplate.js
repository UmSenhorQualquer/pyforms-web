

function ControlTemplate(name, properties){
	ControlBase.call(this, name, properties);
};
ControlTemplate.prototype = Object.create(ControlBase.prototype);


////////////////////////////////////////////////////////////////////////////////

ControlTemplate.prototype.init_control = function(){
	var html = "<div id='"+this.place_id()+"' class='field ControlTemplate' ><div id='"+this.control_id()+"' ></div></div>";
	this.jquery_place().replaceWith(html);

	this.set_value(this.properties.value);
	
	if(!this.properties.visible) this.hide(undefined, true);

	if(!this.properties.enabled){
		this.jquery().attr('disabled', '');
	}else{
		this.jquery().removeAttr('disabled');
	};
};

////////////////////////////////////////////////////////////////////////////////


ControlTemplate.prototype.set_value = function(value){
	var html = Base64.decode(value);

	if(html){
		this.jquery().html(html); 
		this.set_actions();
	}
	else
		this.jquery().html(''); 
};

////////////////////////////////////////////////////////////////////////////////

ControlTemplate.prototype.set_actions = function(){
	this.properties.action_param = undefined;
	var self 	= this;
	
	this.jquery().find('[action]').click(function(){
		var action 					 = $(this).attr('action');
		var action_param 			 = $(this).attr('action-param');
		self.properties.action_param = action_param;
		self.basewidget.fire_event( 'self', action );
	});
};