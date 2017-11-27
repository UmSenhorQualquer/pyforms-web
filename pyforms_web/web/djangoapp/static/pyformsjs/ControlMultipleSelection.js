

function ControlMultipleSelection(name, properties){
	ControlBase.call(this, name, properties);
};
ControlMultipleSelection.prototype = Object.create(ControlBase.prototype);

////////////////////////////////////////////////////////////////////////////////

ControlMultipleSelection.prototype.set_value = function(value){
	//if(value) value = value.join();
	this.flag_exec_on_change_event = false;
	//this.jquery().dropdown('clear');
	this.jquery().dropdown('set exactly', value);
	this.flag_exec_on_change_event = true;
};

////////////////////////////////////////////////////////////////////////////////

ControlMultipleSelection.prototype.get_value = function(){ 
	var values = this.jquery().dropdown('get value');
	if(values.length==0) return [];
	var values = values.split(",").sort();
	return values;
};


////////////////////////////////////////////////////////////////////////////////

ControlMultipleSelection.prototype.init_control = function(){
	var html = "<div class='field ControlMultipleSelection' id='"+this.place_id()+"' >";
	if(this.properties.include_label) html += "<label for='"+this.control_id()+"'>"+this.properties.label+"</label>";
	
	switch(this.properties.mode) {
	    case 'scrolling':
	        html += "<div class='ui dropdown multiple scrolling' id='"+this.control_id()+"'>"
	        html += '<div class="default text">'+this.properties.label+'</div>';
	        html += '<i class="dropdown icon"></i>';
	        html += '<div class="menu"></div>';
			html += '</div>';
	        break;
	    default:
	        html += "<div class='ui search dropdown multiple selection' id='"+this.control_id()+"'>";
	        html += '<i class="dropdown icon"></i>';
			html += '<div class="default text">'+this.properties.label+'</div>';
			html += '</div>';
	};

	this.jquery_place().replaceWith(html);	

	var self = this;
	this.jquery_place().replaceWith(html);
	this.jquery().dropdown({forceSelection:false, allowReselection:false, hideAdditions:true});
	this.jquery().dropdown('setup menu', { values: this.properties.items });
	this.set_value(this.properties.value);

	this.jquery().dropdown('setting', 'onChange', function(){
		if(self.flag_exec_on_change_event)
			self.basewidget.fire_event( self.name, 'changed_event' );
	});

	if(!this.properties.enabled){
		$("#"+this.place_id()+' .ui.dropdown').addClass('disabled');
	}else{
		$("#"+this.place_id()+' .ui.dropdown').removeClass('disabled');
	};

	if(!this.properties.visible) this.hide();
	if(this.properties.error) this.jquery_place().addClass('error'); else this.jquery_place().removeClass('error'); 
};

////////////////////////////////////////////////////////////////////////////////

ControlMultipleSelection.prototype.deserialize = function(data){
	var previous_value = this.properties.value;
	this.properties = $.extend(this.properties, data);
	
	if(this.properties.update_items)
		this.jquery().dropdown('setup menu', { values: this.properties.items });
	
	if(this.properties.value==null)
		this.set_value(null);
	else
		if(previous_value.toString()!=this.properties.value.toString()){
			this.set_value(this.properties.value);
		}

	if(!this.properties.enabled){
		$('#'+this.place_id()+' .ui.dropdown').addClass("disabled")
	}else{
		$('#'+this.place_id()+' .ui.dropdown').removeClass("disabled")
	};

	if(!this.properties.visible) this.hide();
	else this.show();
	if(this.properties.error) this.jquery_place().addClass('error'); else this.jquery_place().removeClass('error'); 
};

////////////////////////////////////////////////////////////////////////////////
