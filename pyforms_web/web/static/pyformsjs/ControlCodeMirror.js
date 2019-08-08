class ControlCodeMirror extends ControlBase{

	////////////////////////////////////////////////////////////////////////////////
	init_control(){
		var html = "<div id='"+this.place_id()+"' class='field control ControlCodeMirror' >"
		if(this.properties.label_visible) html += "<label>"+this.properties.label+"</label>";
		html += `<textarea id='${this.control_id()}' ></textarea>`;
		html += "</div>";
		this.jquery_place().replaceWith(html);

		var mixedMode = {
			name: "htmlmixed",
			scriptTypes: [
				{matches: /\/x-handlebars-template|\/x-mustache/i, mode: null},
				{matches: /(text|application)\/(x-)?vb(a|script)/i, mode: "vbscript"}
			]
		};
		var myTextArea = document.getElementById(this.control_id());
		this.codemirror = CodeMirror(
			function(elt){ myTextArea.parentNode.replaceChild(elt, myTextArea);},
			{ mode: mixedMode, autoRefresh: true }
		);
		var self = this;
		this.codemirror.on('blur',function () {
			self.basewidget.fire_event( self.name, 'update_control_event' );
		})
		this.codemirror.setSize(this.properties.width, this.properties.height);
		this.set_value(this.properties.value);
		if(this.properties.error) this.jquery_place().addClass('error'); else this.jquery_place().removeClass('error');
		if(this.properties.required) this.set_required();

	};
	////////////////////////////////////////////////////////////////////////////////

	get_value(){
        return this.codemirror.getValue();
    }

    ////////////////////////////////////////////////////////////////////////////////

    /**
    Sets the value of the control.
    @param {object} value - Value to set.
    */
    set_value(value){
        this.codemirror.setValue(this.properties.value);
        this.codemirror.refresh();
    }

}