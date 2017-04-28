
function ControlFeed(name, properties){
	ControlBase.call(this, name, properties);
};
ControlFeed.prototype = Object.create(ControlBase.prototype);

////////////////////////////////////////////////////////////////////////////////

ControlFeed.prototype.init_control = function(){
	var html = "<div id='"+this.place_id()+"' class='field'>";
	html += '<div class="ui feed ControlFeed"  id="'+this.control_id()+'">';
	html += '</div>';
	html += "</div>";
	this.jquery_place().replaceWith(html);
	this.set_value(this.properties.value);
	
	if(!this.properties.visible) this.hide();
};

////////////////////////////////////////////////////////////////////////////////

ControlFeed.prototype.get_value = function(){ 
	return this.properties.value;
};

////////////////////////////////////////////////////////////////////////////////

ControlFeed.prototype.compare_obj = function(a, b){ 
	if (a.timestamp < b.timestamp)
		return -1;
	if (a.timestamp > b.timestamp)
		return 1;
	return 0;
};

////////////////////////////////////////////////////////////////////////////////

ControlFeed.prototype.set_value = function(data){
	
	if(data.length==0) return; //no data to process

	//data.sort(this.compare_obj);
	var i = 0

	var self = this;

	for(var i=0; i<data.length; i++){
		var elements = this.jquery().find('[pk="'+data[i].pk+'"]');
		//console.log(elements.size());
		var e = $(data[i].html);
		e.attr('pk', data[i].pk);
		if(elements.size()>0){
			elements.replaceWith(e);
		}else{
			this.jquery().prepend( e );			
		};
		self.set_actions(e);
		
	};
	
	if(this.properties.visible) this.show(); else this.hide();
};

////////////////////////////////////////////////////////////////////////////////

ControlFeed.prototype.set_actions = function(element){
	this.properties.action_param = undefined;
	var self = this;
	
	element.find('[action]').click(function(){
		var action 					 = $(this).attr('action');
		var action_param 			 = $(this).attr('action-param');
		self.properties.action_param = action_param;
		self.basewidget.fire_event( 'self', action );
	});
};

////////////////////////////////////////////////////////////////////////////////

ControlFeed.prototype.update_server = function(){
	return true;
};


////////////////////////////////////////////////////////////////////////////////
