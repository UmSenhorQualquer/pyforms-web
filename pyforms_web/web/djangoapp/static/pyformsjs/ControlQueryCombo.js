class ControlQueryCombo extends ControlBase{

	////////////////////////////////////////////////////////////////////////////////

	init_control(){
		var html = "<div id='"+this.place_id()+"' class='field ControlQueryCombo' ><label>"+this.properties.label+"</label>";
		html += "<select class='ui search dropdown' id='"+this.control_id()+"' ></select></div>";

		this.jquery_place().replaceWith(html);
		var select = document.getElementById(this.control_id());
		var index;
		for (var index = 0; index < this.properties.items.length; ++index) {
			var option = document.createElement("option");
			option.text  = this.properties.items[index].label;
			option.value = this.properties.items[index].value;
			select.add(option);
		}

		var self = this;
		this.jquery().dropdown({onChange:function(){
			self.basewidget.fire_event( self.name, 'changed_event' );
		}});
		
		if(!this.properties.visible) this.hide();
		this.set_value(this.properties.value);

		if(!this.properties.enabled){
			$('#'+this.place_id()+' .ui.dropdown').addClass("disabled")
		}else{
			$('#'+this.place_id()+' .ui.dropdown').removeClass("disabled")
		};

		
		if(this.properties.error) this.jquery_place().addClass('error'); else this.jquery_place().removeClass('error'); 
	};

	////////////////////////////////////////////////////////////////////////////////

	set_value(value){
		this.jquery().dropdown('set value', value );
	};

	////////////////////////////////////////////////////////////////////////////////

	get_value(){ 
		return this.jquery().dropdown('get value')[0];
	};

	////////////////////////////////////////////////////////////////////////////////

	deserialize(data){
		this.properties = $.extend(this.properties, data);
		
		/*
		if( this.jquery().length>0 ){
			this.jquery().empty();
			var select = document.getElementById(this.control_id());
			for (var index = 0; index < this.properties.items.length; ++index) {
				var option = document.createElement("option");
				option.text  = this.properties.items[index].label;
				option.value = this.properties.items[index].value;
				select.add( option );
			}
		}
		this.jquery().dropdown('setup menu');*/

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