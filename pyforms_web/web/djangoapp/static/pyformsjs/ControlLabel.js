

function ControlLabel(name, properties){
    ControlBase.call(this, name, properties);
};
ControlLabel.prototype = Object.create(ControlBase.prototype);


////////////////////////////////////////////////////////////////////////////////

ControlLabel.prototype.get_value = function(){ 
    return this.properties.value;
};

////////////////////////////////////////////////////////////////////////////////

ControlLabel.prototype.init_control = function(){
    var html = '<div class="ui field '+this.properties.css+' message ControlLabel" id="'+this.place_id()+'"  >';
    html += '<div class="header">';
    html += this.properties.label;
    html += '</div>';
    html += '<p id="'+this.control_id()+'" >';
    if(this.properties.value!=null || this.properties.value!=undefined)
        html += this.properties.value;
    html += '</p>';
    html += '</div>';
    this.jquery_place().replaceWith(html);


    if(!this.properties.visible) this.hide(undefined, true);
};

////////////////////////////////////////////////////////////////////////////////

ControlLabel.prototype.set_value = function(value){
    this.init_control();
};

////////////////////////////////////////////////////////////////////////////////