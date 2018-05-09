var COLUMNS_CSS_CLASSES = ['','one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve','thirteen','fourteen','fiveteen','sixteen','seventeen','eighteen','nineteen','twenty','twentyone','twentytwo'];

class ControlBase{

	constructor(name, properties){
		var self = this;
		this.name 			= name;
		this.properties 	= properties;
		this.basewidget 	= undefined; //Will be set in runtime by the parent BaseWidget object.
	}

	////////////////////////////////////////////////////////////////////////////////

	app_id(){ 
		return this.basewidget.widget_id; 
	}

	////////////////////////////////////////////////////////////////////////////////

	control_id(){ 
		return this.basewidget.control_id(this.name); 
	}

	////////////////////////////////////////////////////////////////////////////////

	jquery(){ 
		return $("#"+this.control_id()); 
	}

	////////////////////////////////////////////////////////////////////////////////

	place_id(){ 
		return "place-"+this.control_id(); 
	}

	////////////////////////////////////////////////////////////////////////////////

	jquery_place(){ 
		return $( "#"+this.place_id() ); 
	}

	////////////////////////////////////////////////////////////////////////////////

	get_value(){ 
		if(this.jquery().length==0) return this.properties.value;
		var value = this.jquery().val();
		if(value=='null') return null;
		else return value;
	}

	////////////////////////////////////////////////////////////////////////////////

	set_value(value){
		if(this.jquery().length>0) 
			if(this.properties.value!=null)
				this.jquery().val(this.properties.value); 
			else
				this.jquery().val(''); 
	}

	////////////////////////////////////////////////////////////////////////////////

	set_label(value){
		$( "#"+this.place_id()+' label' ).first().html(value);
	}

	////////////////////////////////////////////////////////////////////////////////

	count_visible( selector ){
		var visible = 0;  
		selector.each(function(i,e){  
			if( $(e).css('display')!='none') visible += 1;  
		});  
		return visible
	}

	////////////////////////////////////////////////////////////////////////////////
	
	enable(){
		this.jquery().removeAttr('disabled');
	}

	////////////////////////////////////////////////////////////////////////////////
	
	disable(){
		this.jquery().attr('disabled', 'true');
	}

	////////////////////////////////////////////////////////////////////////////////

	hide(not_update_columns, init_form){
		
		// if the control is already hidden leave the function
		if(init_form==undefined)
			if( !this.jquery_place().is(':visible') ) return;

		this.jquery_place().hide();
		this.properties.visible = false;

		// check if the parent is fields
		var parent = this.jquery_place().parent();

		if( parent.hasClass('row') && parent.hasClass('fields') )
		{	
			// if the row has more than one element, reduce the number
			if( !parent.hasClass( 'no-alignment') )
				for(var i=2; i<COLUMNS_CSS_CLASSES.length; i++){
					if( parent.hasClass( COLUMNS_CSS_CLASSES[i] ) ){
						parent.removeClass( COLUMNS_CSS_CLASSES[i] );
						parent.addClass( COLUMNS_CSS_CLASSES[i-1] );
						break;
					};
				}
			
			// no visible element inside the row, then hide it
			if( this.count_visible( parent.find('.control') )==0 )
				parent.hide();	
		}

		var pyforms_segment = this.jquery_place().parents('.pyforms-segment');
	    if( this.count_visible( pyforms_segment.find('.control') )==0 ) 
	    	pyforms_segment.hide(); 
	};

	////////////////////////////////////////////////////////////////////////////////

	show(init_form){
		//if( this.jquery_place().is(':visible') ) return;
		
		this.jquery_place().show();
		this.properties.visible = true;

		var parent = this.jquery_place().parent();
		
		if( parent.hasClass('row') )
		
			if( parent.hasClass('fields') && !parent.hasClass( 'no-alignment') ){
				if(init_form!=true)
					for(var i=0; i<COLUMNS_CSS_CLASSES.length-1; i++)
						if( parent.hasClass( COLUMNS_CSS_CLASSES[i] ) ){
							parent.removeClass( COLUMNS_CSS_CLASSES[i] );
							parent.addClass( COLUMNS_CSS_CLASSES[i+1] );
							break;
						};
			}else 
			 	parent.css('display', '');
					
		

		var pyforms_segment = this.jquery_place().parents('.pyforms-segment');
		if( pyforms_segment ) pyforms_segment.show();
	};

	////////////////////////////////////////////////////////////////////////////////

	deserialize(data){
		$.extend(this.properties, data);
		this.set_value(this.properties.value);
		this.set_label(this.properties.label);

		if(this.properties.error) this.jquery_place().addClass('error'); else this.jquery_place().removeClass('error');
	}

	////////////////////////////////////////////////////////////////////////////////

	serialize(){
		this.properties.value = this.get_value();
		return this.properties; 
	}

	////////////////////////////////////////////////////////////////////////////////

	init_control(){
		
		if(this.properties.error) this.jquery_place().addClass('error'); else this.jquery_place().removeClass('error');
		if(this.properties.css) this.jquery().addClass(this.properties.css);
	}

	////////////////////////////////////////////////////////////////////////////////

	update_server(){
		return this.get_value()!=this.properties.value
	}


}
