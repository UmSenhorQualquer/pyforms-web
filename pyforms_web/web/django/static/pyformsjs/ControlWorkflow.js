

function ControlWorkflow(name, properties){
	ControlBase.call(this, name, properties);
};
ControlWorkflow.prototype = Object.create(ControlBase.prototype);

////////////////////////////////////////////////////////////////////////////////

ControlWorkflow.prototype.init_control = function(){
	var html = "<div id='"+this.place_id()+"' class='field ControlWorkflow ui segment' ><label>"+this.properties.label+"</label><div id='"+this.control_id()+"' ></div></div>";
	this.jquery_place().replaceWith(html);

	var self = this;
	this.jquery().change(function(){
		self.basewidget.fire_event( self.name, 'changed' );
	});

	if(!this.properties.visible) this.hide();

	$( '#'+this.control_id() ).flowchart({ data: this.properties.value, multipleLinksOnOutput:true });

	if(this.properties.operator_selected_evt)
		$( '#'+this.control_id() ).flowchart({ onOperatorSelect: function(operatorId){
			self.properties.selected_operator = operatorId;
				
			if( !self.properties.stop_operator_select_evt ){
				self.properties.no_selected_operator_update = 1;
				self.properties.selected_operator = operatorId;
				self.basewidget.fire_event( self.name, 'operator_selected_evt' );
				self.properties.no_selected_operator_update = undefined;
			}
			
			return true;
		} });

	if(this.properties.operator_unselected_evt)
		$( '#'+this.control_id() ).flowchart({ onOperatorUnselect: function(){
			self.properties.selected_operator = undefined;
				
			if( !self.properties.stop_operator_unselect_evt ){
				self.properties.no_selected_operator_update = 1;
				self.basewidget.fire_event( self.name, 'operator_unselected_evt' );
				self.properties.no_selected_operator_update = undefined;
			}
			return true;
		} });
	
};

////////////////////////////////////////////////////////////////////////////////

ControlWorkflow.prototype.set_value = function(value){
	$( '#'+this.control_id() ).flowchart('setData', value);
};

////////////////////////////////////////////////////////////////////////////////

ControlWorkflow.prototype.get_value = function(){ 
	return $( '#'+this.control_id() ).flowchart('getData');
};

////////////////////////////////////////////////////////////////////////////////

ControlWorkflow.prototype.serialize = function(){
	this.properties.value = this.get_value();
	if( !this.properties.no_selected_operator_update ){
		var selected_operator = $( '#'+this.control_id() ).flowchart('getSelectedOperatorId');
		if( selected_operator ) this.properties.selected_operator = selected_operator;
	}
	return this.properties; 
};


////////////////////////////////////////////////////////////////////////////////

ControlWorkflow.prototype.deserialize = function(data){
	$.extend(this.properties, data);

	if(this.properties.visible) 
		this.show();
	else 
		this.hide();

	this.set_value(this.properties.value);

	if( this.properties.selected_operator ){
		this.properties.stop_operator_select_evt = 1;
		$('#'+this.control_id() ).flowchart('selectOperator', this.properties.selected_operator);
		this.properties.stop_operator_select_evt = undefined;
	}
	
	if( data.deleteSelected ){
		this.properties.stop_operator_unselect_evt = 1;
		$( '#'+this.control_id() ).flowchart('deleteSelected');
		this.properties.stop_operator_unselect_evt = undefined;
	};

	
};
