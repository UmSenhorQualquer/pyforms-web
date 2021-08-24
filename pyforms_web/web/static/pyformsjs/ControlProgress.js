class ControlProgress extends ControlBase{

	init_control(){

		var html = `<div id='${this.place_id()}' class='field control ControlProgress' >
		    <div title='${this.properties.help}' class="ui progress" id='${this.control_id()}'>
			  <div class="bar">
				<div class="progress"></div>
			  </div>
			  ${this.properties.label_visible?`<div class="label">${this.properties.label}</div>`:''}
			</div>
		</div>`;
        this.jquery_place().replaceWith(html);

		if(this.properties.required) this.set_required();
	};

	set_value(value) {
		this.jquery().progress({total: this.properties.max, value: this.properties.value})
	}


	deserialize(data){
        super.deserialize(data);
    }
}