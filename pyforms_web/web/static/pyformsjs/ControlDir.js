class ControlDir extends ControlBase{

	////////////////////////////////////////////////////////////////////////////////

	init_control(){

		var html = "<div class='field control ControlDir' id='"+this.place_id()+"' ><label>"+this.properties.label+"</label>";
		html += "<input type='text' class='filename' basewidget='"+this.basewidget.widget_id+"' name='"+this.name+"' id='"+this.control_id()+"' value='"+this.properties.value+"'  placeholder='"+this.properties.label+"' />";
		html += "<div class='ui modal' id='dialog"+this.control_id()+"' ><i class='close icon'></i><div class='header'>"+this.properties.label+"</div><div class='content' id='dialog-content-"+this.control_id()+"'  dom-id='"+this.control_id()+"' ></div></div>";
		
		this.jquery_place().replaceWith(html);

		var self = this;
		function reload_folder(){
			var folder = get_current_folder();
			$( "#dialog-content-"+self.control_id()).load(
				'/pyforms/filesbrowser/?filter-folders=true&p='+folder+'&control-id='+self.control_id(),
				function(){
					$( "#dialog"+self.control_id() ).modal('show');
				}
			);
		}

		this.jquery().unbind('click');
		this.jquery().click(reload_folder);

		
		if(this.properties.error) this.jquery_place().addClass('error'); else this.jquery_place().removeClass('error'); 
	};

	////////////////////////////////////////////////////////////////////////////////

}
