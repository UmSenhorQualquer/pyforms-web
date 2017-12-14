class ControlButton extends ControlBase{


	////////////////////////////////////////////////////////////////////////////////

	init_control(){
		var html = "<div class='field ControlButton' id='"+this.place_id()+"' >";
		if(this.properties.include_label) html += '<label>&nbsp;</label>';
		html +="<button type='button' title='"+this.properties.help+"' id='"+this.control_id()+"' class='ui button' >";
		html += this.properties.label;
		html += '</button>';
		html += '</div>';
		
		this.jquery_place().replaceWith(html);

		var self = this;
		this.jquery().click(function(){
			if( self.properties.value.length>0 )
				eval(self.properties.value);
			else{
				
				self.basewidget.fire_event( self.name, 'pressed' );
			};
		});

		//console.log(!this.properties.visible, this.jquery_place().html(), '-');
		if(!this.properties.visible) this.hide(undefined, true);
		if(this.properties.css) this.jquery().addClass(this.properties.css);

	};

	////////////////////////////////////////////////////////////////////////////////

	get_value(){ 
		return this.properties.value;
	};


	////////////////////////////////////////////////////////////////////////////////

	update_server(){
		return false;
	};


	deserialize(data){
		if(data.css!=this.properties.css)
			this.jquery().removeClass(this.properties.css);
		

		$.extend(this.properties, data);
		this.set_value(this.properties.value);

		this.jquery().html(this.properties.label);

		this.jquery().addClass(this.properties.css);
		
		if(this.properties.visible) 
			this.show();
		else 
			this.hide();

		if(!this.properties.enabled){
			this.jquery().attr('disabled', '');
		}else{
			this.jquery().removeAttr('disabled');
		};

		if(this.properties.error) this.jquery_place().addClass('error'); else this.jquery_place().removeClass('error');
	};

}