class ControlCalendar extends ControlBase{

	

	init_control(){
		
		var html = "<div id='"+this.place_id()+"' class='field control ControlCalendar' ><label>"+this.properties.label+"</label>";
		html += this.create_calendar();
		html += "</div>";
		
		this.jquery_place().replaceWith(html);
		
		
		if(this.properties.error) this.jquery_place().addClass('error'); else this.jquery_place().removeClass('error'); 
		
	};

	////////////////////////////////////////////////////////////////////////////////

	create_calendar(){
		var date  = new Date(this.properties.year, this.properties.month, 0);
		var today = new Date();
		
		var html = "<div class='ui seven column grid' id='"+this.control_id()+"' >";
		for(var n=0; n<date.getDay(); n++) html += "<div class='column'></div>";	
		for(var i=1; i<=date.getDate();i++){
			if( date.getYear()==today.getYear() && date.getMonth()==today.getMonth() && i==today.getDate() )
				html += "<div class='column green'>"+i;
			else
				html += "<div class='column'>"+i;
			if( this.properties.value && (i in this.properties.value) ){
				html += "<small>";
				for(var j=0; j<this.properties.value[i].length; j++)
					html += "</br>"+this.properties.value[i][j];
				html += "</small>";
			};
			html += "</div>";
		};
		html += "</div>";
		return html;
	};

	////////////////////////////////////////////////////////////////////////////////


	set_value(value){
		
		var html = this.create_calendar()
		$("#"+this.control_id()).replaceWith(html);
		
	};

	////////////////////////////////////////////////////////////////////////////////

	get_value(){ 
		return this.properties.value;
	};


	////////////////////////////////////////////////////////////////////////////////
}
