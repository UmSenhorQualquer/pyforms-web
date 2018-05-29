class ControlCheckBoxList extends ControlBase{

    constructor(name, properties){
        super(name, properties);
        this.being_edited = false;
    }

    ////////////////////////////////////////////////////////////////////////////////

    init_control(){
        this.set_value(this.properties.value);
        
    };

    ////////////////////////////////////////////////////////////////////////////////

    get_value(){ 
        if( !this.properties.value ) return [];

        var values = this.properties.value.slice(0);
        $( "#"+this.control_id()+" tbody tr" ).each(function(i, row){
            values[i][0] = $(this).find('.checkbox').checkbox('is checked');
        });
        return values;
    };


    ////////////////////////////////////////////////////////////////////////////////

    set_value(value){
        this.load_table();

    };

    ////////////////////////////////////////////////////////////////////////////////

    load_table(){
        var html = "<div id='"+this.place_id()+"' class='field control'>";
        if(this.properties.label_visible) html += '<label>'+this.properties.label+'</label>';
        html += "<table class='ui selectable celled table "+this.properties.css+" ControlCheckBoxList' id='"+this.control_id()+"' >";
        html += "<thead>";
        html += "<tr>";
        var titles = this.properties.headers;
        for(var i=0; i<titles.length; i++) html += "<th>"+titles[i]+"</th>";
        html += "</tr>";
        html += "</thead>";
        html += "<tbody>";
        var data = this.properties.value;
        
        if(data!=undefined)
            for(var i=0; i<data.length; i++){
                html += "<tr>";
                html += "<td class='collapsing' >";
                html += "<div class='ui fitted "+(data[i][0]?"active":"")+" checkbox'>";
                html += "<input type='checkbox' "+(data[i][0]?"checked=''":"")+" />";
                html += "<label></label></div>";
                html += "</td>";
 
                var length = data[i]?data[i].length:0;
                length     = length>titles.length?titles.length:length;
                for(var j=1; j<length; j++) html += "<td>"+data[i][j]+"</td>";
                if(length<titles.length) 
                    for(var j=length; j<titles.length; j++) html += "<td></td>";
                
                html += "</tr>";
            };
        html += "</tbody>";
        html += "</table>";
        html += "</div>";

        this.jquery_place().replaceWith(html);

        var self = this;
        $( "#"+this.control_id()+" .checkbox").checkbox({
            onChange: function() {
              self.basewidget.fire_event( self.name, 'update_control_event' );
            }
        });
    };

    ////////////////////////////////////////////////////////////////////////////////



}

    