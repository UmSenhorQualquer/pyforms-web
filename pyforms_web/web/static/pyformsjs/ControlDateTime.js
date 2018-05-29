class ControlDateTime extends ControlBase{

    get_value(){ 
        //if(this.jquery().length==0) return this.properties.value;
        return this.jquery().datetimepicker('getValue');
    }

    pad(number, size){
        var s = String(number);
        while (s.length < (size || 2)) {s = "0" + s;}
        return s;
    }

    formatdate(date){
        return date.getFullYear()+'-'+this.pad(date.getMonth()+1,2)+'-'+this.pad(date.getDate(),2)+' '+this.pad(date.getHours(),2) + ":" + this.pad(date.getMinutes(),2);
    }

    set_value(value){
        if(value!=null)
            this.jquery().val(this.formatdate(new Date(value)));
        else
            this.jquery().val('');
    }

    ////////////////////////////////////////////////////////////////////////////////

    init_control(){

        var html = "<div id='"+this.place_id()+"' class='field control ControlDateTime' ><label>"+this.properties.label+"</label><input placeholder='"+this.properties.label+"' type='text' name='"+this.name+"' id='"+this.control_id()+"' value='' /></div>";
        this.jquery_place().replaceWith(html);
        this.set_value(this.properties.value);
        
        this.jquery().datetimepicker({
            format:'Y-m-d H:i',
            formatTime:'H:i',
            formatDate:'Y-m-d'
        });

        var self = this;
        
        this.jquery().change(function(){
            self.basewidget.fire_event( self.name, 'update_control_event' );
        });


        if(this.properties.error) this.jquery_place().addClass('error'); else this.jquery_place().removeClass('error'); 
    };

    ////////////////////////////////////////////////////////////////////////////////



}