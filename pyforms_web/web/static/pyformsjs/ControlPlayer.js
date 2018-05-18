class ControlPlayer extends ControlBase{

    
    get_value(){ 
        this.properties.video_index = $( "#timeline"+this.control_id()).val();
        return this.properties.value; 
    };

    ////////////////////////////////////////////////////////////////////////////////

    set_value(value){
        if(this.properties.base64content){
            $("#display"+this.control_id()).attr("src", "data:image/png;base64,"+this.properties.base64content);
            
            $( "#timeline"+this.control_id()).val(this.properties.video_index);
            $( "#timeline"+this.control_id()).attr("min", 0);
            $( "#timeline"+this.control_id()).attr("max", this.properties.endFrame);
        }
    };

    ////////////////////////////////////////////////////////////////////////////////

    init_control(){

        var html = "<div id='"+this.place_id()+"' class='field control ControlPlayer' >";
        html += "<div class='ui card "+this.properties.css+"' id='card"+this.control_id()+"' >";
        html += "<div class='image'>";
        html += "<img style='width:100%;' class='image' src='data:image/png;base64,"+this.properties.base64content+"' id='display"+this.control_id()+"' />";
        html += "</div>";
        html += "<div class='content'>";
        html += "<input style='width:100%;' type='range' name='"+this.name+"' value='"+this.properties.value+"' id='timeline"+this.control_id()+"' max='"+this.properties.endFrame+"'>";
        html += "</div>";
        html += "</div>";
        html += "</div>";

        this.jquery_place().replaceWith(html);

        
        var self = this;
        $( "#timeline"+this.control_id() ).change(
            function(){ self.basewidget.fire_event( self.name, 'refresh' ); }
        );  
    };

    ////////////////////////////////////////////////////////////////////////////////

    update_server(){
        return this.properties.video_index != $( "#timeline"+this.control_id() ).val()
    }

    ////////////////////////////////////////////////////////////////////////////////

    serialize(){
        super.serialize();
        this.properties.base64content = null;
        return this.properties;
    }

}