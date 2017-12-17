class ControlCombo extends ControlBase{

	

	init_control(){
		var html = "<div id='"+this.place_id()+"' class='field ControlCombo' ><label>"+this.properties.label+"</label>";
		html += "<div class='ui search dropdown selection' id='"+this.control_id()+"' >"
		html += '<i class="dropdown icon"></i>';
		html += '<div class="default text">'+this.properties.label+'</div>';
		html += '</div>';
		
		var self = this;
		this.jquery_place().replaceWith(html);
		this.jquery().dropdown();
		this.jquery().dropdown('setup menu', { values: this.properties.items });
		this.set_value(this.properties.value);
		
		this.jquery().dropdown('setting', 'onChange', function(){
			if(self.flag_exec_on_change_event)
				self.basewidget.fire_event( self.name, 'changed_event' );
		});
		
		if(!this.properties.visible) this.hide();
		if(!this.properties.enabled){
			$('#'+this.place_id()+' .ui.dropdown').addClass("disabled")
		}else{
			$('#'+this.place_id()+' .ui.dropdown').removeClass("disabled")
		};	
		if(this.properties.error) this.jquery_place().addClass('error'); else this.jquery_place().removeClass('error'); 
	};

	////////////////////////////////////////////////////////////////////////////////

	set_value(value){
		this.flag_exec_on_change_event = false;
		this.jquery().dropdown('set exactly', [value]);
		this.flag_exec_on_change_event = true;
	};

	////////////////////////////////////////////////////////////////////////////////

	get_value(){ 
		return this.jquery().dropdown('get value');
	};

	////////////////////////////////////////////////////////////////////////////////

	deserialize(data){
		this.properties = $.extend(this.properties, data);
		
		this.jquery().dropdown('setup menu', { values: this.properties.items });
		this.set_value(this.properties.value);

		if(!this.properties.enabled){
			$('#'+this.place_id()+' .ui.dropdown').addClass("disabled")
		}else{
			$('#'+this.place_id()+' .ui.dropdown').removeClass("disabled")
		};


		if(!this.properties.visible) this.hide();
		else this.show();
		if(this.properties.error) this.jquery_place().addClass('error'); else this.jquery_place().removeClass('error'); 
	};

	////////////////////////////////////////////////////////////////////////////////

}
