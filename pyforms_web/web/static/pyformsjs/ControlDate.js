class ControlDate extends ControlBase{

	get_value(){ 
		//if(this.jquery().length==0) return this.properties.value;
		return this.jquery().datepicker('getDate');
	};

	pad(number, size){
        var s = String(number);
        while (s.length < (size || 2)) {s = "0" + s;}
        return s;
    }

    formatdate(date){
        return date.getFullYear()+'-'+this.pad(date.getMonth()+1,2)+'-'+this.pad(date.getDate(),2);
    }

    set_value(value){
        if(value!=null)
            this.jquery().val(this.formatdate(new Date(value)));
        else
            this.jquery().val('');
    }

	////////////////////////////////////////////////////////////////////////////////

	init_control(){
		var html = "<div id='"+this.place_id()+"' class='field control ControlDate' ><label>"+this.properties.label+"</label><input placeholder='"+this.properties.label+"' type='text' name='"+this.name+"' id='"+this.control_id()+"' /></div>";
		this.jquery_place().replaceWith(html);
		this.set_value(this.properties.value);
		
		this.jquery().datepicker({
			dateFormat: "yy-mm-dd", 
			changeMonth: true,
			changeYear: true,
			yearRange: "1900:3000"
		});

		this.set_value(this.properties.value);

		var self = this;
		this.jquery().change(function(){
			self.basewidget.fire_event( self.name, 'update_control_event' );
		});

		if(this.properties.error) this.jquery_place().addClass('error'); else this.jquery_place().removeClass('error'); 
	};

	////////////////////////////////////////////////////////////////////////////////


}
	