class ImageAnnotator {

	constructor(canvas, ctx, img) {
		this.canvas = canvas;
		this.ctx = ctx;
		this.img = new window.Image();
		this.img.parent = this;
		this.img.onload = this.on_load;

		this.x = 0;
		this.y = 0;
		this.width = 0;
		this.height = 0;

		this.zoom = 1;
		this.xshift = 0;
		this.yshift = 0;

		this.objects = [];
	}

	on_load(){
		var self = (this instanceof ImageAnnotator)?this:this.parent;
		self.update();
		self.draw();
	}

	update(){
		var self = (this instanceof ImageAnnotator)?this:this.parent;

		var aspect_ratio = self.img.width / self.img.height;
		var width = self.canvas.width*self.zoom;
		var height = self.canvas.height*self.zoom;
		if( aspect_ratio<1 ){
			width = ((self.canvas.height*self.img.width)/self.img.height)*self.zoom;
		}else{
			height = ((self.canvas.width*self.img.height)/self.img.width)*self.zoom;
		}
		this.x = self.canvas.width/2-width/2+self.xshift;
		this.y = self.canvas.height/2-height/2+self.yshift;
		this.width = width;
		this.height = height;
	}

	draw(){
		var self = (this instanceof ImageAnnotator)?this:this.parent;

		self.ctx.clearRect(0, 0, self.canvas.width, self.canvas.height);
		self.ctx.drawImage(self.img, self.x, self.y, self.width, self.height);

		for(var i=0; i<self.objects.length; i++) {
			self.objects[i].draw(self.ctx);
		}
	}

	move(x, y){
		var self = (this instanceof ImageAnnotator)?this:this.parent;
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
		var self = (this instanceof ImageAnnotator)?this:this.parent;

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

	set_value(value){
		this.img.src = value;
	}
}

class Circle{

	constructor(annotator, x, y, radius)
	{
		this.annotator = annotator;
		this.x = x;
		this.y = y;
		this.radius = radius;

		this._x = x;
		this._y = y;
		this._radius = radius;

		this.ref_x = 0;
		this.ref_y = 0;
	}

	update(){
		this._x = this.annotator.x + this.x * this.annotator.zoom;
		this._y = this.annotator.y + this.y * this.annotator.zoom;
		this._radius = this.radius * this.annotator.zoom;
	}

	move(x, y){
		this._x = this.x + x;
		this._y = this.y + y;
		this.ref_x = x;
		this.ref_y = y;
	}

	draw(ctx, center_active, radius_active, xx, yy, zoom){

		ctx.beginPath();
		ctx.arc(this._x, this._y, 1, 0, 2 * Math.PI);
		ctx.strokeStyle = center_active?'#ff0000':'#000000';
		ctx.stroke();

		ctx.beginPath();
		ctx.arc(this._x, this._y, this._radius, 0, 2 * Math.PI);
		ctx.strokeStyle = radius_active?'#ff0000':'#000000';
		ctx.stroke();
	}
}

class ControlDrawInImg extends ControlBase{


	////////////////////////////////////////////////////////////////////////////////
	init_control(){
		var html = `<div id='${this.place_id()}' class='field control ControlDrawInImg' >`;
		if(this.properties.label_visible)
			html += `<label for='${this.control_id()}'>${this.properties.label}</label>`;
		html += `<canvas id='${this.control_id()}' width='300' height='150' style='border:1px solid #d3d3d3;'>`;

		this.jquery_place().replaceWith(html);


		this.zoom = 1;
		this.xshift = 0;
		this.yshift = 0;
		this.active_idx = undefined;
		this.edit_center = false;
		this.edit_radius = false;

		this.canvas = document.getElementById(this.control_id());
		this.canvas.control = this;
		this.canvas.onwheel = this.onwheel;
		this.canvas.onmousemove = this.onmousemove;
		this.canvas.onmousedown = this.onmousedown;
		this.canvas.onmouseup = this.onmouseup;
		this.canvas.ondblclick = this.ondblclick;

		this.ctx = this.canvas.getContext("2d");


		this.annotator = new ImageAnnotator(this.canvas, this.ctx, this.img);

		this.annotator.objects.push( new Circle(this.annotator, 100, 50, 20) )

		this.set_value(this.properties.value);
		if(this.properties.required) this.set_required();
	};
	////////////////////////////////////////////////////////////////////////////////
		
	get_value(){ 
		return this.properties.value;
	};

	ondblclick(evt){
		var self = (this instanceof ControlDrawInImg)?this:this.control;

		var x = self.annotator.x;
		var y = self.annotator.y;

		self.annotator.objects.push( new Circle(evt.offsetX-x, evt.offsetY-y, 20) );
		self.draw();
	}

	onmouseup(evt){
		var self = (this instanceof ControlDrawInImg)?this:this.control;
		self.edit = false;
	}

	onmousedown(evt){
		var self = (this instanceof ControlDrawInImg)?this:this.control;

		var x = self.annotator.x;
		var y = self.annotator.y;

		for(var i=0; i<self.annotator.objects.length; i++){
			var circle = self.annotator.objects[i];
			var xx = circle.x*self.zoom+x;
			var yy = circle.y*self.zoom+y;

			var dist = Math.sqrt(Math.pow(xx-evt.offsetX, 2) + Math.pow(yy-evt.offsetY, 2) )
			if( dist<=5){
				self.edit_center = true;
				self.edit_radius = false;
				self.active_idx = i;
				self.draw();
				return
			}

			var radius = self.zoom*circle.radius;
			if( (radius-2)<=dist && dist<=(radius+2) ){
				self.edit_radius = true;
				self.edit_center = false;
				self.active_idx = i;
				self.draw();
				return;
			}
		};
		self.edit_center = false;
		self.edit_radius = false;
		this.active_idx = undefined;
		self.draw();
	}

	onmousemove(evt){
		var self = (this instanceof ControlDrawInImg)?this:this.control;


		if( evt.which ){
			if( self.edit_radius || self.edit_center ){

				var x = self.annotator.x;
				var y = self.annotator.y;

				var circle = self.annotator.objects[self.active_idx];
				var xx = circle.x*self.zoom+x;
				var yy = circle.x*self.zoom+y;
				var dist = Math.sqrt(Math.pow(xx-evt.offsetX, 2) + Math.pow(yy-evt.offsetY, 2) )
				var radius = self.zoom*circle.radius;

				if( self.edit_center){
					circle.x = (evt.offsetX-x)/self.zoom;
					circle.y = (evt.offsetY-y)/self.zoom;
					self.draw();
					return;
				}

				if( self.edit_radius ){
					circle.radius = dist/self.zoom;
					self.draw();
					return;
				}

			}else{
				self.annotator.move(evt.movementX, evt.movementY)
			}
		}else {

			var x = self.annotator.x;
			var y = self.annotator.y;

			for(var i=0; i<self.annotator.objects.length; i++) {
				var circle = self.annotator.objects[i];
				circle.set_move(x, y);
			}

			for(var i=0; i<self.annotator.objects.length; i++){
				var circle = self.annotator.objects[i];
				var xx = circle.x*self.zoom+x;
				var yy = circle.y*self.zoom+y;
				var dist = Math.sqrt(Math.pow(xx-evt.offsetX, 2) + Math.pow(yy-evt.offsetY, 2) )
				var radius = self.zoom*circle.radius;

				if( dist<=5){
					document.body.style.cursor = 'move';
					return;
				}

				if( (radius-2)<=dist && dist<=(radius+2) ){
					document.body.style.cursor = 'col-resize';
					return;
				}
			};
			document.body.style.cursor = 'default';
			console.log(document.body.style.cursor);

		}
	}

	onwheel(evt){
		var self = (this instanceof ControlDrawInImg)?this:this.control;

		self.annotator.do_zoom(evt.deltaY)
		self.annotator.draw();
		return false;
	};


	////////////////////////////////////////////////////////////////////////////////

	set_value(value){
		this.annotator.set_value(value);
	};
}