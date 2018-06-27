class ControlQueryList extends ControlBase{

	////////////////////////////////////////////////////////////////////////////////

	init_control(){

		var html = "<div id='"+this.place_id()+"' class='field control ControlQueryList'>";

		var filters = this.properties.filters_list;
		
		if( this.properties.search_field_key!=undefined ){
			html += "<div class='field'>";
			html += "<input placeholder='Search by' type='text' name='search_key' id='"+this.control_id()+"-search' />";
			html += "</div>";
		};

		// render the filters
		if(filters && filters.length>0){
			for(var j=0; j<filters.length; j+=4){
				html += "<div class='fields four'>";
				
				for(var i=0; i<4; i++){
					if( (j+i)>=filters.length ) break; 

					html += "<div class='field'>";
					html += "<label for='"+this.control_id()+"-filter-"+filters[(j+i)].column+"'>"+filters[(j+i)].label+"</label>";
					html += "<select class='ui search dropdown queryset-filter' column='"+filters[(j+i)].column+"' id='"+this.control_id()+"-filter-"+filters[(j+i)].column+"' >";
					html += "<option value='000000000000'>---</label>";
					var data = filters[(j+i)].items;
					for(var k=0; k<data.length; k++){
						html += "<option filter='"+data[k][0]+"' value='"+data[k][0]+"'>"+data[k][1]+"</label>";
					};
					html += "</select>";
					html += "</div>";
				};
				html += "</div>";
			};
		};


		html += "<table class='ui selectable celled striped table ControlQueryList "+this.properties.css+" sortable' id='"+this.control_id()+"' >";
		// render the table titles
		var titles = this.properties.horizontal_headers;
		if(titles && titles.length>0){
			html += "<thead>";
			html += "<tr>";
			for(var i=0; i<titles.length; i++) html += "<th column='"+titles[i].column+"' >"+titles[i].label+"</th>";
			html += "</tr>";
			html += "</thead>";
		};
		html += "<tbody>";
		html += "</tbody>";
		html += "</table>";
		html += "</div>";

		this.jquery_place().replaceWith(html);
		this.set_value(this.properties.value);	

		var self = this;

		if( this.properties.search_field_key!=undefined )
			$("#"+this.control_id()+"-search").keypress(function (ev) {
				var keycode = (ev.keyCode ? ev.keyCode : ev.which);
				if (keycode == '13') {
					self.properties.search_field_key = $(this).val();
					self.basewidget.fire_event( self.name, 'filter_changed_event' );
					return false;
				}
			})

		$( "#"+this.place_id()+" .queryset-filter" ).dropdown({onChange:function(value, text, selectedItem){
			self.properties.filter_by = [];

			$( "#"+self.place_id()+" .queryset-filter" ).each(function(){

				var filter_value = $(this).dropdown('get value');

				if( filter_value!='' && filter_value!='000000000000' ){
					//var key = $(this).find('select').attr('column');
					var filters = filter_value.split('&');

					for(var j=0; j<filters.length; j++){
						var cols = filters[j].split('=', 2);
						var key  = cols[0];
						var filter_value = cols[1];
						if( filter_value=='true')  filter_value = true;
						if( filter_value=='null')  filter_value = null;
						if( filter_value=='false') filter_value = false;
						var filter = { [key]: filter_value};
						self.properties.filter_by.push(filter)
					};
					
				};	
			});

			self.basewidget.fire_event( self.name, 'filter_changed_event' );
		}});
		 

		

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

			self.basewidget.fire_event( self.name, 'sort_changed_event' );
		});


		

	};

	////////////////////////////////////////////////////////////////////////////////

	get_value(){
		return undefined;
	};


	////////////////////////////////////////////////////////////////////////////////

	set_value(value){
		
		var titles = this.properties.horizontal_headers;
		var data   = this.properties.values;

		if(this.properties.search_field_key==null)
			$("#"+this.place_id()+"-search").val('');
		else
			$("#"+this.place_id()+"-search").val(this.properties.search_field_key);
		
		var rows_html = '';
		for(var i=0; i<data.length; i++){
			var selected = this.properties.selected_row_id==data[i][0];
			rows_html += "<tr row-id='"+data[i][0]+"' >";
			for(var j=1; j<data[i].length; j++)
				rows_html += "<td class='"+(selected?'active':'')+"' >"+(data[i][j]?data[i][j]:'')+"</td>";
			rows_html += "</tr>";
		};
		$( "#"+this.control_id()+" tbody" ).html(rows_html);
		$( "#"+this.control_id()+" tfoot" ).remove();

		var titles = this.properties.horizontal_headers;
		
		var html 		= '';
		var pages_list 	= this.properties.pages.pages_list;
		if(pages_list.length>1){
			html += '<tfoot>';
			html += '<tr>';
			html += '<th colspan="'+(titles?titles.length:1)+'">';
			//html += '<div class="ui left floated pagination menu tiny">';

			html += '<a class="ui pointing basic label">'+this.properties.values_total+' results</a> ';
			//html += '</div>';
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
				self.properties.selected_row_id = $(this).parent().attr('row-id');
				self.basewidget.fire_event( self.name, 'item_selection_changed_client_event' );
			}
		});

		$("#"+this.control_id()+" .pagination .item" ).click(function(){
			if( !$(this).hasClass('active') ){
				self.properties.pages.current_page = $(this).attr('pageindex');
				self.basewidget.fire_event( self.name, 'page_changed_event' );
			}
		});
		
	};
}