var COLUMNS_CSS_CLASSES = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve'];

function ControlBase(name, properties){
	var self = this;


	this.name 			= name;
	this.properties 	= properties;
	this.basewidget 	= undefined; //Will be set in runtime by the parent BaseWidget object.
};

////////////////////////////////////////////////////////////////////////////////

ControlBase.prototype.app_id = function(){ 
	return this.basewidget.widget_id; 
};

////////////////////////////////////////////////////////////////////////////////

ControlBase.prototype.control_id = function(){ 
	return this.basewidget.control_id(this.name); 
};

////////////////////////////////////////////////////////////////////////////////

ControlBase.prototype.jquery = function(){ 
	return $("#"+this.control_id()); 
};

////////////////////////////////////////////////////////////////////////////////

ControlBase.prototype.place_id = function(){ 
	return "place-"+this.control_id(); 
};

////////////////////////////////////////////////////////////////////////////////

ControlBase.prototype.jquery_place = function(){ 
	return $( "#"+this.place_id() ); 
};

////////////////////////////////////////////////////////////////////////////////

ControlBase.prototype.get_value = function(){ 
	if(this.jquery().size()==0) return this.properties.value;
	return this.jquery().val(); 
};

////////////////////////////////////////////////////////////////////////////////

ControlBase.prototype.set_value = function(value){
	if(this.jquery().size()>0) this.jquery().val(value); 
};

////////////////////////////////////////////////////////////////////////////////

ControlBase.prototype.hide = function(not_update_columns){
	if( !this.jquery_place().is(':visible') ) return;
	var parent = this.jquery_place().parent();

	if( parent.hasClass('fields') ){
		var found = false;
		for(var i=2; i<COLUMNS_CSS_CLASSES.length; i++)
			if( parent.hasClass( COLUMNS_CSS_CLASSES[i] ) ){
				parent.removeClass( COLUMNS_CSS_CLASSES[i] );
				parent.addClass( COLUMNS_CSS_CLASSES[i-1] );
				
				found = true;
				break;
			};

		if(!found){
			parent.removeClass( 'fields' );
			parent.removeClass( 'two' );
		}
	}
	

	this.jquery_place().hide();
	this.properties.visible = 0;
};

////////////////////////////////////////////////////////////////////////////////

ControlBase.prototype.show = function(not_update_columns){
	if( this.jquery_place().is(':visible') ) return;
	var parent = this.jquery_place().parent();
	
	if( parent.hasClass('fields') ){
		for(var i=0; i<COLUMNS_CSS_CLASSES.length-1; i++)
			if( parent.hasClass( COLUMNS_CSS_CLASSES[i] ) ){
				parent.removeClass( COLUMNS_CSS_CLASSES[i] );
				parent.addClass( COLUMNS_CSS_CLASSES[i+1] );
				break;
			};
	}else 
	 	if( !parent.hasClass('form') && !parent.hasClass('tab') && !parent.hasClass('ControlEmptyWidget') ){
	 		parent.addClass( 'fields' );
			parent.addClass( 'two' );
	 	}
	this.jquery_place().show();
	this.properties.visible = 1;
};

////////////////////////////////////////////////////////////////////////////////

ControlBase.prototype.deserialize = function(data){
	$.extend(this.properties, data);


	this.set_value(this.properties.value);
	if(this.properties.visible) 
		this.show();
	else 
		this.hide();
};

////////////////////////////////////////////////////////////////////////////////

ControlBase.prototype.serialize = function(){
	this.properties.value = this.get_value();
	return this.properties; 
};

////////////////////////////////////////////////////////////////////////////////

ControlBase.prototype.init_control = function(){
	if(!this.properties.visible) this.hide();
};