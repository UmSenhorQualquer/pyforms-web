

function ControlDateTime(name, properties){
	ControlBase.call(this, name, properties);
};
ControlDateTime.prototype = Object.create(ControlBase.prototype);

////////////////////////////////////////////////////////////////////////////////

ControlDateTime.prototype.init_control = function(){
	var html = "<div id='"+this.place_id()+"' class='field ControlDateTime' ><label>"+this.properties.label+"</label><input placeholder='"+this.properties.label+"' type='text' name='"+this.name+"' id='"+this.control_id()+"' value=\""+this.properties.value+"\" /></div>";
	this.jquery_place().replaceWith(html);

	this.jquery().datetimepicker({
		format:'Y-m-d H:i',
		formatTime:'H:i',
		formatDate:'Y-m-d'
	});

	var self = this;
	this.jquery().on("change", function(){
		self.basewidget.fire_event( self.name, 'changed_event' );
	});

	if(!this.properties.visible) this.hide();
	if(this.properties.error) this.jquery_place().addClass('error'); else this.jquery_place().removeClass('error'); 
};

////////////////////////////////////////////////////////////////////////////////