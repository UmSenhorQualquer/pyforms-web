

class TimelineWidget{
    /**
    ControlBase class implements the basic control functionalities.
    @param {str} name - Name of the control.
    @param {str} properties - Properties of the control.
    */
    constructor(options, player){
        this.options = {
            selector: false,
            x_step: 100,
            y_step: 34,
            top_margin: 20
        };

        for (var i in options) {
            this.options[i] = options[i];
        }

        this.timeline_length=10000;

        this.player = player;

        this.timeline = document.querySelector(this.options.selector);
        
        this.timeline.innerHTML = `
        <canvas></canvas>
        <div class='timeline-progressbar'><div></div></div>
        <div class='timeline-zoombar'><i class='ui icon minus'></i><i class='ui icon plus'></i><div></div></div>
        `
        this.canvas       = document.querySelector(this.options.selector + '> canvas');
        this.zoom_wrapper = document.querySelector(this.options.selector + '> .timeline-zoombar');
        this.zoom_div     = document.querySelector(this.options.selector + '> .timeline-zoombar > div');
        
        this.progress_wrapper = document.querySelector(this.options.selector + '> .timeline-progressbar');
        this.progrees_div     = document.querySelector(this.options.selector + '> .timeline-progressbar > div');
        
        this.ctx = this.canvas.getContext('2d');

        this.last_x     = null;
        this.last_clip  = null;
        this.tracks     = [];
        this.graphs     = [];

        this.offset     = 0;
        this.pointer_frame = 0;

        this.set_zoom(1.0);

    }

    init(){
        this.width  = this.timeline.clientWidth;
        this.height = this.timeline.clientHeight;
        this.canvas.setAttribute('width', this.width);
        this.canvas.setAttribute('height', this.height);

        
        /*var track = this.add_track('track 1');
        track.add_event('Event x', 20, 40);
        track.add_event('Event x', 200, 300);
        track.add_event('Event x', 50, 70);
        track.add_event('Event x', 500, 650);
        track.add_event('Event x', 1000, 1200, 'green');

        // draw graph
        var values = Array.from({length: 1000}, () => Math.floor(Math.random() * 70));

        var graph = this.add_graph('Test', values, '#4c4');*/

        this.draw();
        
        this.bind();
    }



    bind(){
        var self = this;
        
        this.timeline.addEventListener('click', function(e){
            if(e.offsetY<self.options.top_margin)
                self.player.jumpToFrame( self.x2frame(e.offsetX) );
        });

        window.addEventListener('resize', function() {
            self.width  = self.timeline.clientWidth;
            self.canvas.setAttribute('width', self.width);
            self.update_progressbar();
            self.zoom_div.style.width = self.zoom_wrapper.clientWidth*self.zoom/4;
            self.draw();
        });

        /*
        this.progress_wrapper.addEventListener('click', function(e){
            var percentage = e.offsetX / self.timeline_length;
            var frame2jump = self.timeline_length*percentage;
            self.set_offset( frame2jump );
        });*/

        this.timeline.addEventListener('wheel', function(e){
            self.move(-e.deltaY);
            event.preventDefault();
        });

        this.zoom_wrapper.addEventListener('click', function(e) {
            var percentage = e.offsetX / self.zoom_wrapper.clientWidth;
            self.set_zoom(percentage*4);
        });
    }

    update_progressbar(){
        var percentage = ( this.x2frame(this.width) / this.timeline_length )*100;
        this.progrees_div.style.width = (percentage<100?percentage:100) + '%';
    }

    set_length(value){
        this.timeline_length = value;
        this.update_progressbar();
    }

    set_zoom(percentage){
        this.zoom = percentage;
        this.zoom_div.style.width = this.zoom_wrapper.clientWidth*this.zoom/4;
        this.draw();

        // update progress bar
        this.update_progressbar()
    }

    set_offset(offset){
        this.offset = offset;
        var visible_frames = (this.width/this.zoom);

        if( this.x2frame(this.width) > this.timeline_length ) this.offset = this.timeline_length-(this.width/this.zoom);
        if( this.offset<0) this.offset=0;
        

        this.draw();
        // update progress bar
        this.update_progressbar()
    }

    move(delta){
        this.set_offset(this.offset+delta);
        /*
        if(delta>0){
            var clip = this.ctx.getImageData(0, 0, this.width-delta, this.height);
            this.ctx.putImageData(clip, delta, 0);

            this.draw_grid(  0, delta);
            this.draw_events(0, delta);
            this.draw_graphs(0, delta);

        }else if(delta<0){
            delta = Math.abs(delta);
            var clip = this.ctx.getImageData(delta, 0, this.width-delta, this.height);
            this.ctx.putImageData(clip, 0, 0);

            this.draw_grid(  this.width-delta, this.width);
            this.draw_events(this.width-delta, this.width);
            this.draw_graphs(this.width-delta, this.width);
        }*/
    }

    add_track(title, color){
        var track = new TimelineTrack(this.tracks.length, title, color, this);
        this.tracks.push(track);
        return track;
    }

    add_graph(title, data, color){
        var graph = new TimelineGraph(title, data, color, this);
        this.graphs.push(graph);
        this.draw();
        return graph;
    }

    add_event(title, begin, end, color, track_idx){
        if( track_idx>=this.tracks.length ){
            for(var i=0; i<(track_idx-this.tracks.length+1); i++)
                this.add_track('');
        }

        return this.tracks[track_idx].add_event(title, begin, end, color, this.tracks[track_idx]);
    }

    draw_grid(){
        this.ctx.clearRect(0, 0, this.width, this.height);

        this.ctx.setLineDash([4, 4]);
        this.ctx.strokeStyle = "#ddd";
        this.ctx.fillStyle   = "#ccc"
        this.ctx.font        = "10px Arial";

        this.ctx.beginPath();

        var begin = this.offset % this.options.x_step;
        
        var x_pixel = 0;

        // draw vertical lines
        for(var x=begin+0.5; x<this.width; x+=this.options.x_step){
            this.ctx.moveTo(x,this.options.top_margin);
            this.ctx.lineTo(x,this.height);

            // draw frames text
            var txt = this.x2frame(x).toString();
            var txt_x = -this.ctx.measureText(txt).width/2+x;
            this.ctx.fillText(txt, txt_x, 15);
        }

                // draw horizontal labs
        for(var y=this.options.top_margin+0.5; y<this.height; y+=this.options.y_step){
            this.ctx.moveTo(0,y);
            this.ctx.lineTo(this.width,y);

        }
        this.ctx.stroke();
        this.ctx.setLineDash([]);   
    }

    draw_events(){
        for(var i in this.tracks){
            this.tracks[i].draw();
        }
    }

    draw_graphs(){
        for(var i in this.graphs){
            this.graphs[i].draw();
        }
    }

    draw_pointer(){
        var x = this.frame2x(this.pointer_frame+0.5);
        this.ctx.beginPath();
        this.ctx.globalAlpha=0.6;
        this.ctx.strokeStyle = "green";
        this.ctx.moveTo(x,10);
        this.ctx.lineTo(x,this.height);
        this.ctx.stroke();

        this.ctx.beginPath();
        this.ctx.arc(x,10,3,0,2*Math.PI);    
        this.ctx.fill();
        this.ctx.globalAlpha=1;
    }

    draw(){
        this.draw_grid();
        this.draw_graphs();
        this.draw_events();
        this.draw_pointer();
    }


    set_position(frame_idx){
        this.pointer_frame = frame_idx;

        var x = this.frame2x(frame_idx);

        if(x>this.width || x<0)
            this.set_offset(frame_idx);
        
        if(this.last_clip)
            this.ctx.putImageData(this.last_clip, this.last_x, 0);

        this.last_clip = this.ctx.getImageData((x-5)<0?0:(x-5), 0, 10, this.height);
        this.last_x    = x-5;

        this.draw_pointer();

        
    }


    x2frame(x){
        return (this.offset + (x/this.zoom)) | 0;
    }

    frame2x(frame){
        return ( (frame-this.offset) * this.zoom) | 0;
    }
}