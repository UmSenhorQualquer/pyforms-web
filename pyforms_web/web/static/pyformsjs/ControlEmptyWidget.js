class ControlEmptyWidget extends ControlBase{


	////////////////////////////////////////////////////////////////////////////////

	init_control(){
		var widget_html = '';
		if( this.properties.html!==undefined ) widget_html = Base64.decode(this.properties.html);

		
		var html = "<div id='"+this.place_id()+"' class='field control ControlEmptyWidget "+this.properties.css+"' >"+widget_html+"</div>";
		this.jquery_place().replaceWith(html);
		
		if(this.properties.child_widget_id!==undefined){
			var child_app = pyforms.find_app(this.properties.child_widget_id);
			child_app.deserialize(this.properties.widget_data);
		}
		
		this.set_value(this.properties.value);

		
	};

	////////////////////////////////////////////////////////////

	serialize(){
		if(this.properties.child_widget_id===undefined) return this.properties;

		var child_app = pyforms.find_app(this.properties.child_widget_id);
		this.properties['widget_data'] = child_app.serialize();
		
		if( child_app.events_queue.length>0 ) this.properties['widget_data']['event'] = child_app.events_queue.pop(0);

		return this.properties;
	};

	////////////////////////////////////////////////////////////////////////////////

	deserialize(data){
		
		if(data.clear_widget==1){
			pyforms.remove_app( this.properties.child_widget_id );
			this.jquery_place().html('');
			if( data.child_widget_id===undefined ) delete this.properties.child_widget_id;
			delete this.properties.clear_widget;
			delete data.clear_widget;
		}

		if( data.html!==undefined ){
			this.jquery_place().html( Base64.decode(data.html) );
			delete data.html;
		}

		

		$.extend(this.properties, data);

		
		if(this.properties.child_widget_id!==undefined){
			var child_app = pyforms.find_app(this.properties.child_widget_id);
			child_app.deserialize(this.properties.widget_data);
		}
		
		this.set_value(this.properties.value);

	};


	update_server(){
		return true;
	};
	
}
