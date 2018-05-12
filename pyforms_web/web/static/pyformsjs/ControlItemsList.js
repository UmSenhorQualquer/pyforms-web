class ControlItemsList extends ControlBase{

	constructor(name, properties){
		super(name, properties);
		this.being_edited = false;
	}

	////////////////////////////////////////////////////////////////////////////////

	init_control(){
		var html = "<div id='"+this.place_id()+"' class='field control'>";
		html += '<div class="ui divided items ControlItemsList"  id="'+this.control_id()+'">';
		html += '</div>';
		html += "</div>";
		this.jquery_place().replaceWith(html);
		this.set_value(this.properties.value);
		
		
	};

	////////////////////////////////////////////////////////////////////////////////

	get_value(){ 
		return this.properties.value;
	};

	////////////////////////////////////////////////////////////////////////////////

	set_value(data){
		html = '';
		for(var i=0; i<data.length; i++){
			var selected = this.properties.selected_index==i;

			html += '<div class="item">';
			if(data[i].img){
				html += '<div class="image">';
				html += '<img src="'+data[i].img+'">';
				html += '</div>';
			};
			html += '<div class="content">';
			if(data[i].title){
				html += '<a class="header">'+data[i].title+'</a>';
			};
			if(data[i].meta){
				html += '<div class="meta">';
				html += '<span>'+data[i].meta+'</span>';
				html += '</div>';
			}
			if(data[i].text){
				html += '<div class="description">';
				html += '<p>'+data[i].text+'</p>';
				html += '</div>';
			};

			if(data[i].tags || this.properties.select_btn_label){
				html += '<div class="extra">';
				if(this.properties.select_btn_label){
					html += '<div row-number="'+i+'" class="ui right floated primary mini button">'
					html += this.properties.select_btn_label;
					html += '</div>'
				};
				if(data[i].tags)
					for(var j=0; j<data[i].tags.length; j++)
						html += '<div class="ui label">'+data[i].tags[j]+'</div>'
				html += '</div>';
			};
			html += '</div>';
			html += '</div>';
		};
		this.jquery().html(html);

		var self = this;
		this.jquery().find('.extra .button').click(function(){
			self.properties.selected_index = $(this).attr('row-number');
			self.basewidget.fire_event( self.name, 'item_selection_changed_event' );
		});

	};

	////////////////////////////////////////////////////////////////////////////////

	update_server(){
		return true;
	};
}


