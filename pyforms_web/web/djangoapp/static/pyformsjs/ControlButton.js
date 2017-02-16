

function ControlButton(name, properties){
	ControlBase.call(this, name, properties);
};
ControlButton.prototype = Object.create(ControlBase.prototype);


////////////////////////////////////////////////////////////////////////////////

ControlButton.prototype.init_control = function(){

	var html = "<div class='field ControlButton' id='"+this.place_id()+"' ><label>&nbsp;</label>";
	html +="<button type='button' title='"+this.properties.help+"' id='"+this.control_id()+"' class='ui button' >";
	html += this.properties.label;
	html += '</button>';
	html += '</div>';
	
	this.jquery_place().replaceWith(html);

	var self = this;
	this.jquery().click(function(){
		if( self.properties.value.length>0 )
			eval(self.properties.value);
		else
			self.basewidget.fire_event( self.name, 'pressed' );
	});

	if(!this.properties.visible) this.hide();
	if(this.properties.css) this.jquery().addClass(this.properties.css);

};

////////////////////////////////////////////////////////////////////////////////

ControlButton.prototype.get_value = function(){ 
	return this.properties.value;
};

////////////////////////////////////////////////////////////////////////////////

ControlButton.prototype.update_server = function(){
	return false;
};