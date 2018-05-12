class ControlFeed extends ControlBase{

	
	init_control(){
		var html = "<div id='"+this.place_id()+"' class='field control'>";
		html += '<div class="ui '+this.properties.mode+' ControlFeed"  id="'+this.control_id()+'">';
		html += '</div>';
		html += "</div>";
		this.jquery_place().replaceWith(html);

		this.set_value(this.properties.value);

		if(this.properties.value==undefined || this.properties.value.length==0){
			this.jquery().html('<div class="ui basic center  very padded segment"><i class="icon ban" ></i></div>');
		}
		
		
	};

	////////////////////////////////////////////////////////////////////////////////

	get_value(){ 
		return this.properties.value;
	};

	////////////////////////////////////////////////////////////////////////////////

	set_value(data){
		
		if(data.length==0) return; //no data to process

		var i	 = 0
		var self = this;

		for(var i=0; i<data.length; i++){
			var elements = this.jquery().find('[pk="'+data[i].pk+'"]');
			var e = $(data[i].html); e.attr('pk', data[i].pk);
			
			if(elements.length>0){
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
		
	};

	////////////////////////////////////////////////////////////////////////////////

	set_actions(element){
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

	update_server(){
		return true;
	};

	////////////////////////////////////////////////////////////////////////////////

	deserialize(data){
		$.extend(this.properties, data);
		
		if(this.properties.clear) this.jquery().empty();
		
		this.set_value(this.properties.value);
	

		if(this.properties.error) this.jquery_place().addClass('error'); else this.jquery_place().removeClass('error');
	};

	////////////////////////////////////////////////////////////////////////////////

	update_server(){
		return this.properties.action_param != undefined;
	};

}


