class ControlProgress extends ControlBase{

	init_control(){

		var html = `<div id='${this.place_id()}' class='field control ControlProgress' >
		    <div title='${this.properties.help}' class="ui progress" id='${this.control_id()}'>
			  <div class="bar">
				<div class="progress"></div>
			  </div>
			  ${this.properties.label_visible?`<div class="label" for="${this.control_id()}">${this.properties.label}</div>`:''}
			</div>
		</div>`;
        this.jquery_place().replaceWith(html);

		if(this.properties.required) this.set_required();
	};

	////////////////////////////////////////////////////////////////////////////////

	set_value(value) {
		this.jquery().progress({total: this.properties.max, value: this.properties.value})
	}

	////////////////////////////////////////////////////////////////////////////////

    /**
    Sets the label of the control.
    @param {string} value - Label to set.
    */
    set_label(value){
        $( `#${this.place_id()} .label[for='${this.control_id()}']` ).first().html(value);
    }
}