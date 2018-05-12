class ControlLabel extends ControlBase{

    ////////////////////////////////////////////////////////////////////////////////

    get_value(){ 
        return this.properties.value;
    };

    ////////////////////////////////////////////////////////////////////////////////

    init_control(){
        var html = '<div class="ui field '+this.properties.css+' message control ControlLabel" id="'+this.place_id()+'"  >';
        html += '<div class="header">';
        html += this.properties.label;
        html += '</div>';
        html += '<p id="'+this.control_id()+'" >';
        if(this.properties.value!=null || this.properties.value!=undefined)
            html += this.properties.value;
        html += '</p>';
        html += '</div>';
        this.jquery_place().replaceWith(html);

       
    };

    ////////////////////////////////////////////////////////////////////////////////

    set_value(value){
        this.init_control();
    };

    ////////////////////////////////////////////////////////////////////////////////
    
}
