

function ControlQueryList(name, properties){
	ControlBase.call(this, name, properties);
	this.being_edited = false;
};
ControlQueryList.prototype = Object.create(ControlBase.prototype);

////////////////////////////////////////////////////////////////////////////////

ControlQueryList.prototype.init_control = function(){
	this.load_table();
	if(!this.properties.visible) this.hide();
};

////////////////////////////////////////////////////////////////////////////////

ControlQueryList.prototype.get_value = function(){ 
	return undefined;
};


////////////////////////////////////////////////////////////////////////////////

ControlQueryList.prototype.set_value = function(value){
	var html = '';
	var titles = this.properties.horizontal_headers;
	var data = this.properties.values;
	for(var i=0; i<data.length; i++){
		var selected = this.properties.selected_index==i;
		html += selected?"<tr>":"<tr>";
		var length = 0;
		if(data[i]) length = data[i].length;
		for(var j=0; j<length; j++) 
			html += selected?"<td class='active' >"+data[i][j]+"</td>":"<td>"+data[i][j]+"</td>";
		if(length<titles.length) 
			for(var j=length; j<titles.length; j++) 
				html += selected?"<td class='active' ></td>":"<td></td>";
		html += "</tr>";
	};

	$( "#"+this.control_id()+" tbody" ).html(html);
	this.set_click_events();

	if(this.properties.visible) 
		this.show();
	else 
		this.hide();
};

////////////////////////////////////////////////////////////////////////////////

ControlQueryList.prototype.load_table = function(){
	var html = "<div id='"+this.place_id()+"' class='field'>";

	html += "<div class='fields'>";
	var filters = this.properties.filters_list;
	for(var i=0; i<filters.length; i++){
		html += "<div class='field'>";
		html += "<label for='"+this.control_id()+"-filter-"+filters[i].column+"'>"+filters[i].label+"</label>";
		html += "<select class='ui search dropdown' id='"+this.control_id()+"-filter-"+filters[i].column+"' >";
		html += "<option value=''></label>";
		var data = filters[i].items;
		for(var i=0; i<data.length; i++){
			html += "<option value='"+data[i].key+"'>"+data[i].label+"</label>";
		};
		html += "</select>";
		html += "</div>";
	};

	html += "<div class='field'>";
	html += "<label for='"+this.control_id()+"-order-by'>Order by</label>";
	html += "<select class='ui search dropdown' id='"+this.control_id()+"-order-by' multiple='' >";
	var data = this.properties.orderby_items;
	for(var i=0; i<data.length; i++){
		html += "<option value='"+data[i].value+"'>"+data[i].label+"</label>";
	};
	html += "</select>";
	html += "</div>";

	html += "</div>";


	html += "<table class='ui selectable celled table gray inverted ControlQueryList' id='"+this.control_id()+"' >";
	html += "<thead>";
	html += "<tr>";
	var titles = this.properties.horizontal_headers;
	for(var i=0; i<titles.length; i++) html += "<th>"+titles[i]+"</th>";
	html += "</tr>";
	html += "</thead>";
	html += "<tbody>";
	var data = this.properties.values;
	
	for(var i=0; i<data.length; i++){
		var selected = this.properties.selected_index==i;

		html += selected?"<tr>":"<tr>";
		var length = 0;
		if(data[i]) length = data[i].length;
		for(var j=0; j<length; j++) 
			html += selected?"<td class='active' >"+data[i][j]+"</td>":"<td>"+data[i][j]+"</td>";
		if(length<titles.length) 
			for(var j=length; j<titles.length; j++) 
				html += selected?"<td class='active' ></td>":"<td></td>";
		html += "</tr>";
	};
	html += "</tbody>";


	html += '<tfoot>';
	html += '<tr>';
	html += '<th colspan="3">';
	html += '<div class="ui right floated pagination menu">';
		html += '<a class="icon item">';
			html += '<i class="left chevron icon"></i>';
			html += '</a>';
			html += '<a class="item">1</a>';
			html += '<a class="item">2</a>';
			html += '<a class="item">3</a>';
			html += '<a class="item">4</a>';
			html += '<a class="icon item">';
			html += '<i class="right chevron icon"></i>';
			html += '</a>';
	html += '</div>';
	html += '</th>';
	html += '</tr>';
	html += '</tfoot>';

	html += "</table>";
	html += "</div>";

	this.jquery_place().replaceWith(html);
	$( "#"+this.control_id()+"-order-by" ).dropdown({forceSelection:false});

	this.set_click_events();

	// remove the selection if the header is selected
	var self = this;
	$("#"+this.control_id()+" thead th" ).click(function(){
		$("#"+self.control_id()+" tbody td" ).removeClass('active');
		$("#"+self.control_id()+" tbody tr" ).removeClass('active');
		self.properties.selected_index = -1;
		self.basewidget.fire_event( self.name, 'item_selection_changed_event' );
	});
	
};

////////////////////////////////////////////////////////////////////////////////


ControlQueryList.prototype.set_click_events = function(){
	var self = this;

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
};