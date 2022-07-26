class ControlInteger extends ControlBase{

	////////////////////////////////////////////////////////////////////////////////

	init_control(){
		var html = `<div id='${this.place_id()}' class='field control ControlInteger' >
					<label for='${this.control_id()}' >${this.properties.label}</label>
					<input placeholder='${this.properties.placeholder}' type='text' name='${this.name}' id='${this.control_id()}' />
					</div>`;
		this.jquery_place().replaceWith(html);
		this.set_value(this.properties.value);

		this.jquery().change(()=>{
			console.debug('update_control_event')
			this.basewidget.fire_event( this.name, 'update_control_event' );
		});

		if(this.properties.error) this.jquery_place().addClass('error'); else this.jquery_place().removeClass('error');
		if(this.properties.required) this.set_required();
	};

	////////////////////////////////////////////////////////////////////////////////

}

