function add_file2control(control_id, filename){
	$( "#dialog"+control_id ).modal('hide');
	$( "#"+control_id ).val(filename);
	
	var ids 			= pyforms.split_id(control_id);
	var widget_id 		= ids[0];
	var control_name 	= ids[1];

	pyforms.find_app(widget_id).fire_event( control_name, 'update_control_event' )
}

class ControlFile extends ControlBase{

	

	////////////////////////////////////////////////////////////////////////////////

	init_control(){
		var value = this.properties.value?this.properties.value:'';
		var html = "<div class='field control ControlFile' id='"+this.place_id()+"' >";
		html += "<label>"+this.properties.label+"</label>";
		html += "<input type='text' class='filename' name='"+this.name+"' id='"+this.control_id()+"' value='"+value+"'  placeholder='"+this.properties.label+"' />";
		html += "</div>";
		
		this.jquery_place().replaceWith(html);

		/*
		var self = this;
		function reload_folder(){
			var folder = get_current_folder();
			$( "#dialog-content-"+self.control_id()).load(
				'/pyforms/filesbrowser/?p='+folder+'&control-id='+self.control_id(),
				function(){
					$( "#dialog"+self.control_id() ).modal('show');
				}
			);
		}
		this.jquery().unbind('click');
		this.jquery().click(reload_folder);
		*/
		var self = this;
		this.jquery().click(function(){
			self.basewidget.fire_event( self.name, 'open_file_browser' );
		});
		
		if(this.properties.error) this.jquery_place().addClass('error'); else this.jquery_place().removeClass('error'); 
	};


}

