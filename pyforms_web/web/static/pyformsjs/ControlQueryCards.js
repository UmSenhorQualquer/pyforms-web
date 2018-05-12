class ControlQueryCards extends ControlBase{


	////////////////////////////////////////////////////////////////////////////////

	init_control(){
		var html = "<div id='"+this.place_id()+"' class='field control'>";

		var filters = this.properties.filters_list;
		
		// render the filters
		if(filters.length>0){
			html += "<div class='fields'>";
			for(var i=0; i<filters.length; i++){
				html += "<div class='field'>";
				html += "<label for='"+this.control_id()+"-filter-"+filters[i].column+"'>"+filters[i].label+"</label>";
				html += "<select class='ui search dropdown queryset-filter' column='"+filters[i].column+"' id='"+this.control_id()+"-filter-"+filters[i].column+"' >";
				html += "<option value='000000000000'>--- None ---</label>";
				var data = filters[i].items;
				for(var j=0; j<data.length; j++){
					html += "<option value='"+data[j]+"'>"+data[j]+"</label>";
				};
				html += "</select>";
				html += "</div>";
			};
			html += "</div>";
		};


		html += "<div class='ui link cards' id='"+this.control_id()+"' ></div>";
		
		this.jquery_place().replaceWith(html);
		this.set_value(this.properties.value);	

		var self = this;

		$( "#"+this.place_id()+" .queryset-filter" ).dropdown({onChange:function(){
			self.properties.filter_by = [];

			$( "#"+self.place_id()+" .queryset-filter" ).each(function(){
				var filter_value = $(this).dropdown('get value');
				if( filter_value!='' && filter_value!='000000000000' ){
					var key = $(this).find('select').attr('column');
					var filter = { [key]: filter_value};
					self.properties.filter_by.push(filter)
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
		
		var rows_html = '';
		for(var i=0; i<data.length; i++){
			var selected = this.properties.selected_row_id==data[i][0];
			rows_html += "<div class='card' row-id='"+data[i][0]+"' >";
			for(var j=1; j<data[i].length; j++) 
				rows_html += "<div class='content "+(selected?'active':'')+"' >"+data[i][j]+"</div>";
			rows_html += "</div>";
		};
		$( "#"+this.control_id() ).html( rows_html);

		var html 		= '';
		var pages_list 	= this.properties.pages.pages_list;
		if(pages_list.length>1){
			html += '<div class="ui right floated pagination menu small">';
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
			
			$( "#"+this.control_id() ).append(html);
		};
		
		this.set_click_events();

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