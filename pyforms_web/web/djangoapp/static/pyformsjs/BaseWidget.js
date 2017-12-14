class BaseWidget{

	constructor(widget_id, widget_name, controls, parent_id, data){
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
	}


	////////////////////////////////////////////////////////////

	refresh_timeout_event(){
		this.fire_event('self', 'refresh_event');
	}

	////////////////////////////////////////////////////////////

	parent_widget(){
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

	find_control(name){
		for(var index = 0; index < this.controls.length; index++)
			if(this.controls[index].name==name)
				return this.controls[index];
		
		return undefined;
	}

	////////////////////////////////////////////////////////////

	control_id(name){
		return this.widget_id+'-'+name;
	}

	////////////////////////////////////////////////////////////

	current_folder(){
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

	fire_event(dom_in, event, show_loading){

		var data = {event: {control:dom_in, event: event}, userpath: this.current_folder() };
		this.events_queue.push(data)

		if(this.parent_id===undefined)
			pyforms.query_server(this, this.events_queue.pop(0), show_loading );
		else{
			pyforms.query_server(this, undefined, show_loading);
		};
	}

	////////////////////////////////////////////////////////////

	update_controls(){		
		pyforms.query_server(this, { userpath: this.current_folder() }); 
	}

	////////////////////////////////////////////////////////////

	deserialize(data){
		var js_code2excute = data['js-code'];
		if(js_code2excute && js_code2excute.length>0)
			for(var i=0; i<js_code2excute.length; i++)
				eval(js_code2excute[i]);

		
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
	}
	////////////////////////////////////////////////////////////

	serialize(){
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
	}
	////////////////////////////////////////////////////////////

	serialize_data(data){
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
	}

	////////////////////////////////////////////////////////////

	activate_load_event(){
		if(this.loading_counter<=0){
			this.jquery().removeClass('loading');
			return false; //exit the checker
		}

		if(this.loading_begin!=undefined && (Date.now()-this.loading_begin)>PYFORMS_CHECKER_LOOP_INTERVAL && !this.jquery().hasClass('loading') )
			this.jquery().addClass('loading')

		return true; 
	}

	loading(){
		//$("#app-"+this.widget_id).addClass('loading');
		if(this.loading_begin==undefined) this.loading_begin = Date.now();
		this.loading_counter++;
		if(this.loading_counter==1){
			var self = this;
			pyforms.register_checkloop( function(){return self.activate_load_event()} );		
		}
	}

	////////////////////////////////////////////////////////////

	not_loading(){
		//$("#app-"+this.widget_id).removeClass('loading');

		this.loading_counter--;
		pyforms.checker_loop();
	}

	////////////////////////////////////////////////////////////

	close_sub_apps(){

		for (var index = 0; index <  this.controls.length; index++) {
			if( this.controls[index].properties.child_widget_id!==undefined )
				pyforms.remove_app(this.controls[index].properties.child_widget_id);
		};
	}

	////////////////////////////////////////////////////////////

	query_server(params){
		pyforms.query_server(this, params); 
	}


	////////////////////////////////////////////////////////////

	jquery(){
		return $("#app-"+this.widget_id);
	}

	////////////////////////////////////////////////////////////

	close(){
		clearTimeout(this.timeout_loop);
		this.close_sub_apps();
		this.jquery().remove();
	}

}