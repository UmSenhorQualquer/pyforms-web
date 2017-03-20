

function ControlPassword(name, properties){
	ControlBase.call(this, name, properties);
};
ControlPassword.prototype = Object.create(ControlBase.prototype);


////////////////////////////////////////////////////////////////////////////////

ControlPassword.prototype.init_control = function(){
	var html = "<div id='"+this.place_id()+"' class='field ControlPassword' ><label>"+this.properties.label+"</label><input placeholder='"+this.properties.label+"' type='password' name='"+this.name+"' id='"+this.control_id()+"' /></div>";
	this.jquery_place().replaceWith(html);

	var self = this;
	this.jquery().change(function(){
		self.basewidget.fire_event( this.name, 'changed_event' );
	});

	if(!this.properties.visible) this.hide();

	if(!this.properties.enabled){
		this.jquery().attr('disabled', '');
	}else{
		this.jquery().removeAttr('disabled');
	};

	
	if(this.properties.error) this.jquery_place().addClass('error'); else this.jquery_place().removeClass('error'); 
};

////////////////////////////////////////////////////////////////////////////////
