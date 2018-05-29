class ControlCheckBoxListQuery extends ControlCheckBoxList{

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
        html += "<tr><th></th>";
        var titles = this.properties.headers;
        for(var i=0; i<titles.length; i++) html += "<th>"+titles[i]+"</th>";
        html += "</tr>";
        html += "</thead>";
        html += "<tbody>";
        var data = this.properties.value;
        
        var header_length = (titles.length+1);

        if(data!=undefined)
            for(var i=0; i<data.length; i++){
                html += "<tr>";
                html += "<td class='collapsing' >";
                html += "<div class='ui fitted " +(data[i][0]?"active":"")+" checkbox'>";
                html += "<input type='checkbox' "+(data[i][0]?"checked=''":"")+" />";
                html += "<label></label></div>";
                html += "</td>";
                
                var length = data[i]?data[i].length:0;
                length     = length>header_length?header_length:length;
                for(var j=1; j<length; j++) 
                    html += "<td>"+data[i][j]+"</td>";
                if(length<header_length) 
                    for(var j=length; j<header_length; j++)
                        html += "<td></td>";
                
                html += "</tr>";
            };
        
        if(this.properties.remove_button || this.properties.add_button){
            html += '<tfoot>';
            html += '<tr>';
            html += '<th colspan="'+header_length+'">';
            if(this.properties.add_button)
                html += '<div class="ui small button add-btn" >Add</div>';
            if(this.properties.remove_button)
                html += '<div class="ui small button remove-btn" >Remove</div>';
            html += '</th>';
            html += '</tr>';
            html += '</tfoot>';
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

        if(this.properties.remove_button)
            $( "#"+this.control_id()+" .remove-btn").click(function(){
                self.basewidget.fire_event( self.name, 'remove_event' );
            });

        if(this.properties.add_button)
            $( "#"+this.control_id()+" .add-btn").click(function(){
                self.basewidget.fire_event( self.name, 'add_event' );
            });
    };

    ////////////////////////////////////////////////////////////////////////////////



}

    