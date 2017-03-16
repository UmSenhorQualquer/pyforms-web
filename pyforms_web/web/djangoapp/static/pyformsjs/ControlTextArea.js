

function ControlTextArea(name, properties){
	ControlBase.call(this, name, properties);
};
ControlTextArea.prototype = Object.create(ControlBase.prototype);


////////////////////////////////////////////////////////////////////////////////

ControlTextArea.prototype.init_control = function(){
	var html = "<div id='"+this.place_id()+"' class='field ControlTextArea' ><label>"+this.properties.label+"</label><textarea placeholder='"+this.properties.label+"' type='text' name='"+this.name+"' id='"+this.control_id()+"' >"+this.properties.value+"</textarea></div>";
	this.jquery_place().replaceWith(html);

	var self = this;
	this.jquery().change(function(){
		self.basewidget.fire_event( this.name, 'changed_event' );
	});

	if(!this.properties.enabled){
		this.jquery().attr('disabled', '');
	}else{
		this.jquery().removeAttr('disabled');
	};	

	if(!this.properties.visible) this.hide();
	if(this.properties.error) this.jquery_place().addClass('error'); else this.jquery_place().removeClass('error'); 
};

////////////////////////////////////////////////////////////////////////////////
