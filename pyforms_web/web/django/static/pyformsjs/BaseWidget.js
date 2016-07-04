

function BaseWidget(widget_id, widget_name, controls, parent_id){
	this.name 		= widget_name;
	this.widget_id 	= widget_id;
	this.controls 	= controls;
	this.events_queue = [];
	this.parent_id  = parent_id;

	for(var index = 0; index < controls.length; index++){
		controls[index].basewidget = this;
		controls[index].init_control();
	};
	//$('.application-tabs').tabs()
}

////////////////////////////////////////////////////////////

BaseWidget.prototype.parent_widget = function(){
	//if(this.parent!==undefined) return this.parent;
	if(this.parent_id!==undefined){
		var parent = pyforms.find_app(this.parent_id);
		//if(parent!==undefined) this.parent = parent;
		return parent;
	}
	else 
		return undefined;
}

////////////////////////////////////////////////////////////

BaseWidget.prototype.find_control = function(name){
	for(var index = 0; index < this.controls.length; index++)
		if(this.controls[index].name==name)
			return this.controls[index];
	
	return undefined;
}

////////////////////////////////////////////////////////////

BaseWidget.prototype.control_id = function(name){
	return this.widget_id+'-'+name;
}

////////////////////////////////////////////////////////////

BaseWidget.prototype.current_folder = function(){
	try {
    	var currentfolder = $('#files-browser-div').dataviewer('path');
		if(currentfolder==undefined) currentfolder = '/';
	}
	catch(err) {
	    currentfolder = '/';
	}	
	return currentfolder;
}

////////////////////////////////////////////////////////////

BaseWidget.prototype.fire_event = function(dom_in, event){
	
	var data = {event: {control:dom_in, event: event}, userpath: this.current_folder() };
	this.events_queue.push(data)

	if(this.parent_id===undefined)
		this.update_data( this.events_queue.pop(0) );
	else{
		this.update_data();
	}
}

////////////////////////////////////////////////////////////

BaseWidget.prototype.update_controls = function(){		
	this.update_data({ userpath: this.current_folder() }); 
};

////////////////////////////////////////////////////////////

BaseWidget.prototype.deserialize = function(data){
	for (var index = 0; index < this.controls.length; index++) {
		var name 		= this.controls[index].name;
		if(data[name])  this.controls[index].deserialize( data[name] );
	};
};
////////////////////////////////////////////////////////////

BaseWidget.prototype.serialize = function(){
	var data = undefined;
	if(this.events_queue.length>0)
		data = this.events_queue.pop(0)
	else
		data = { userpath: this.current_folder() };
	
	
	for (var index = 0; index <  this.controls.length; index++) {
		var name 	= this.controls[index].name;
		data[name] 	= this.controls[index].serialize();
	};
	return data;
};
////////////////////////////////////////////////////////////

BaseWidget.prototype.serialize_data = function(data){
	for (var index = 0; index <  this.controls.length; index++) {
		var name 	= this.controls[index].name;
		data[name] 	= this.controls[index].serialize();
	};
	return data;
};

////////////////////////////////////////////////////////////

BaseWidget.prototype.loading = function(){
	$("#app-"+this.widget_id).addClass('loading');
};

////////////////////////////////////////////////////////////

BaseWidget.prototype.not_loading = function(){
	$("#app-"+this.widget_id).removeClass('loading');
};

////////////////////////////////////////////////////////////

BaseWidget.prototype.update_data = function(data2send){	
	if(data2send===undefined) data2send = {};

	if(this.parent_id!==undefined){
		var parent_widget = this.parent_widget();
		parent_widget.update_data(data2send);
	}else{
		
		this.loading();
		data2send = this.serialize_data(data2send);
		var self 	= this;
		var jsondata =  $.toJSON(data2send);
		$.ajax({
			method: 'post',
			cache: false,
			dataType: "json",
			url: '/pyforms/update/'+this.name+'/?nocache='+$.now(),
			data: jsondata,
			contentType: "application/json; charset=utf-8",
			success: function(res){
				if( res.result=='error' )
					error(res.msg);
				else
					self.deserialize(res);
			}
		}).fail(function(xhr){
			error(xhr.status+" "+xhr.statusText+": "+xhr.responseText);
		}).always(function(){
			self.not_loading();
		});

		if(  this.events_queue.length>0 )  this.update_data(  this.events_queue.pop(0) );
	}
}

////////////////////////////////////////////////////////////

BaseWidget.prototype.update_controls = function(){	
	this.update_data({ userpath: this.current_folder() }); 
};

////////////////////////////////////////////////////////////

BaseWidget.prototype.close_sub_apps = function(){

	for (var index = 0; index <  this.controls.length; index++) {
		if( this.controls[index].properties.child_widget_id!==undefined )
			pyforms.remove_app(this.controls[index].properties.child_widget_id);
	};
};


////////////////////////////////////////////////////////////

BaseWidget.prototype.close = function(){
	this.close_sub_apps();
	$("#app-"+this.widget_id).remove();
};