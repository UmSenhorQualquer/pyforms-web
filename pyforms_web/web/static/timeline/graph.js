var TIMELINEGRAPH_COLORS = ['#DC143C','	#6495ED','#008B8B','#7FFF00', '#E9967A','#2F4F4F', '#9400D3', '#FFD700', '#FFB6C1', '#BA55D3','#9ACD32' ];

class TimelineGraph{
	
	constructor(title, data, color, timeline){

    	this.title    = title;
    	this.color 	  = color?color:TIMELINEGRAPH_COLORS.shift();
    	this.timeline = timeline;
    	this.data     = data?data:[];

    	this.zoom = 1.0;
    	this.top = 0;
    	this.min = Math.min(...this.data);
    	this.max = Math.max(...this.data);

    	this.ctx = timeline.ctx;
    }

    draw(){
    	var begin = this.timeline.offset | 0;
        var end   = (this.timeline.offset+this.timeline.width) | 0;

    	if( begin>=this.data.length ) return;

    	var top_margin = this.timeline.options.top_margin;
    	//calculate the height visible 
		var fov_height = (this.timeline.height - top_margin) * this.zoom;
		//check if the end frame his higher than the available data
		end = end>this.data.length?this.data.length:end;
		//calculate the difference bettween the lower and higher value
		var diff_max_min = this.max - this.min;
		if(diff_max_min<=0) diff_max_min = 1

		this.ctx.beginPath();
        this.ctx.strokeStyle = this.color;

        var y = this.data[begin];
        y = this.timeline.height - (y*fov_height)/diff_max_min;
        this.ctx.moveTo(0,y);

        for(var x=begin; x<end; x++){
        	y = this.data[x];

        	if( y==undefined ) continue;
			y = this.timeline.height - (y*fov_height)/diff_max_min;			
            this.ctx.lineTo( this.timeline.frame2x(x)+0.5, y);    
        }
        this.ctx.stroke();
    }
}