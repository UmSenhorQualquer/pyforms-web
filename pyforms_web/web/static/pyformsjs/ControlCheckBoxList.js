class ControlCheckBoxList extends ControlBase{

    constructor(name, properties){
        super(name, properties);
        this.being_edited = false;
        this.update_server_flag = false;
    }

    ////////////////////////////////////////////////////////////////////////////////

    init_control(){
        this.set_value(this.properties.value);
		if(this.properties.required) this.set_required();

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
        this.set_click_events()
    };

    ////////////////////////////////////////////////////////////////////////////////

    load_table(){
        var html = "<div id='"+this.place_id()+"' class='field control'>";

        if(this.properties.label_visible)
            html += `<label for="${this.control_id()}">${this.properties.label}</label>`;
        html += "<table class='ui selectable celled table "+this.properties.css+" ControlCheckBoxList' id='"+this.control_id()+"' >";
        html += "<thead>";
        html += "<tr>";
        var titles = this.properties.headers;
        var columns_styles = this.properties.columns_styles;
        for(var i=0; i<titles.length; i++)
            html += `<th ${(columns_styles)?`style='${columns_styles[i]}'`:''} >${titles[i]}</th>`;
        html += "</tr>";
        html += "</thead>";
        html += "<tbody>";
        var data = this.properties.value;


        if(data!=undefined)
            for(var i=0; i<data.length; i++){

                const selected = this.properties.selected_index == i;

                html += `<tr row-id="${i}" >`;
                html += `<td class='collapsing ${(selected?'active':'')}' >`;
                html += "<div class='ui fitted "+(data[i][0]?"active":"")+" checkbox'>";
                html += "<input type='checkbox' "+(data[i][0]?"checked=''":"")+" />";
                html += "<label></label></div>";
                html += "</td>";

                var length = data[i]?data[i].length:0;
                length     = length>titles.length?titles.length:length;
                for(var j=1; j<length; j++) html += `<td class='${(selected?'active':'')}' >`+data[i][j]+"</td>";
                if(length<titles.length)
                    for(var j=length; j<titles.length; j++) html += `<td class='${(selected?'active':'')}'></td>`;

                html += "</tr>";
            };
        html += "</tbody>";
        html += "</table>";
        html += "</div>";

        this.jquery_place().replaceWith(html);

        this.changed = false;
        var self = this;
        $( "#"+this.control_id()+" .checkbox").checkbox({
            onChange: function() {
                self.changed = true;
              self.basewidget.fire_event( self.name, 'update_control_event' );
            }
        });
    };

    set_click_events(){
        var self = this;

        $("#"+this.control_id()+" tbody td" ).click(function(){

            if( !$(this).hasClass('active') ){
                var new_id = $(this).parent().attr('row-id');

                self.update_server_flag = new_id!=self.properties.selected_index;
                self.properties.selected_index = new_id;
                self.basewidget.fire_event( self.name, 'item_selection_changed_client_event' );
            }
        });

    };



    ////////////////////////////////////////////////////////////////////////////////

    update_server(){
        return this.changed || this.update_server_flag;
    }

    serialize(){
        var data = super.serialize();
        this.update_server_flag = false;
        return data;
    }


    ////////////////////////////////////////////////////////////////////////////////

    /**
    Enable the control.
    */
    enable(){
        this.jquery().find('tr').removeAttr('disabled');
        this.jquery().find('tr').removeClass('disabled');
    }

    ////////////////////////////////////////////////////////////////////////////////

    /**
    Disable the control.
    */
    disable(){
        this.jquery().find('tr').attr('disabled', 'true');
        this.jquery().find('tr').addClass('disabled');
    }

}

