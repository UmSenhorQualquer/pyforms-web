class ControlTree extends ControlBase{

    ////////////////////////////////////////////////////////////////////////////////
    init_control(){
        var html = "<div id='"+this.place_id()+"' class='field control ControlTree' >"
        html += "<ul class='tree' id='"+this.control_id()+"' >";
        for(var i=0; i<this.properties.root.childs.length; i++)
            html += this.render_node(this.properties.root.childs[i]);
        html += "</ul>"
        html += "</div>";
        this.jquery_place().replaceWith(html);

        this.set_value(this.properties.value);

        var self = this;
        $("#"+this.control_id()+" label").click(function(){
            self.set_value( $(this).attr('node-id') );
            self.basewidget.fire_event( self.name, 'update_control_event' );
        });

        if(this.properties.error) this.jquery_place().addClass('error'); else this.jquery_place().removeClass('error');
		if(this.properties.required) this.set_required();
    };
    ////////////////////////////////////////////////////////////////////////////////

    render_node(node){
        var html = "<li><label node-id='"+node.node_id+"' >"+node.name+"</label>";
        if( node.childs.length>0 ){
            html += "<ul>";
            for(var i=0; i<node.childs.length; i++)
                html += this.render_node(node.childs[i]);
            html += "</ul>";  
        };
        html += "</li>"
        return html;
    };

    ////////////////////////////////////////////////////////////////////////////////

    /**
    Sets the value of the control.
    @param {object} value - Value to set.
    */
    set_value(value){
        $("#"+this.control_id()+" label").removeClass('selected');
        $("#"+this.control_id()+" label[node-id="+value+"]").addClass('selected');
    }

    ////////////////////////////////////////////////////////////////////////////////
    
    /**
    Get the value of the control.
    @returns {jquery}.
    */
    get_value(){ 
        var e = $("#"+this.control_id()+" label.selected");
        if( e.length>0 )
            return e.attr('node-id');
        return null;
    }

    ////////////////////////////////////////////////////////////////////////////////

    /**
    Sets the label of the control.
    @param {string} value - Label to set.
    */
    set_label(value){}


}