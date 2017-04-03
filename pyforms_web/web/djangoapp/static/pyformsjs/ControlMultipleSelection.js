

function ControlMultipleSelection(name, properties){
	ControlBase.call(this, name, properties);
};
ControlMultipleSelection.prototype = Object.create(ControlBase.prototype);

////////////////////////////////////////////////////////////////////////////////

ControlMultipleSelection.prototype.set_value = function(value){
	var count = 0;
	var curr_vals = this.get_value()
	for(var i=0; i<value.length; i++)
		for(var j=0; j<curr_vals.length; j++)
			if(value[i]==curr_vals[j]){
				count++;
				break;
			};

	if(count!=value.length || count==0 || value.length==0)	
		this.jquery().dropdown('set exactly', this.properties.value);
};

////////////////////////////////////////////////////////////////////////////////

ControlMultipleSelection.prototype.get_value = function(){
	var values = this.jquery().dropdown('get value');
	values = values.slice( 0, values.length-1);
	res = [];
	for(var i=0; i<values.length; i++)
		if(values[i]!=null) res.push(values[i])
	return res;
};

////////////////////////////////////////////////////////////////////////////////

ControlMultipleSelection.prototype.init_control = function(){
	var html = "<div class='field ControlMultipleSelection' id='"+this.place_id()+"' >";
	html += "<label for='"+this.control_id()+"'>"+this.properties.label+"</label>";
	html += "<select class='ui search dropdown' id='"+this.control_id()+"' multiple='' >";
	var data = this.properties.items;
	for(var i=0; i<data.length; i++){
		html += "<option value='"+data[i].value+"'>"+data[i].label+"</label>";
	};
	html += "</select>";
	html += "</div>";

	this.jquery_place().replaceWith(html);	
	this.jquery().dropdown({forceSelection:false});

	if(!this.properties.enabled){
		$("#"+this.place_id()+' .ui.dropdown').addClass('disabled');
	}else{
		$("#"+this.place_id()+' .ui.dropdown').removeClass('disabled');
	};

	if(!this.properties.visible) this.hide();
	this.set_value(this.properties.value);
	if(this.properties.error) this.jquery_place().addClass('error'); else this.jquery_place().removeClass('error'); 
};

////////////////////////////////////////////////////////////////////////////////


