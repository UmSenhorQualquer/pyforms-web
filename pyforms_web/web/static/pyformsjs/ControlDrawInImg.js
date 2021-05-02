class ImageAnnotator {

	constructor(canvas_id, update_evt) {
		this.canvas = document.getElementById(canvas_id);
		this.canvas.annotator = this;
		this.canvas.onwheel = this.onwheel;
		this.canvas.onmousemove = this.onmousemove;
		this.canvas.onmousedown = this.onmousedown;
		this.canvas.onmouseup = this.onmouseup;
		this.canvas.ondblclick = this.ondblclick;

		this.canvas.onmouseleave = this.onmouseleave;
		this.canvas.onmouseenter = this.onmouseenter;

		document.onkeydown = this.keydown;
		document.annotator = this;

		this.ctx = this.canvas.getContext("2d");

		this.img = new window.Image();
		this.img.annotator = this;
		this.img.onload = this.on_load;

		this.x = 0;
		this.y = 0;
		this.width = 0;
		this.height = 0;

		this.mouse_is_hover = false;

		this.zoom = 1;
		this.xshift = 0;
		this.yshift = 0;

		this.update_evt = update_evt;

		this.objects = [];
	}

	onmouseleave(evt){
		var self = (this instanceof ImageAnnotator)?this:this.annotator;
		self.mouse_is_hover = false;
	}

	onmouseenter(evt){
		var self = (this instanceof ImageAnnotator)?this:this.annotator;
		self.mouse_is_hover = true;
	}

	keydown(event) {
		var self = (this instanceof ImageAnnotator)?this:this.annotator;
		if( !self.mouse_is_hover ) return true;

		var key = event.keyCode || event.charCode;
		if( key == 8 ){
			if (self.active_idx) {
			  self.objects.splice(self.active_idx, 1);
			  self.edit_radius = false;
			  self.edit_center = false;
			  self.active_idx = undefined;
			  //self.update();
			  self.draw();
			  self.update_evt();
			}
		}
	}

	clear(){
		this.objects = [];
		this.update();
	}

	add_object(obj){
		obj.annotator = this;
		this.objects.push(obj)
		obj.update();
	}

	onwheel(evt){
		var self = (this instanceof ImageAnnotator)?this:this.annotator;
		self.do_zoom(evt.deltaY)
		self.draw();
		return false;
	};

	image_coordinates(x, y){ // x and y are mouse coordinates
		var xx = (x - this.x )/this.zoom;
		var yy = (y - this.y )/this.zoom;
		return [xx, yy];
	}

	ondblclick(evt){
		var self = (this instanceof ImageAnnotator)?this:this.annotator;

		var coords = self.image_coordinates(evt.offsetX, evt.offsetY);

		self.add_object( new Circle(coords[0], coords[1], 50) );
		self.draw();
		self.update_evt();
	}

	onmouseup(evt){
		var self = (this instanceof ImageAnnotator)?this:this.annotator;

		if( self.edit_center ){
			if( self.update_evt ) self.update_evt();
		}
		if( self.edit_radius ){
			if( self.update_evt ) self.update_evt();
		}
		self.edit_radius = false;
		self.edit_center = false;
		//self.active_idx = undefined;
		self.draw();
	}

	onmousedown(evt){
		var self = (this instanceof ImageAnnotator)?this:this.annotator;

		for(var i=0; i<self.objects.length; i++){
			var circle = self.objects[i];
			var choice = circle.is_mouse_hover(evt.offsetX, evt.offsetY);

			switch (choice){
				case 1:
					self.edit_center = true;
					self.edit_radius = false;
					self.active_idx = i;
					self.draw();
					return
					break;
				case 2:
					self.edit_radius = true;
					self.edit_center = false;
					self.active_idx = i;
					self.draw();
					return;
					break;
			}
		};
		self.edit_center = false;
		self.edit_radius = false;
		this.active_idx = undefined;
		self.draw();
	}

	onmousemove(evt){

		var self = (this instanceof ImageAnnotator)?this:this.annotator;

		if( evt.which ){
			if( self.edit_radius || self.edit_center ){

				var circle = self.objects[self.active_idx];

				if( self.edit_center){
					circle.move_to(evt.offsetX, evt.offsetY);
					self.draw();
					return;
				}

				if( self.edit_radius ){
					circle.screen_set_radius(circle.screen_distance_to_center(evt.offsetX, evt.offsetY));
					self.draw();
					return;
				}

			}else{
				self.move(evt.movementX, evt.movementY)
			}
		}else {

			for(var i=0; i<self.objects.length; i++) {
				var circle = self.objects[i];
				switch (circle.is_mouse_hover(evt.offsetX, evt.offsetY)) {
					case 1:
						document.body.style.cursor = 'move';
						return
						break;
					case 2:
						document.body.style.cursor = 'col-resize';
						return;
						break;
				}
				document.body.style.cursor = 'default';
			}
		}
	}

	update(){
		var self = (this instanceof ImageAnnotator)?this:this.annotator;

		var width = self.img.width*self.zoom;
		var height = self.img.height*self.zoom;

		this.x = self.canvas.width/2-width/2+self.xshift;
		this.y = self.canvas.height/2-height/2+self.yshift;
		this.width = width;
		this.height = height;

		for(var i=0; i<self.objects.length; i++) {
			self.objects[i].update();
		}
	}

	draw(){
		var self = (this instanceof ImageAnnotator)?this:this.annotator;

		self.ctx.clearRect(0, 0, self.canvas.width, self.canvas.height);
		self.ctx.drawImage(self.img, self.x, self.y, self.width, self.height);

		for(var i=0; i<self.objects.length; i++) {
			self.objects[i].draw(
				self.ctx,
				i==self.active_idx,
				i==self.active_idx && self.edit_radius
			);
		}
	}

	move(x, y){
		var self = (this instanceof ImageAnnotator)?this:this.annotator;
		self.xshift += x;
		self.yshift += y;
		if( self.xshift>self.canvas.width ){
			self.xshift = self.canvas.width;
		}
		if( (self.xshift+self.img.width)<0 ){
			self.xshift = -self.img.width;
		}
		if( self.yshift>self.canvas.height ){
			self.yshift = self.canvas.height;
		}
		if( (self.yshift+self.img.height)<0 ){
			self.yshift = -self.img.height;
		}
		self.update();

		for(var i=0; i<self.objects.length; i++) {
			self.objects[i].update()
		}

		self.draw();
	}

	do_zoom(deltaY){
		var self = (this instanceof ImageAnnotator)?this:this.annotator;

		self.zoom += deltaY * -0.01;

		if( self.zoom<0.1 ){
			self.zoom = 0.1;
		}
		if( self.zoom>20 ){
			self.zoom = 20;
		}
		self.update();

		for(var i=0; i<self.objects.length; i++) {
			self.objects[i].update()
		}

		self.draw();
	}

	on_load(){
		var self = (this instanceof ImageAnnotator)?this:this.annotator;

		var aspect_ratio = self.img.width / self.img.height;
		var width = self.canvas.width;
		var height = self.canvas.height;
		if( aspect_ratio>1 ){
			if( (self.canvas.width/self.canvas.height)>1 ){
 				width = (self.canvas.height*self.canvas.width)/self.img.height;
 				self.zoom = width / self.img.width;
			}else{
				height = (self.canvas.width*self.canvas.height)/self.img.width;
 				self.zoom = width / self.img.width;
			}
		}else{
			if( (self.canvas.width/self.canvas.height)>1 ){
				height = (self.canvas.width*self.canvas.height)/self.img.width;
 				self.zoom = height / self.img.height;
			}else{
				width = (self.canvas.height*self.canvas.width)/self.img.height;
 				self.zoom = width / self.img.width;
			}
		}

		self.update();
		self.draw();
	}

	set_value(value){
		this.img.src = value;
	}
}




class Circle{

	constructor(x, y, radius, text)
	{
		this.annotator = undefined; // pointer to the annotator object.
		this.x = x; // x coordinate of the circle in relation to the image.
		this.y = y; // y coordinate of the circle in relation to the image.
		this.radius = radius; // radius of the circle in relation to the image.
		this.text = text;

		this._x = x; // x coordinate of the circle in relation to the canvas.
		this._y = y; // y coordinate of the circle in relation to the canvas.
		this._radius = radius; // radius of the circle in relation to the canvas.
	}

	update(){
		this._x = this.annotator.x + this.x * this.annotator.zoom;
		this._y = this.annotator.y + this.y * this.annotator.zoom;
		this._radius = this.radius * this.annotator.zoom;
	}

	move_to(x, y){ // x, y are coordinates of the mouse.
		this._x = x;
		this._y = y;
		this.x = (x - this.annotator.x)/this.annotator.zoom;
		this.y = (y - this.annotator.y)/this.annotator.zoom;
	}

	screen_distance_to_center(x, y){ // x, y are coordinates of the mouse.
		return Math.sqrt(Math.pow(this._x-x, 2) + Math.pow(this._y-y, 2) )
	}

	screen_set_radius(radius){
		this._radius = radius;
		this.radius = radius / this.annotator.zoom;
	}

	draw(ctx, center_active, radius_active, xx, yy, zoom){

		ctx.beginPath();
		ctx.arc(this._x, this._y, 1, 0, 2 * Math.PI);
		ctx.strokeStyle = center_active?'#ff0000':'#00FF00';
		ctx.stroke();

		if(this.text){
			ctx.font = "12px Arial";
			ctx.fillStyle = radius_active?'#ff0000':'#00FF00';
			ctx.textAlign = "center";
			ctx.fillText(this.text, this._x, this._y-5);
		}

		ctx.beginPath();
		ctx.arc(this._x, this._y, this._radius, 0, 2 * Math.PI);
		ctx.strokeStyle = radius_active?'#ff0000':'#00FF00';
		ctx.stroke();

		ctx.beginPath();
		ctx.rect(this._x-this._radius*1.2, this._y-this._radius*1.2, 2*this._radius*1.2, 2*this._radius*1.2);
		ctx.strokeStyle = 'rgba(225,0,0,0.5)';
		ctx.stroke();
	}

	is_mouse_hover(x, y){
		var dist = this.screen_distance_to_center(x, y);

		if( dist<=5){
			// Hover the center.
			return 1;
		}

		if( (this._radius-2)<=dist && dist<=(this._radius+2) ){
			// Hover the radius.
			return 2;
		}
	}
}




class ControlDrawInImg extends ControlBase{


	////////////////////////////////////////////////////////////////////////////////
	init_control(){
		var html = `<div id='${this.place_id()}' class='field control ControlDrawInImg' >`;
		if(this.properties.label_visible)
			html += `<label for='${this.control_id()}'>${this.properties.label}</label>`;
		html += `<canvas id='${this.control_id()}' style='border:1px solid #d3d3d3;'>`;

		this.jquery_place().replaceWith(html);

		var width = this.jquery_place().width();
		var height = this.jquery_place().height();
		if( height < 500 ) height = 500;
		this.jquery().attr('width', width);
		this.jquery().attr('height', height);


		this.annotator = new ImageAnnotator(this.control_id(), this.annotator_has_updated);
		this.annotator.control = this;

		this.set_value(this.properties.value);

		for(var i=0; i<this.properties.circles.length; i++){
			var circle = this.properties.circles[i];
			this.annotator.add_object(new Circle(circle[0], circle[1], circle[2], circle[3]) )
		}

		if(this.properties.required) this.set_required();
	};
	////////////////////////////////////////////////////////////////////////////////

	deserialize(data) {
		super.deserialize(data);

		this.annotator.clear()
		for(var i=0; i<this.properties.circles.length; i++){
			var circle = this.properties.circles[i];
			this.annotator.add_object(new Circle(circle[0], circle[1], circle[2], circle[3]) )
		}
		this.annotator.update();
		this.annotator.draw();
	}

	serialize(){
        var data = super.serialize();
        data.circles = [];
		for(var i=0; i<this.annotator.objects.length; i++){
			var circle = this.annotator.objects[i];
			data.circles.push([circle.x, circle.y, circle.radius, circle.text])
		}
		return data;
    }

    update_server(){
		return true;
	}


	annotator_has_updated(){
		this.control.basewidget.fire_event( this.control.name, 'update_control_event' );
	}

	////////////////////////////////////////////////////////////////////////////////

	set_value(value){
		this.annotator.set_value(value);
	};
}