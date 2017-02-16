

function ControlBoundingSlider(name, properties){
	ControlBase.call(this, name, properties);
};
ControlBoundingSlider.prototype = Object.create(ControlBase.prototype);

////////////////////////////////////////////////////////////////////////////////

ControlBoundingSlider.prototype.set_value = function(value){
	this.jquery().slider({values:val})
	$("#value-"+this.control_id() ).html( val );
};

////////////////////////////////////////////////////////////////////////////////

ControlBoundingSlider.prototype.get_value = function(){
	return { value: this.jquery().slider("values"), max: this.properties.max, min: this.properties.min }
};

////////////////////////////////////////////////////////////////////////////////

ControlBoundingSlider.prototype.init_control = function(){
	var html =	"<div class='ControlSlider' id='"+this.place_id()+"' title='"+this.properties.help+"'   >";
	html +=		"<label style='margin-right: 20px;' for='"+this.control_id()+"'>"+this.properties.label+": <small id='value-"+this.control_id()+"' style='color:red' >"+this.properties.value+"</small></label>";
	html += 	"<div class='slider' name='"+this.name+"' id='"+this.control_id()+"' ></div>";
	html += 	"</div>";
	this.jquery_place().replaceWith(html);

	var self = this;
	this.jquery().slider({ 
		range: true,
		slide: function( event, ui ) { $( "#value-"+self.control_id() ).html( ui.value ); },
		stop:  function(){ self.basewidget.fire_event( self.name, 'changed_event' )}, 
		min: this.properties.min, max: this.properties.max, values: this.properties.value 
	});

	if(!this.properties.visible) this.hide();
	
};

////////////////////////////////////////////////////////////////////////////////

