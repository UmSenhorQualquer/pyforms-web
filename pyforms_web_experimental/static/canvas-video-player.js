


class CanvasVideoPlayer{

    constructor(options){

        this.options = {
            framesPerSecond: 30,
            hideVideo: true,
            autoplay: false,
            playerSelector: false,
            timelineSelector: false,
            resetOnLastFrame: false,
            loop: false,
            video_width: null,
            video_height: null
        };

        for (var i in options) this.options[i] = options[i];

        // events handlers
        this.canvasClickHandler       = undefined;
        this.videoLoadedUpdateHandler = undefined;
        this.videoTimeUpdateHandler   = undefined;
        this.videoCanPlayHandler      = undefined;
        this.videoDurationChangeHandler = undefined
        this.timelineClickHandler     = undefined;
        this.windowResizeHandler      = undefined;

        this.player = document.querySelector(this.options.playerSelector);
        this.video  = document.querySelector(this.options.videoSelector);
        this.video_source = document.querySelector(this.options.videoSelector + '> source');
        this.canvas = document.querySelector(this.options.canvasSelector);
        this.timeline = document.querySelector(this.options.timelineSelector);
        this.timelinePassed  = document.querySelector(this.options.timelineSelector + '> div.video-timeline-passed');
        this.timeline_loaded = document.querySelector(this.options.timelineSelector + '> div.video-timeline-loaded');
        this.timeline_loaded = document.querySelector(this.options.timelineSelector + '> div.video-timeline-loaded');
        
        this.graph = new TimelineWidget({selector: this.options.playerSelector + '> div.video-graph' }, this);


        if (!this.options.videoSelector || !this.video) {
            console.error('No "videoSelector" property, or the element is not found');
            return;
        }

        if (!this.options.canvasSelector || !this.canvas) {
            console.error('No "canvasSelector" property, or the element is not found');
            return;
        }

        if (this.options.timelineSelector && !this.timeline) {
            console.error('Element for the "timelineSelector" selector not found');
            return;
        }

        if (this.options.timelineSelector && !this.timelinePassed) {
            console.error('Element for the "timelinePassed" not found');
            return;
        }

        if (this.options.timelineSelector && !this.timeline_loaded) {
            console.error('Element for the "timeline_loaded" not found');
            return;
        }


        // Canvas context
        this.ctx = this.canvas.getContext('2d');

        this.init();
        this.graph.init();
    }

    init() {
        this.unbind();
        this.video.load();
        
        this.draws = [];
        this.resizeTimeoutReference = false;
        this.RESIZE_TIMEOUT = 1000;
        this.playing = false;
        
        this.canvas.style.width  = this.options.video_width;
        this.canvas.style.height = this.options.video_height;

        this.setCanvasSize();

        if (this.options.hideVideo) {
            this.video.style.display = 'none';
        }

        this.bind();
    }

    open(video_url){
        this.video_source.src = video_url;
        this.init()
    }
    
  
    // Used most of the jQuery code for the .offset() method
    getOffset(elem) {
        var docElem, rect, doc;

        if (!elem) {
            return;
        }

        rect = elem.getBoundingClientRect();

        // Make sure element is not hidden (display: none) or disconnected
        if (rect.width || rect.height || elem.getClientRects().length) {
            doc = elem.ownerDocument;
            docElem = doc.documentElement;

            return {
                top: rect.top + window.pageYOffset - docElem.clientTop,
                left: rect.left + window.pageXOffset - docElem.clientLeft
            };
        }
    }

    jumpTo(percentage) {
        this.video.currentTime = this.video.duration * percentage;
    };

    jumpToFrame(frame) {
        this.video.currentTime = frame / this.options.framesPerSecond;
    };

    bind() {
        var self = this;

        // Playes or pauses video on canvas click
        this.canvas.addEventListener('click', this.canvasClickHandler = function() {
            self.playPause();
        });

        // On every time update draws frame
        this.video.addEventListener('progress', this.videoLoadedUpdateHandler = function(e) {
            if (self.options.timelineSelector)
                self.updateProgress();
        });

        // On every time update draws frame
        this.video.addEventListener('timeupdate', this.videoTimeUpdateHandler = function() {
            self.drawFrame();
            if (self.options.timelineSelector) {
                self.updateTimeline();
            }
        });

        // Draws first frame
        this.video.addEventListener('canplay', this.videoCanPlayHandler = function() {
            self.drawFrame();
        });
            
        this.video.addEventListener('durationchange', this.videoDurationChangeHandler = function(){

            self.graph.set_length((self.video.duration*self.options.framesPerSecond) | 0);
            
            /*           
            var link = self.options.draws_url.replace('{video}', 'xx')
            link = link.replace('{begin}', '0');
            link = link.replace('{end}', ''+ ((self.video.duration*self.options.framesPerSecond) | 0) );
            $.ajax({
                method: 'get',
                cache: false,
                dataType: "json",
                url: link+'?nocache='+$.now(),
                contentType: "application/json; charset=utf-8",
                success: function(res){
                    self.draws = res.drawings;
                }
            });*/
        });

        // To be sure 'canplay' event that isn't already fired
        if (this.video.readyState >= 2) this.drawFrame();

        if (this.options.autoplay) this.play();

        // Click on the video seek video
        this.timeline.addEventListener('click', this.timelineClickHandler = function(e) {

            var percentage = e.offsetX / self.timeline.clientWidth;
            self.jumpTo(percentage);
        });

        // Cache canvas size on resize (doing it only once in a second)
        window.addEventListener('resize', this.windowResizeHandler = function() {
            clearTimeout(self.resizeTimeoutReference);

            self.resizeTimeoutReference = setTimeout(function() {
                self.setCanvasSize();
                self.drawFrame();
            }, self.RESIZE_TIMEOUT);
        });
    };

    unbind(){

        if(this.canvasClickHandler)       this.canvas.removeEventListener('click', this.canvasClickHandler);
        if(this.videoLoadedUpdateHandler) this.video.removeEventListener('progress', this.videoLoadedUpdateHandler);
        if(this.videoTimeUpdateHandler)   this.video.removeEventListener('timeupdate', this.videoTimeUpdateHandler);
        if(this.videoCanPlayHandler)      this.video.removeEventListener('canplay', this.videoCanPlayHandler);
        if(this.videoDurationChangeHandler) this.video.removeEventListener('durationchange', this.videoDurationChangeHandler);
        if(this.timelineClickHandler)     this.timeline.removeEventListener('click', this.timelineClickHandler);
        if(this.windowResizeHandler)      window.removeEventListener('resize', this.windowResizeHandler);

    };

    updateProgress() {
        var buff = this.video.buffered;
        for(var i=0; i<buff.length; i++){
            if( buff.start(i)<=this.video.currentTime<=buff.end(i) ){
                var percentage = (buff.end(i) * 100 / this.video.duration).toFixed(2);
                if( percentage>=100 )
                    this.timeline_loaded.style.display = 'none';
                else
                    this.timeline_loaded.style.width = percentage + '%';
            }
        }
    };

    updateTimeline() {
        var percentage = (this.video.currentTime * 100 / this.video.duration).toFixed(2);
        this.timelinePassed.style.width = percentage + '%';

        this.graph.set_position( this.frame_index() );
    };

    setCanvasSize() {
        this.width  = this.canvas.clientWidth;
        this.height = this.canvas.clientHeight;

        this.canvas.setAttribute('width',  this.width);
        this.canvas.setAttribute('height', this.height);
    };

    play() {
        this.lastTime = Date.now();
        this.playing = true;
        this.loop();
    };

    pause() {
        this.playing = false;
    };

    playPause() {
        if (this.playing) {
            this.pause();
        }
        else {
            this.play();
        }
    };

    loop() {
        var self = this;
        var time = Date.now();
        var elapsed = (time - this.lastTime) / 1000;

        // Render
        if(elapsed >= (1 / this.options.framesPerSecond)) {
            this.video.currentTime = this.video.currentTime + elapsed;
            this.lastTime = time;
            
        }

        // If we are at the end of the video stop
        if (this.video.currentTime >= this.video.duration) {
            this.playing = false;

            if (this.options.resetOnLastFrame === true) {
                this.video.currentTime = 0;
            }

            if (this.options.loop === true) {
                this.video.currentTime = 0;
                this.play();
            }
        }

        if (this.playing) {
            this.animationFrame = window.requestAnimationFrame(function(){
                self.loop();
            });
        }
        else {
            window.cancelAnimationFrame(this.animationFrame);
        }
    };

    current_draws() {
        var idx = this.frame_index();
        
        if( idx>=this.draws.length ) return undefined;
        return this.draws[idx];
    };

    frame_index() {
        return (this.video.currentTime*this.options.framesPerSecond) | 0;
    };

    circle(x,y,radius,color) {
        
    };

    line(x,y,xx,yy,color) {
        this.ctx.beginPath();
        this.ctx.moveTo(x,y);
        this.ctx.lineTo(xx,yy);
        this.ctx.stroke();
    };

    contours(contours,color) {
        
    };

    rect(x,y,xx,yy,color) {
        
    };

    drawFrame() {
        this.ctx.drawImage(this.video, 0, 0, this.width, this.height);

        var draws = this.current_draws();
        if( draws!=undefined )
            for(var i=0; i<draws.length; i++){
                var draw = draws[i];
                switch( draw[0] ) {
                    case 0:
                        this.circle(draw[1], draw[2], draw[3], draw[4])
                        break;
                    case 1:
                        this.line(draw[1], draw[2], draw[3], draw[4], draw[5])
                        break;
                    case 2:
                        this.contours(draw[1], draw[2])
                        break;
                    case 3:
                        this.rect(draw[1], draw[2], draw[3], draw[4], draw[5])
                        break;
                };
            };
    };

    draw_timeline(){
        this.graph.draw();
    }

    add_graph(title, data, color){
        return this.graph.add_graph(title, data, color);
    } 

    add_event(title, begin, end, color, track_idx){
        this.graph.add_event(title, begin, end, color, track_idx);
    }
}
