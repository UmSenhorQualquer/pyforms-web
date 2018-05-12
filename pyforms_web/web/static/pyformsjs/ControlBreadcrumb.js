class ControlBreadcrumb extends ControlBase{


	////////////////////////////////////////////////////////////////////////////////

	init_control(){
		var html = "<div class='field control ControlBreadcrumb' id='"+this.place_id()+"' >";
		html += '<div class="ui breadcrumb">';
		if(this.properties.value)
			for( var i=0; i<this.properties.value.length; i++){
				var breadcrumb = this.properties.value[i];

				var label  = breadcrumb.label;
				var action = breadcrumb.action_param;
				var link   = breadcrumb.link;
				var attrs  = (breadcrumb.active)?'class="active section"':'class="section"';
				
				if(link || action){
					attrs += (link)?"href='"+link+"'":"action-param='"+action+"'";
					html += '<a class="section" '+attrs+' >'+label+'</a>';
					html += '<i class="right angle icon divider"></i>';
				}
				else{
					html += '<div '+attrs+' >'+label+'</div>';
				}
			};
		html += '</div>';
		html += '</div>';
		
		this.jquery_place().replaceWith(html);

		var self = this;
		this.jquery().find('[action-param]').click(function(){
			var action_param 			 = $(this).attr('action-param');
			self.properties.action_param = action_param;
			self.basewidget.fire_event( self.name, 'pressed' );
		});

	};

	////////////////////////////////////////////////////////////////////////////////

	get_value(){ 
		return this.properties.value;
	};


	////////////////////////////////////////////////////////////////////////////////

	update_server(){
		return false;
	};

}