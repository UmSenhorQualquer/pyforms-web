class ControlList extends ControlBase{

	constructor(name, properties){
		super(name, properties);
		this.being_edited = false;
	}

	////////////////////////////////////////////////////////////////////////////////

	init_control(){
		this.set_value(this.properties.value);
		

		if(this.properties.required) this.set_required();
	};

	////////////////////////////////////////////////////////////////////////////////

	get_value(){ 
		var res=[];
		$( "#"+this.control_id()+" tbody tr" ).each(function(i, row){
			var new_row=[]
			$(this).children('td').each(function(j, col){
				new_row.push($(col).html());
			});
			res.push(new_row);
		});
		return res
	};


	////////////////////////////////////////////////////////////////////////////////

	set_value(value){
		this.load_table();
	};

	////////////////////////////////////////////////////////////////////////////////

	load_table(){
		var html = "<div id='"+this.place_id()+"' class='field control'>";
		if(this.properties.label_visible) html += "<label for='"+this.control_id()+"'>&nbsp;</label>";
		html += "<div style='overflow-x: auto;' ><table class='ui selectable celled table "+this.properties.css+" ControlList' id='"+this.control_id()+"' >";
		
		// GENERATE THE HEADER
		html += "<thead>";
		html += "<tr>";
		var colsalign = this.properties.columns_align;
		var colssizes = this.properties.columns_size;
		var titles 	  = this.properties.horizontal_headers;
		for(var i=0; i<titles.length; i++){
			html += `<th style='${(colssizes)?`width:${colssizes[i]}`:''}; ${(colsalign)?`text-align:${colsalign[i]}`:''}' >${titles[i]}</th>`;
		};
		html += "</tr>";
		html += "</thead>";
		// END GENERATE THE HEADER

		var data = this.properties.value;
		
		html += "<tbody></div>";
		if(data!=undefined)
			for(var i=0; i<data.length; i++){
				var selected = this.properties.selected_index==i;

				html += selected?"<tr>":"<tr>";
				var length = 0;
				if(data[i]) length = data[i].length;
				for(var j=0; j<length; j++)
					html += selected?`<td style='${(colsalign)?`text-align:${colsalign[j]}`:''}' class='active' >${data[i][j]}</td>`:`<td style='${(colsalign)?`text-align:${colsalign[j]}`:''}' >${data[i][j]}</td>`;
				
				if(length<titles.length) 
					for(var j=length; j<titles.length; j++) 
						html += selected?"<td class='active' ></td>":"<td></td>";
				html += "</tr>";
			};
		html += "</tbody>";
		html += "</table>";
		html += "</div>";

		this.jquery_place().replaceWith(html);

		var self = this;
			
		if(!this.properties.read_only){
			$( "#"+this.control_id()+" tbody td" ).dblclick(function(){
				if( self.being_edited ) return false;

				self.being_edited = true;
				var cell = $(this);
				var value = cell.html();
				cell.html('<div class="ui input"><input type="text" value="'+value+'" /></div>');
				cell.find('input').focus();
				cell.find('input').focusout(function(){
					cell.html($(this).val());
					self.being_edited = false;
					self.basewidget.fire_event( self.name, 'update_control_event' );
				});
			});
		}else{
			$("#"+this.control_id()+" tbody td" ).dblclick(function(){
				self.basewidget.fire_event( self.name, 'row_double_click_event' );
			});
		};

		$("#"+this.control_id()+" tbody td" ).click(function(){
			if( !$(this).hasClass('active') ){
				$("#"+self.control_id()+" tbody td" ).removeClass('active');
				$("#"+self.control_id()+" tbody tr" ).removeClass('active');			

				if( self.properties.select_entire_row )
					$(this).parent().find('td').addClass('active');
				else
					$(this).addClass('active');

				self.properties.selected_index = $("#"+self.control_id()+" tbody tr" ).index($(this).parent());

				self.basewidget.fire_event( self.name, 'item_selection_changed_event' );
			}
		});

		// remove the selection if the header is selected
		$("#"+this.control_id()+" thead th" ).click(function(){
			$("#"+self.control_id()+" tbody td" ).removeClass('active');
			$("#"+self.control_id()+" tbody tr" ).removeClass('active');
			self.properties.selected_index = -1;
			self.basewidget.fire_event( self.name, 'item_selection_changed_event' );
		});
		
	};

	////////////////////////////////////////////////////////////////////////////////



}

	