class ControlDateTime extends ControlBase{


	////////////////////////////////////////////////////////////////////////////////

	init_control(){

		var value = this.properties.value;
		if(value==null) value = '';

		var html = "<div id='"+this.place_id()+"' class='field ControlDateTime' ><label>"+this.properties.label+"</label><input placeholder='"+this.properties.label+"' type='text' name='"+this.name+"' id='"+this.control_id()+"' value=\""+value+"\" /></div>";
		this.jquery_place().replaceWith(html);

		this.jquery().datetimepicker({
			format:'Y-m-d H:i',
			formatTime:'H:i',
			formatDate:'Y-m-d'
		});

		var self = this;
		this.jquery().on("change", function(){
			self.basewidget.fire_event( self.name, 'changed_event' );
		});

		if(!this.properties.enabled){
			this.jquery().attr('disabled', '');
		}else{
			this.jquery().removeAttr('disabled');
		};

		if(!this.properties.visible) this.hide(undefined, true);
		if(this.properties.error) this.jquery_place().addClass('error'); else this.jquery_place().removeClass('error'); 
	};

	////////////////////////////////////////////////////////////////////////////////
}