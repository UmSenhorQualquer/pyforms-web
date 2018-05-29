class ControlMultipleChecks extends ControlBase{

    ////////////////////////////////////////////////////////////////////////////////

    set_value(value){
        this.flag_exec_on_change_event = false;
        if(value==null || value==undefined || value.length==0){
            $("#"+this.place_id()+' .ui.checkbox').checkbox('uncheck');
            return;
        };
        for(var i=0; i<this.properties.items.length; i++){
            var item = this.properties.items[i];

            var c = $("#"+this.place_id()+' .ui.checkbox[value="'+item.value+'"]');
            if(value.indexOf(item.value)>-1){
                c.checkbox('set checked');
            }else{
                c.checkbox('set unchecked');
            };
        };
        this.flag_exec_on_change_event = true;
    };

    ////////////////////////////////////////////////////////////////////////////////

    get_value(){ 
        var values = [];
        for(var i=0; i<this.properties.items.length; i++){
            var item = this.properties.items[i];
            var c = $("#"+this.place_id()+' .ui.checkbox[value="'+item.value+'"]')
            if(c.checkbox('is checked'))
                values.push(item.value)
        };
        return values;
    };


    ////////////////////////////////////////////////////////////////////////////////

    init_control(){
        var html = "<div class='field control ControlMultipleChecks' id='"+this.place_id()+"' >";
        if(this.properties.label_visible) html += "<label for='"+this.control_id()+"'>"+this.properties.label+"</label>";
           
        html += '<div class="ui grid">';
  
        for(var i=0; i<this.properties.items.length; i++){
            var item = this.properties.items[i];
            html += '<div class="five wide column">'; 
                html += '<div class="ui checkbox" value="'+item.value+'" >';
                html += '<input type="checkbox" value="'+item.value+'" name="'+this.properties.name+'">';
                html += '<label>'+item.text+'</label>';
                html += '</div>';
            html += '</div>';
        }

        html += '</div>';
        html += '</div>';
    
        this.jquery_place().replaceWith(html);
        this.set_value(this.properties.value);

        this.flag_exec_on_change_event = true;
        $("#"+this.place_id()+' .ui.checkbox').checkbox({
            onChange:function(){
                if(self.flag_exec_on_change_event)
                    self.basewidget.fire_event( this.name, 'update_control_event' );
            }
        });

        if(this.properties.error) this.jquery_place().addClass('error'); else this.jquery_place().removeClass('error'); 
        
    };

    ////////////////////////////////////////////////////////////////////////////////
    /*
    deserialize(data){
        var previous_value = this.properties.value;
        this.properties = $.extend(this.properties, data);
        
        if(this.properties.update_items)
            this.jquery().dropdown('setup menu', { values: this.properties.items });
        
        if(this.properties.value==null)
            this.set_value(null);
        else
            if(previous_value.toString()!=this.properties.value.toString()){
                this.set_value(this.properties.value);
            }

        if(!this.properties.enabled){
            $('#'+this.place_id()+' .ui.dropdown').addClass("disabled")
        }else{
            $('#'+this.place_id()+' .ui.dropdown').removeClass("disabled")
        };

        
        ;
        if(this.properties.error) this.jquery_place().addClass('error'); else this.jquery_place().removeClass('error'); 
    };*/

    ////////////////////////////////////////////////////////////////////////////////

    
}