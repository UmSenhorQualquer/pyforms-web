class ControlOrganogram extends ControlBase{

    ////////////////////////////////////////////////////////////////////////////////

    init_control(){

        var html = `
            <div class='field control ControlOrganogram' id='${this.place_id()}' >
            </div>`;
        
        this.jquery_place().replaceWith(html);

        var config = [{
            container: "#"+this.place_id(),
            connectors: { type: 'curve' }
        }];

        var x = conf.concat(this.properties.value);
        this.graph = new Treant( chart_config );
		if(this.properties.required) this.set_required();
    };

    ////////////////////////////////////////////////////////////////////////////////

}
