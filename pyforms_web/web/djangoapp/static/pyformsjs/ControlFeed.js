
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

	this.jquery().children().each(function(){
		var pk = $(this).attr('pk');
		if(i<data.length){
			if( pk>data[i].pk ){
				var e = $(data[i].html)
				e.insertBefore( $(this) );
				e.attr('pk', data[i].pk);
				self.set_actions(e);
				i++;
			}else if( pk==data[i].pk ){
				var e = $(data[i].html)
				e.insertBefore( $(this) );
				e.attr('pk', data[i].pk);
				self.set_actions(e);
				$(this).remove();
				i++;
			};
		};
	});

	for(var j=i;j<data.length;j++){
		var e = $(data[j].html);
		e.prependTo(this.jquery());
		e.attr('pk', data[j].pk);
		self.set_actions(e);
	};

	if(this.properties.visible) this.show(); else this.hide();
};

////////////////////////////////////////////////////////////////////////////////

ControlFeed.prototype.set_actions = function(element){
	this.properties.action_param = undefined;
	var self = this;
	
	element.find('[action]').click(function(){
		console.log(element.html());
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
