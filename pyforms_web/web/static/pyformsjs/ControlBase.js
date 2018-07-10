var COLUMNS_CSS_CLASSES = ['','one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve','thirteen','fourteen','fiveteen','sixteen','seventeen','eighteen','nineteen','twenty','twentyone','twentytwo'];

class ControlBase{
    /**
    ControlBase class implements the basic control functionalities.
    @param {str} name - Name of the control.
    @param {str} properties - Properties of the control.
    */
    constructor(name, properties){
        var self = this;
        this.name           = name;
        this.properties     = properties;
        this.basewidget     = undefined; //Will be set in runtime by the parent BaseWidget object.
        this.added_classes  = [];
        this.added_fieldclasses  = [];
    }

    ////////////////////////////////////////////////////////////////////////////////

    /**
    Widget id.
    @returns {str}.
    */
    app_id(){ 
        return this.basewidget.widget_id; 
    }

    ////////////////////////////////////////////////////////////////////////////////

    /**
    Control id.
    @returns {str}.
    */
    control_id(){ 
        return this.basewidget.control_id(this.name); 
    }

    ////////////////////////////////////////////////////////////////////////////////

    /**
    JQuery object of the control html.
    @returns {jquery}.
    */
    jquery(){ 
        return $("#"+this.control_id()); 
    }

    ////////////////////////////////////////////////////////////////////////////////

    /**
    Div id where the control is placed.
    @returns {str}.
    */
    place_id(){ 
        return "place-"+this.control_id(); 
    }

    ////////////////////////////////////////////////////////////////////////////////

    /**
    JQuery object of the div where the control is placed.
    @returns {jquery}.
    */
    jquery_place(){ 
        return $( "#"+this.place_id() ); 
    }

    ////////////////////////////////////////////////////////////////////////////////

    /**
    Sets the css classes for the control. Previously added classes will be removed.
    @param {str} css - String with the css classes to add.
    */
    set_css(css){
        for(var i=0; i<this.added_classes.length; i++)
            this.jquery().removeClass(this.added_classes[i]);
    
        var classes = css.split(" ");

        for(var i=0; i<classes.length; i++)
            this.jquery().addClass(classes[i]);

        this.added_classes = classes;
    }

    ////////////////////////////////////////////////////////////////////////////////

    /**
    Sets the css classes for the field where the control is. Previously added classes will be removed.
    @param {str} css - String with the css classes to add.
    */
    set_field_css(css){
        for(var i=0; i<this.added_fieldclasses.length; i++)
            this.jquery_place().removeClass(this.added_fieldclasses[i]);
    
        var classes = css.split(" ");

        for(var i=0; i<classes.length; i++)
            this.jquery_place().addClass(classes[i]);
        
        this.added_fieldclasses = classes;
    }

    ////////////////////////////////////////////////////////////////////////////////

    /**
    Get the value of the control.
    @returns {jquery}.
    */
    get_value(){ 
        if(this.jquery().length==0) return this.properties.value;
        var value = this.jquery().val();
        if(value=='null') return null;
        else return value;
    }

    ////////////////////////////////////////////////////////////////////////////////

    /**
    Sets the value of the control.
    @param {object} value - Value to set.
    */
    set_value(value){
        if(this.jquery().length>0) 
            if(this.properties.value!=null)
                this.jquery().val(this.properties.value); 
            else
                this.jquery().val(''); 
    }

    ////////////////////////////////////////////////////////////////////////////////

    /**
    Sets the label of the control.
    @param {str} value - Label to set.
    */
    set_label(value){
        $( "#"+this.place_id()+' label' ).first().html(value);
    }

    ////////////////////////////////////////////////////////////////////////////////
    
    /**
    Enable the control.
    */
    enable(){
        this.jquery().removeAttr('disabled');
        this.jquery().removeClass('disabled');
    }

    ////////////////////////////////////////////////////////////////////////////////
    
    /**
    Disable the control.
    */
    disable(){
        this.jquery().attr('disabled', 'true');
        this.jquery().addClass('disabled');
    }

    ////////////////////////////////////////////////////////////////////////////////

    /**
    Hide the control.
    */
    hide(){
        function count_visible( selector ){
            var visible = 0;  
            selector.each(function(i,e){  
                if( $(e).css('display')!='none') visible += 1;  
            });  
            return visible
        }

        if( count_visible( this.jquery_place() )==0 ) return;
        
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
            if( count_visible( parent.find('.control') )==0 ){
                parent.hide();  
                for(var i=0; i<COLUMNS_CSS_CLASSES.length-1; i++)
                    parent.removeClass( COLUMNS_CSS_CLASSES[i] );
            }
        }

        var pyforms_segment = this.jquery_place().parents('.pyforms-segment');
        if( count_visible( pyforms_segment.find('.control') )==0 ) 
            pyforms_segment.hide(); 
    }

    ////////////////////////////////////////////////////////////////////////////////

    /**
    Show the control.
    */
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
    }

    ////////////////////////////////////////////////////////////////////////////////

    /**
    Deserialize the data from the server. 
    This function is called at the initialization of the control and everytime data is received from the server. 
    @param {object} data - Data sent by the server.
    */
    deserialize(data){
        $.extend(this.properties, data);
        this.set_value(this.properties.value);
        this.set_label(this.properties.label);

        if(this.properties.error) this.jquery_place().addClass('error'); else this.jquery_place().removeClass('error');
    }

    ////////////////////////////////////////////////////////////////////////////////

    /**
    Function called after the deserialization of the server data. 
    It applies the controls most common configurations.
    @param {object} data - Data sent by the server.
    */
    apply_deserialization(data){

        if(this.properties.visible) 
            this.show();
        else
            this.hide();

        if(this.properties.enabled)
            this.enable();
        else
            this.disable();

        if(this.properties.style)
            this.jquery().attr('style', this.properties.style);

        if(this.properties.field_style)
            this.jquery_place().attr('style', this.properties.field_style);

        if(this.properties.css)
            this.set_css(this.properties.css);

        if(this.properties.field_css)
            this.set_field_css(this.properties.field_css);
    }

    ////////////////////////////////////////////////////////////////////////////////

    /**
    Serializes the control data to send back to the server.
    @returns {object}.
    */
    serialize(){
        this.properties.value = this.get_value();
        return this.properties; 
    }

    ////////////////////////////////////////////////////////////////////////////////

    /**
    Function called to initialize the control html and events.
    */
    init_control(){   
        if(this.properties.error) this.jquery_place().addClass('error'); else this.jquery_place().removeClass('error');
    }

    ////////////////////////////////////////////////////////////////////////////////

    /**
    Function called after the init_control function. It applies the controls most common configurations.
    */
    after_init_control(){
        
        if(!this.properties.visible)    
            this.hide();
        
        if(!this.properties.enabled)
            this.disable();
        
        if(this.properties.style)
            this.jquery().attr('style', this.properties.style);
        
        if(this.properties.field_style)
            this.jquery_place().attr('style', this.properties.field_style);

        if(this.properties.css)
            this.set_css(this.properties.css);

        if(this.properties.field_css)
            this.set_field_css(this.properties.field_css);
    }

    ////////////////////////////////////////////////////////////////////////////////

    /**
    Function called before the serialization.
    It is used to decide if the control should be updated in the server.
    */
    update_server(){
        return this.get_value()!=this.properties.value
    }


}
