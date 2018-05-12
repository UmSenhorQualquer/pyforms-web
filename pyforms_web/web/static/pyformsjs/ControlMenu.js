class ControlMenu extends ControlBase{

	get_value(){ 
		return this.properties.value;
	};

	////////////////////////////////////////////////////////////////////////////////

	init_control(){
		var html = '<div id="'+this.place_id()+'" class="field control ControlMenu">';
		if(this.properties.label) html += '<label>'+this.properties.label+'</label>';
		html += '<div id="'+this.control_id()+'" class="ui vertical accordion menu">';

		menu = this.properties.value;
		
		for(var i=0; i<menu.length; i++){
			html += '<div class="item">';
			html += '<a class="active title"><i class="dropdown icon"></i> <b>'+menu[i][0]+'</b></a>';
			html += '<div class="active content menu">';

			for(var j=0; j<menu[i][1].length; j++){
				html += '<a class="item" href="javascript:pyforms.find_app(\''+this.app_id()+'\').fire_event(\'self\', \''+menu[i][1][j][1]+'\');">'+menu[i][1][j][0]+'</a>';			
			};
			html += '</div>';
			html += '</div>';
		};
		html += '</div>';
		html += '</div>';


		this.jquery_place().replaceWith(html);
		this.jquery_place().accordion({exclusive: false});

		
	};

	////////////////////////////////////////////////////////////////////////////////

	set_value(value){
		this.init_control();
	};

	////////////////////////////////////////////////////////////////////////////////
	
}


	