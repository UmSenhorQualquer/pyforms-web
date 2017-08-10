

function BaseWidget(widget_id, widget_name, controls, parent_id, data){
	this.name 		= widget_name;
	this.widget_id 	= widget_id;
	this.controls 	= controls;
	this.events_queue = [];
	this.parent_id  = parent_id;

	// variables used to verify if the loading layer needs to be shown or not
	this.loading_begin 	 = undefined;
	this.loading_counter = 0;

	for(var index = 0; index < controls.length; index++){
		controls[index].basewidget = this;
		controls[index].init_control();
	};


	if(data.messages!=undefined)
		for (var i=0; i<data.messages.length; i++){
			var msg = data.messages[i]; 
			if(msg.type!='') this.jquery().addClass(msg.type);

			var html = '<div class="ui '+msg.type+' message">';
			html 	+= '<i class="close icon"></i>';
			if(msg.title)  html += '<div class="header">'+msg.title+'</div>';	
			if(msg.messages.length==1)	
				html 	+= '<p>'+msg.messages[0]+'</p>';
			else{
				html 	+= '<ul class="list">';
				for(var i=0; i<msg.messages.length; i++) html += '<li>'+msg.messages[i]+'</li>';
				html 	+= '</ul>';
			};
			$(html).prependTo(this.jquery()).find('.close').on('click', function(){
				$(this).closest('.message').transition({animation:'fade',onComplete:function(){$(this).remove();} });
			});
		};

	//add auto refresh
	if(data.refresh_timeout){
		var self = this;
		this.timeout_loop = setInterval(function(){ self.refresh_timeout_event(); }, data.refresh_timeout);
	};
};
////////////////////////////////////////////////////////////

BaseWidget.prototype.refresh_timeout_event = function(){
	this.fire_event('self', 'refresh_event');
};

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
};

////////////////////////////////////////////////////////////

BaseWidget.prototype.find_control = function(name){
	for(var index = 0; index < this.controls.length; index++)
		if(this.controls[index].name==name)
			return this.controls[index];
	
	return undefined;
};

////////////////////////////////////////////////////////////

BaseWidget.prototype.control_id = function(name){
	return this.widget_id+'-'+name;
};

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
};

////////////////////////////////////////////////////////////

BaseWidget.prototype.fire_event = function(dom_in, event, show_loading){

	var data = {event: {control:dom_in, event: event}, userpath: this.current_folder() };
	this.events_queue.push(data)

	if(this.parent_id===undefined)
		pyforms.query_server(this, this.events_queue.pop(0), show_loading );
	else{
		pyforms.query_server(this, undefined, show_loading);
	};
};

////////////////////////////////////////////////////////////

BaseWidget.prototype.update_controls = function(){		
	pyforms.query_server(this, { userpath: this.current_folder() }); 
};

////////////////////////////////////////////////////////////

BaseWidget.prototype.deserialize = function(data){
	for (var index = 0; index < this.controls.length; index++) {
		var name 		= this.controls[index].name;
		if(data[name])  this.controls[index].deserialize( data[name] );
	};
	this.children_windows = data['children-windows']



	if(data.messages!=undefined)
		for (var i=0; i<data.messages.length; i++){
			var msg = data.messages[i]; 
			if(msg.type!='') this.jquery().addClass(msg.type);

			var html = '<div class="ui '+msg.type+' message">';
			html 	+= '<i class="close icon"></i>';
			if(msg.title)  html += '<div class="header">'+msg.title+'</div>';	
			if(msg.messages.length==1)	
				html 	+= '<p>'+msg.messages[0]+'</p>';
			else{
				html 	+= '<ul class="list">';
				for(var i=0; i<msg.messages.length; i++) html += '<li>'+msg.messages[i]+'</li>';
				html 	+= '</ul>';
			};
			$(html).prependTo(this.jquery()).find('.close').on('click', function(){
				$(this).closest('.message').transition({animation:'fade',onComplete:function(){$(this).remove();} });
			});
		};
	

	if(data['close_widget']){ 
		pyforms.remove_app(data['uid']);
		pyforms.close_layout_place(data['layout_position']);
	}
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
		var control = this.controls[index];
		if( control.update_server() ){
			var name 	= control.name;
			data[name] 	= control.serialize();
		};
	};
	data['uid'] 			 = this.widget_id;
	data['children-windows'] = this.children_windows;	
	return data;
};

////////////////////////////////////////////////////////////

BaseWidget.prototype.activate_load_event = function(){
	if(this.loading_counter<=0){
		this.jquery().removeClass('loading');
		return false; //exit the checker
	}

	if(this.loading_begin!=undefined && (Date.now()-this.loading_begin)>PYFORMS_CHECKER_LOOP_INTERVAL && !this.jquery().hasClass('loading') )
		this.jquery().addClass('loading')

	return true; 
};

BaseWidget.prototype.loading = function(){
	//$("#app-"+this.widget_id).addClass('loading');
	if(this.loading_begin==undefined) this.loading_begin = Date.now();
	this.loading_counter++;
	if(this.loading_counter==1){
		var self = this;
		pyforms.register_checkloop( function(){return self.activate_load_event()} );		
	}
};

////////////////////////////////////////////////////////////

BaseWidget.prototype.not_loading = function(){
	//$("#app-"+this.widget_id).removeClass('loading');

	this.loading_counter--;
	pyforms.checker_loop();
};

////////////////////////////////////////////////////////////

BaseWidget.prototype.close_sub_apps = function(){

	for (var index = 0; index <  this.controls.length; index++) {
		if( this.controls[index].properties.child_widget_id!==undefined )
			pyforms.remove_app(this.controls[index].properties.child_widget_id);
	};
};

////////////////////////////////////////////////////////////

BaseWidget.prototype.query_server = function(params){
	pyforms.query_server(this, params); 
};


////////////////////////////////////////////////////////////

BaseWidget.prototype.jquery = function(){
	return $("#app-"+this.widget_id);
};

////////////////////////////////////////////////////////////

BaseWidget.prototype.close = function(){
	clearTimeout(this.timeout_loop);
	this.close_sub_apps();
	this.jquery().remove();
};