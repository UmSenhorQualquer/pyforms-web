class ControlThumbnailSelection extends ControlBase{

	////////////////////////////////////////////////////////////////////////////////
	init_control(){
		var html = `
			<div id='${this.place_id()}' class='field control ControlText' >
				<label for='${this.control_id()}'>${this.properties.label}</label>
				<div class="ui grid"  id='${this.control_id()}' ></div>
			</div>
		`;
		this.jquery_place().replaceWith(html);

		this.set_value(this.properties.value);

		/*
		var self = this;
		this.jquery().change(function(){
			self.basewidget.fire_event( this.name, 'update_control_event' );
		});

		this.jquery().keypress(function(e) {
        	if(e.which == 13)
				self.basewidget.fire_event( this.name, 'on_enter_event' );
		});

		if(this.properties.error) this.jquery_place().addClass('error'); else this.jquery_place().removeClass('error');
		if(this.properties.required) this.set_required();*/
	};
	////////////////////////////////////////////////////////////////////////////////

	set_value(value) {

		if( !this.properties.value ){
			return;
		}

		let html = '';
		const labels = this.properties.labels;

		for(let i=0; i<this.properties.value.length; i++){
			const obj = this.properties.value[i];

			html += `
				<div class="four wide column">
					<div class="ui card">
						<div class="ui slide masked reveal image">
							<img src="/media/thumbnails/${obj.thumbnails[0]}" class="visible content">
							<img src="/media/thumbnails/${obj.thumbnails[1]}" class="hidden content">
						</div>
						<div class="content">
							<div class="description">
								<div class="grouped fields">
			`;

			for(let j=0; j<labels.length; j++){
				html += `
					<div class="field">
						<div class="ui radio checkbox">
							<input type="radio" name="group_${obj['pk']}" pk="${obj['pk']}" label="${labels[j]}" checked="${(new String(obj['selected_label']).valueOf()===new String(labels[j]).valueOf())?'checked':''}" tabindex="0" class="hidden">
							<label>${labels[j]}</label>
						</div>
					</div>
				`;
			}

			html += `
								</div>
							</div>
						</div>
					</div>
				</div>
			`;
		}

		this.jquery().html(html);
		this.properties.value = [];

		const self = this;
		this.jquery().find('.ui.radio.checkbox').checkbox({
			onChange: function(){
				self.update_control = true;
				self.properties.selected_pk = $(this).attr('pk');
				self.properties.selected_label = $(this).attr('label');

				console.debug($(this).attr('pk'), $(this).attr('label '));
				self.basewidget.fire_event(self.name, 'update_selection_event' );
			}
		});
	}

	update_server() {
		if( this.update_control ){
			this.update_control = undefined;
			return true;
		}else{
			return false;
		}
	}
}
