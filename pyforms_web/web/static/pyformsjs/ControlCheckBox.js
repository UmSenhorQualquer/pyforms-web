class ControlCheckBox extends ControlBase{

	set_value(value){
		if(value)
			this.jquery().prop('checked', true);
		else
			this.jquery().prop('checked', false);
	};

	////////////////////////////////////////////////////////////////////////////////

	get_value(){
		if(this.jquery().length==0) return this.properties.value;
		return this.jquery().is(':checked');
	};

	////////////////////////////////////////////////////////////////////////////////

	init_control(){
		var html = "<div class='field control ControlCheckBox' id='"+this.place_id()+"' >";
		if(this.properties.label_visible)
			html += "<div style='height: 31px' ></div>";
		else
			html += "<div style='height: 3px' ></div>";
		html += `<div class='ui ${this.properties.checkbox_type} checkbox' >`;
		html += "<input name='"+this.name+"' id='"+this.control_id()+"' type='checkbox' value='true' class='hidden' />";
		html += `<label title='${this.properties.help}' for='${this.control_id()}'>${this.properties.label}</label>`;
		html += "</div></div>";
		this.jquery_place().replaceWith(html);

		if( this.properties.value)
			this.jquery().prop('checked', true);
		else
			this.jquery().prop('checked', false);


		var self = this;
		this.jquery().click(function(){ self.basewidget.fire_event( self.name, 'update_control_event' ); });

		if(!this.properties.visible) this.hide(undefined, true);
		if(this.properties.error) this.jquery_place().addClass('error'); else this.jquery_place().removeClass('error');
		if(this.properties.required) this.set_required();
	};

	////////////////////////////////////////////////////////////////////////////////

	set_label(value){
		var label = value;
		
		if(this.properties.help)
			label = label + `<i class="help circle icon" title="${this.properties.help}" style="margin: -0.2em 0em 0em 0.2em;"></i>`;
        $( `#${this.place_id()} label[for='${this.control_id()}']` ).first().html(label);
    }

    ////////////////////////////////////////////////////////////////////////////////

    /**
    Sets the css classes for the control. Previously added classes will be removed.
    @param {string} css - String with the css classes to add.
    */
    set_css(css){
        for(var i=0; i<this.added_classes.length; i++)
            this.jquery_place().children('.ui.checkbox').removeClass(this.added_classes[i]);

        var classes = css.split(" ");

        for(var i=0; i<classes.length; i++)
            this.jquery_place().children('.ui.checkbox').addClass(classes[i]);

        this.added_classes = classes;
    }


}
