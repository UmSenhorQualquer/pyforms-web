class ControlTime extends ControlBase{

	getItems(value){
		var items = [];
		var used = false;
		for(var t=0; t<=1440; t+=30){

			if( !used && value>t ){
				items.push(
					{
						value: t,
						text: String(Math.floor(value / 60)).padStart(2, '0') + ':' + String(Math.floor(value % 60)).padStart(2, '0'),
						name: String(Math.floor(value / 60)).padStart(2, '0') + ':' + String(Math.floor(value % 60)).padStart(2, '0')
					}
				);
				used = true;
			}

			items.push(
				{
					value: t,
					text: String(Math.floor(t / 60)).padStart(2, '0') + ':' + String(Math.floor(t % 60)).padStart(2, '0'),
					name: String(Math.floor(t / 60)).padStart(2, '0') + ':' + String(Math.floor(t % 60)).padStart(2, '0')
				}
			);
		}
		return items;
	}

	init_control(){
		var html = "<div id='"+this.place_id()+"' class='field control ControlTime' ><label>"+this.properties.label+"</label>";
		html += "<div class='ui search dropdown selection' id='"+this.control_id()+"' >"
		html += '<i class="dropdown icon"></i>';
		html += '<div class="default text">'+this.properties.placeholder+'</div>';
		html += '</div>';

		var self = this;
		this.jquery_place().replaceWith(html);
		this.jquery().dropdown();
		this.jquery().dropdown('setup menu', { values: this.getItems(this.properties.value) });
		this.set_value(this.properties.value);

		this.jquery().dropdown('setting', 'onChange', function(){
			if(self.flag_exec_on_change_event)
				self.basewidget.fire_event( self.name, 'update_control_event' );
		});

		if(this.properties.error) this.jquery_place().addClass('error'); else this.jquery_place().removeClass('error');
		if(this.properties.required) this.set_required();
	};

	////////////////////////////////////////////////////////////////////////////////

	set_value(value){
		this.flag_exec_on_change_event = false;
		this.jquery().dropdown('set exactly', [String(value)]);
		this.flag_exec_on_change_event = true;
	};

	////////////////////////////////////////////////////////////////////////////////

	get_value(){
		var value = this.jquery().dropdown('get value');
		if(value=='None') return null;
        if(value=='true')  return true;
		if(value=='false') return false;
		if(value=='null')  return null;
		return value;
	};

	////////////////////////////////////////////////////////////////////////////////

	deserialize(data){
		this.properties = $.extend(this.properties, data);

		this.jquery().dropdown('setup menu', { values: this.getItems(this.properties.value) });
		this.set_value(this.properties.value);

		if(this.properties.error)
			this.jquery_place().addClass('error');
		else
			this.jquery_place().removeClass('error');
	};

	////////////////////////////////////////////////////////////////////////////////

}
