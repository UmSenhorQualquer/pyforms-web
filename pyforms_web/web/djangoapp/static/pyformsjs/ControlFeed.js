
function ControlFeed(name, properties){
	ControlBase.call(this, name, properties);
};
ControlFeed.prototype = Object.create(ControlBase.prototype);

////////////////////////////////////////////////////////////////////////////////

ControlFeed.prototype.init_control = function(){
	var html = "<div id='"+this.place_id()+"' class='field'>";
	html += '<div class="ui '+this.properties.mode+' ControlFeed"  id="'+this.control_id()+'">';
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

ControlFeed.prototype.set_value = function(data){
	
	if(data.length==0) return; //no data to process

	var i	 = 0
	var self = this;

	for(var i=0; i<data.length; i++){
		var elements = this.jquery().find('[pk="'+data[i].pk+'"]');
		var e = $(data[i].html); e.attr('pk', data[i].pk);
		
		if(elements.size()>0){
			elements.replaceWith(e);
		}else{
			this.jquery().append( e );
		};
		self.set_actions(e);
	};
	
	this.jquery().find('[action="load_more"]').remove();
	
	if(this.properties.has_more){
		var e = $('<div class="fluid ui button" action="load_more" action-param="'+data[data.length - 1].pk+'" >More</div>');
		this.jquery().append(e);
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
	
	if( element.attr('action') )
		element.click(function(){
			var action 					 = element.attr('action');
			var action_param 			 = element.attr('action-param');
			self.properties.action_param = action_param;
			self.basewidget.fire_event( 'self', action );
		});
};

////////////////////////////////////////////////////////////////////////////////

ControlFeed.prototype.update_server = function(){
	return true;
};

////////////////////////////////////////////////////////////////////////////////

ControlFeed.prototype.deserialize = function(data){
	$.extend(this.properties, data);
	
	if(this.properties.clear) this.jquery().empty();
	
	this.set_value(this.properties.value);
	
	if(this.properties.visible)  this.show();
	else this.hide();

	if(!this.properties.enabled)
		this.jquery().attr('disabled', '');
	else
		this.jquery().removeAttr('disabled');

	if(this.properties.error) this.jquery_place().addClass('error'); else this.jquery_place().removeClass('error');
};

////////////////////////////////////////////////////////////////////////////////

ControlFeed.prototype.update_server = function(){
	return this.properties.action_param != undefined;
};
