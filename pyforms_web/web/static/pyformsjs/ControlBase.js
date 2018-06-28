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
		this.jquery().removeClass('disabled');
	}

	////////////////////////////////////////////////////////////////////////////////
	
	disable(){
		this.jquery().attr('disabled', 'true');
		this.jquery().addClass('disabled');
	}

	////////////////////////////////////////////////////////////////////////////////

	hide(){
		if( this.count_visible( this.jquery_place() )==0 ) return;
		
		this.jquery_place().hide();
		this.properties.visible = false;

		// check if the parent is fields
		var parent = this.jquery_place().parent();

		if( parent.hasClass('row') && parent.hasClass('fields') )
		{	
			// if the row has more than one element, reduce the number
			if( !parent.hasClass( 'no-alignment') )
				for(var i=COLUMNS_CSS_CLASSES.length; i>1; i--){
					if( parent.hasClass( COLUMNS_CSS_CLASSES[i] ) ){
						parent.removeClass( COLUMNS_CSS_CLASSES[i] );
						parent.addClass( COLUMNS_CSS_CLASSES[i-1] );
						//parent.removeClass('fields');
						break;
					};
				}
			
			// no visible element inside the row, then hide it
			if( this.count_visible( parent.find('.control') )==0 ){
				parent.hide();	
				for(var i=0; i<COLUMNS_CSS_CLASSES.length-1; i++)
					parent.removeClass( COLUMNS_CSS_CLASSES[i] );
			}
		}

		var pyforms_segment = this.jquery_place().parents('.pyforms-segment');
	    if( this.count_visible( pyforms_segment.find('.control') )==0 ) 
	    	pyforms_segment.hide(); 
	};

	////////////////////////////////////////////////////////////////////////////////

	show(){
		if( this.jquery_place().is(':visible') ) return;
		
		this.jquery_place().show();
		this.properties.visible = true;

		var parent = this.jquery_place().parent();
		
		if( parent.hasClass('row') ){

			if( parent.hasClass( 'no-alignment') ){
				//parent.addClass('fields');
				parent.show();

			}else{

				if( parent.hasClass('fields') ) parent.show();
					
				var found = false;
				for(var i=1; i<(COLUMNS_CSS_CLASSES.length-1); i++)
					if( parent.hasClass( COLUMNS_CSS_CLASSES[i] ) ){
						parent.removeClass( COLUMNS_CSS_CLASSES[i] );
						parent.addClass( COLUMNS_CSS_CLASSES[i+1] );
						//parent.addClass('fields');
						found = true;
						break;
					};
					
				if(!found){ 
				 	parent.addClass('fields');
					parent.addClass('one');
				}
			}
		}
		

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

	apply_deserialization(data){
		if(this.properties.visible)	
			this.show();
		else
			this.hide();

		if(this.properties.enabled)
			this.enable();
		else
			this.disable();
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

	after_init_control(){
		if(!this.properties.visible)	
			this.hide();
		if(!this.properties.enabled)
			this.disable();
		if(this.properties.style)
			this.jquery().attr('style', this.properties.style);
		if(this.properties.field_style)
			this.jquery_place().attr('style', this.properties.field_style);
	}

	////////////////////////////////////////////////////////////////////////////////

	update_server(){
		return this.get_value()!=this.properties.value
	}


}
