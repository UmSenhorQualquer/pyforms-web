class ControlQueryList extends ControlBase{

    /**
    Build the filters html
    @param {list(object)} filters - List of filters objects to build.
    @returns {string}
    */
    build_filters_html(filters){

        var html = '';

        for(var j=0; j<filters.length; j+=4){

            html += "<div class='fields four'>";
            for(var i=0; i<4; i++){
                if( (j+i)>=filters.length ) break; 

                

                var filter = filters[(j+i)];

                switch(filter.field_type) {
                    case "combo":
                        html += "<div class='field'>";
                        html += "<label for='"+this.control_id()+"-filter-"+filter.column+"'>"+filter.label+"</label>";
                        html += "<select class='ui search dropdown queryset-filter' column='"+filter.column+"' id='"+this.control_id()+"-filter-"+filter.column+"' >";
                        html += "<option value='000000000000'>---</label>";
                        var data = filter.items;
                        for(var k=0; k<data.length; k++)
                            html += "<option filter='"+data[k][0]+"' value='"+data[k][0]+"'>"+data[k][1]+"</label>";
                        html += "</select>";
                        html += "</div>";
                        break;
                    case "date-range":
                        html += `<div class='field date-filter' id='${this.control_id()}-filter-${filter.column}' >`;
                
                        html += `<label>${filter.label}</label>`;

                        html += `
                            <div class="ui basic button choose"><i class="icon calendar"></i>Choose range <span></span></div>
                            <div class='circular ui button icon basic mini clear' col='${filter.column}' style='display:none' ><i class="remove icon"></i></div>
                            <div class="ui flowing popup bottom left transition hidden">
                              <div class="ui three column center aligned grid">
                                <div class="column">
                                    <div class="ui icon input" style='width:150px;' >
                                        <input type="text" name="begin" class="begin" placeholder="Start date">
                                        <i class="calendar icon"></i>
                                    </div>
                                </div>
                                <div class="column">
                                    <div class="ui icon input" style='width:150px;' >
                                        <input type="text" name="end" class="end" placeholder="End date">
                                        <i class="calendar icon"></i>
                                    </div>
                                </div>
                                <div class="column" style='width:140px;' >
                                  <div class='ui button blue apply' col='${filter.column}' ><i class="filter icon"></i>Apply</div>
                                </div>
                              </div>
                            </div>
                        `;
                        html += "</div>";
                        break;
                }
            };

            html += "</div>";
        };

        return html;
    }

    init_date_filters_events(filters){

        var self = this;

        for(var i=0; i<filters.length; i++){
            
            var filter = filters[i];

            if(filter.field_type=='date-range'){
                
                // set popup
                $(`#${this.control_id()}-filter-${filter.column} .button.choose`).popup({
                    on: 'click',
                    popup: `#${this.control_id()}-filter-${filter.column} .popup`
                });

                // set datetime pickers
                $(`#${this.control_id()}-filter-${filter.column} input`).datepicker({
                    dateFormat: "yy-mm-dd", 
                    changeMonth: true,
                    changeYear: true,
                    yearRange: "1900:3000"
                });

                // set apply button
                $(`#${this.control_id()}-filter-${filter.column} .button.apply`).click(function(){
                    var column = $(this).attr('col');
                    var choose_button = $(`#${self.control_id()}-filter-${column} .button.choose`);
                    choose_button.popup('hide');

                    var begin = $(`#${self.control_id()}-filter-${column} .begin`).val();
                    var end   = $(`#${self.control_id()}-filter-${column} .end`).val();
                    
                    var filter_value = '';
                    if( begin || end ){
                        filter_value += begin?`[${begin};`:'[;';
                        filter_value += end?`${end}]`:']';

                        $(`#${self.control_id()}-filter-${column} .button.clear`).show();
                    }else
                        $(`#${self.control_id()}-filter-${column} .button.clear`).hide();

                    choose_button.children('span').html(filter_value);
                    
                    self.collect_filters_values();
                    self.update_server_flag = true;
                    self.basewidget.fire_event( self.name, 'filter_changed_event' );
                });

                // clear button
                $(`#${this.control_id()}-filter-${filter.column} .button.clear`).click(function(){
                    var column = $(this).attr('col');
                    $(`#${self.control_id()}-filter-${column} .begin`).val('');
                    $(`#${self.control_id()}-filter-${column} .end`).val('');
                    $(`#${self.control_id()}-filter-${column} .button.choose span`).html('');
                    $(this).hide();

                    self.collect_filters_values();
                    self.update_server_flag = true;
                    self.basewidget.fire_event( self.name, 'filter_changed_event' );
                });
            }
        }
    }

    pad(number, size){
        var s = String(number);
        while (s.length < (size || 2)) {s = "0" + s;}
        return s;
    }

    formatdate(date){
        return date.getFullYear()+'-'+this.pad(date.getMonth()+1,2)+'-'+this.pad(date.getDate(),2);
    }

    collect_filters_values(){
        var filters = this.properties.filters_list;
        this.properties.filter_by = [];

        for(var i=0; i<filters.length; i++){
            var filter = filters[i];

            switch(filter.field_type) {
                case "combo":
                    var filter_value = $(`#${this.control_id()}-filter-${filter.column}`).dropdown('get value');
                    break;
                case "date-range":
                    var begin = $(`#${this.control_id()}-filter-${filter.column} .begin`).val();
                    var end   = $(`#${this.control_id()}-filter-${filter.column} .end`).val();
                    var filter_value = begin?`${filter.column}__gte=${begin}`:'';
                    filter_value += (begin && end)?`&`:'';

                    if( end ){
                        end = new Date(end);
                        end.setDate( end.getDate()+1 );
                    }else{
                        end = undefined;
                    }

                    filter_value += end?`${filter.column}__lte=${this.formatdate(end)}`:'';
                    break;
            }

            if( filter_value!='' && filter_value!='000000000000' ){
                var fs = filter_value.split('&');
                for(var j=0; j<fs.length; j++){
                    var cols = fs[j].split('=', 2);
                    var key  = cols[0];
                    var filter_value = cols[1];
                    if( filter_value=='true')  filter_value = true;
                    if( filter_value=='null')  filter_value = null;
                    if( filter_value=='false') filter_value = false;
                    var filter = { [key]: filter_value};
                    this.properties.filter_by.push(filter)
                };
            };  
        }

    }

    ////////////////////////////////////////////////////////////////////////////////

    init_control(){
        this.update_server_flag = false;

        var html = "<div id='"+this.place_id()+"' class='field control ControlQueryList'>";

        var filters = this.properties.filters_list;
        
        if( this.properties.search_field_key!=undefined ){
            html += "<div class='field'>";
            html += "<input placeholder='Search by' type='text' name='search_key' id='"+this.control_id()+"-search' />";
            html += "</div>";
        };

        // render the filters ###############################################
        if(filters && filters.length>0)
            html += this.build_filters_html(filters)
        // End render the filters ###############################################


        html += "<div style='overflow-x: auto;' ><table class='ui selectable celled striped table ControlQueryList "+this.properties.css+" sortable' id='"+this.control_id()+"' >";
        // render the table titles
        var colsalign = this.properties.columns_align;
        var colssizes = this.properties.columns_size;
        var titles    = this.properties.horizontal_headers;
        if(titles && titles.length>0){
            html += "<thead>";
            html += "<tr>";
            for(var i=0; i<titles.length; i++) 
                html += `<th style='${(colssizes)?`width:${colssizes[i]}`:''}; ${(colsalign)?`text-align:${colsalign[i]}`:''}' column='${titles[i].column}' >${titles[i].label}</th>`;
            html += "</tr>";
            html += "</thead>";
        };
        html += "<tbody>";
        html += "</tbody>";
        html += "</table></div>";
        html += "</div>";

        this.jquery_place().replaceWith(html);
        this.set_value(this.properties.value);  

        var self = this;

        //set dates ranges events ///////////////////////
        if(filters && filters.length>0)
            this.init_date_filters_events(filters);
        /////////////////////////////////////////////////

        if( this.properties.search_field_key!=undefined )
            $("#"+this.control_id()+"-search").keypress(function (ev) {
                var keycode = (ev.keyCode ? ev.keyCode : ev.which);
                if (keycode == '13') {
                    self.update_server_flag = true;
                    self.properties.search_field_key = $(this).val();
                    self.basewidget.fire_event( self.name, 'filter_changed_event' );
                    return false;
                }
            })

        $( "#"+this.place_id()+" .queryset-filter" ).dropdown({
            onChange: function(value, text, selectedItem){
                self.collect_filters_values();
                self.update_server_flag = true;

                self.basewidget.fire_event( self.name, 'filter_changed_event' );
            },
            fullTextSearch: 'exact',
            match: 'text'
        });
         

        

        // remove the selection if the header is selected
        var self = this;
        $("#"+this.control_id()+" thead th" ).click(function(){
            $("#"+self.control_id()+" tbody td" ).removeClass('active');
            $("#"+self.control_id()+" tbody tr" ).removeClass('active');
            self.properties.selected_index = -1;
            
            if( $(this).hasClass('ascending') ){
                $(this).removeClass('ascending');
                $(this).addClass('descending');
            }else
                if( $(this).hasClass('descending') ){
                    $(this).removeClass('sorted');
                    $(this).removeClass('descending');
                }else{
                    $(this).addClass('sorted');
                    $(this).addClass('ascending');
                };

            self.properties.sort_by = [];
            $("#"+self.control_id()+" thead th" ).each(function(index){         
                if( $(this).hasClass('ascending') || $(this).hasClass('descending') ){
                    var sort_query = { column: $(this).attr('column'), desc: $(this).hasClass('descending') };
                    self.properties.sort_by.push(sort_query);
                };          
            });


            self.update_server_flag = true;
            self.basewidget.fire_event( self.name, 'sort_changed_event' );
        });
		if(this.properties.required) this.set_required();


        

    };

    ////////////////////////////////////////////////////////////////////////////////

    get_value(){
        return undefined;
    };


    ////////////////////////////////////////////////////////////////////////////////

    set_value(value){
        var titles = this.properties.horizontal_headers;
        var data   = value;

        if(this.properties.search_field_key==null)
            $("#"+this.place_id()+"-search").val('');
        else
            $("#"+this.place_id()+"-search").val(this.properties.search_field_key);
        
        var rows_html = '';
        var colsalign = this.properties.columns_align;
        for(var i=0; i<data.length; i++){
            var selected = this.properties.selected_row_id==data[i][0];
            rows_html += "<tr row-id='"+data[i][0]+"' >";
            for(var j=1; j<data[i].length; j++)
                rows_html += `<td style='${(colsalign)?`text-align:${colsalign[j-1]}`:''}' class='${(selected?'active':'')}' >${(data[i][j]?data[i][j]:'')}</td>`;
            rows_html += "</tr>";
        };
        $( "#"+this.control_id()+" tbody" ).html(rows_html);
        $( "#"+this.control_id()+" tfoot" ).remove();

        var titles = this.properties.horizontal_headers;
        
        var html        = '';
        var pages_list  = this.properties.pages.pages_list;
        if(pages_list.length>1){
            html += '<tfoot>';
            html += '<tr>';
            html += '<th colspan="'+(titles?titles.length:1)+'">';

            html += '<a class="ui pointing basic label">'+this.properties.values_total+' results</a> ';
            
            if( this.properties.export_csv )
                html += '<a class="ui button mini basic export-csv-btn "> <i class="ui icon cloud download"></i> CSV</a> ';
            
            html += '<div class="ui right floated pagination menu tiny">';

            var start_page = 0;
            var end_page = (pages_list.length-1)>5?(pages_list.length-1):pages_list.length;
                if( pages_list[0]>0 )
                    html += '<a class="icon item" pageindex="'+pages_list[0]+'" ><i class="left chevron icon"></i></a>';            
                for(var i=1; i<(pages_list.length-1); i++){
                    html += '<a pageindex="'+pages_list[i]+'" class="item '+((pages_list[i]==this.properties.pages.current_page)?'active':'')+'">'+pages_list[i]+'</a>';            
                };      
                if( pages_list[pages_list.length-1]>0 ) 
                    html += '<a pageindex="'+pages_list[pages_list.length-1]+'" class="icon item"><i class="right chevron icon"></i></a>';
            html += '</div>';

            html += '</th>';
            html += '</tr>';
            html += '</tfoot>';

            $( "#"+this.control_id()+" tbody ").after(html);
        };
        
        this.set_click_events();

    };

    ////////////////////////////////////////////////////////////////////////////////



    set_label(value){
        //The list has no label
    };


    ////////////////////////////////////////////////////////////////////////////////

    set_click_events(){
        var self = this;

        $("#"+this.control_id()+" tbody td" ).click(function(){
            if( !$(this).hasClass('active') ){
                var new_id = $(this).parent().attr('row-id');
                self.update_server_flag = new_id!=self.properties.selected_row_id;
                self.properties.selected_row_id = new_id;
                //self.jquery().children('td').removeClass('active');
                //self.jquery().children('tr[row-id='+self.properties.selected_row_id+'] td').addClass('active');
                self.basewidget.fire_event( self.name, 'item_selection_changed_client_event' );
            }
        });

        $("#"+this.control_id()+" .pagination .item" ).click(function(){
            if( !$(this).hasClass('active') ){
                self.update_server_flag = true;
                self.properties.pages.current_page = $(this).attr('pageindex');
                self.basewidget.fire_event( self.name, 'page_changed_event' );
            }
        });

        $("#"+this.control_id()+" .export-csv-btn" ).click(function(){
            self.basewidget.fire_event( self.name, 'export_csv_event' );
        });
        
    };

    update_server(){
        return this.update_server_flag;
    }

    serialize(){
        var data = super.serialize();
        this.update_server_flag = false;
        return data;
    }
}