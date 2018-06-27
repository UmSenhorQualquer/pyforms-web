class ControlCombo extends ControlBase{

	

	init_control(){
		var html = "<div id='"+this.place_id()+"' class='field control ControlCombo' ><label>"+this.properties.label+"</label>";
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
				self.basewidget.fire_event( self.name, 'update_control_event' );
		});
		
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
		var value = this.jquery().dropdown('get value');
		if( value.length==0 ) return null;
        if(value=='true')  return true;
		if(value=='false') return false;
		if(value=='null')  return null;
		return value;
	};

	////////////////////////////////////////////////////////////////////////////////

	deserialize(data){
		this.properties = $.extend(this.properties, data);
		
		this.jquery().dropdown('setup menu', { values: this.properties.items });
		this.set_value(this.properties.value);

		if(this.properties.error)
			this.jquery_place().addClass('error'); 
		else
			this.jquery_place().removeClass('error'); 
	};

	////////////////////////////////////////////////////////////////////////////////

}
