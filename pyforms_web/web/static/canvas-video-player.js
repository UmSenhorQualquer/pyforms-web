var cvpHandlers = {
    canvasClickHandler: null,
    videoTimeUpdateHandler: null,
    videoCanPlayHandler: null,
    windowResizeHandler: null,
    videoLoadedUpdateHandler: null
};

var CanvasVideoPlayer = function(options) {
    this.options = {
        framesPerSecond: 25,
        hideVideo: true,
        autoplay: false,
        audio: false,
        playerSelector: false,
        timelineSelector: false,
        resetOnLastFrame: true,
        loop: false,
        video_width: null,
        video_height: null,
        draws_url: null
    };

    for (var i in options) {
        this.options[i] = options[i];
    }

    this.player = document.querySelector(this.options.playerSelector);
    this.video  = document.querySelector(this.options.videoSelector);
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


    if (this.options.audio) {
        if (typeof(this.options.audio) === 'string'){
            // Use audio selector from options if specified
            this.audio = document.querySelectorAll(this.options.audio)[0];

            if (!this.audio) {
                console.error('Element for the "audio" not found');
                return;
            }
        } else {
            // Creates audio element which uses same video sources
            this.audio = document.createElement('audio');
            this.audio.innerHTML = this.video.innerHTML;
            this.video.parentNode.insertBefore(this.audio, this.video);
            this.audio.load();
        }

        var iOS = /iPad|iPhone|iPod/.test(navigator.platform);
        if (iOS) {
            // Autoplay doesn't work with audio on iOS
            // User have to manually start the audio
            this.options.autoplay = false;
        }
    }

    // Canvas context
    this.ctx = this.canvas.getContext('2d');
    this.playing = false;

    this.resizeTimeoutReference = false;
    this.RESIZE_TIMEOUT = 1000;

    this.draws = [];

    this.init();
    this.bind();
    this.graph.init();
};

CanvasVideoPlayer.prototype.init = function() {
    this.video.load();
    
    this.canvas.style.width  = this.options.video_width;
    this.canvas.style.height = this.options.video_height;

    this.setCanvasSize();

    if (this.options.hideVideo) {
        this.video.style.display = 'none';
    }    
};


// Used most of the jQuery code for the .offset() method
CanvasVideoPlayer.prototype.getOffset = function(elem) {
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
};

CanvasVideoPlayer.prototype.jumpTo = function(percentage) {
    this.video.currentTime = this.video.duration * percentage;

    if (this.options.audio) {
        this.audio.currentTime = this.audio.duration * percentage;
    }
};

CanvasVideoPlayer.prototype.jumpToFrame = function(frame) {
    this.video.currentTime = frame / this.options.framesPerSecond;

    if (this.options.audio) {
        this.audio.currentTime = frame / this.options.framesPerSecond;
    }
};

CanvasVideoPlayer.prototype.bind = function() {
    var self = this;

    // Playes or pauses video on canvas click
    this.canvas.addEventListener('click', cvpHandlers.canvasClickHandler = function() {
        self.playPause();
    });

    // On every time update draws frame
    this.video.addEventListener('progress', cvpHandlers.videoLoadedUpdateHandler = function(e) {
        if (self.options.timelineSelector)
            self.updateProgress();
    });

    // On every time update draws frame
    this.video.addEventListener('timeupdate', cvpHandlers.videoTimeUpdateHandler = function() {
        self.drawFrame();
        if (self.options.timelineSelector) {
            self.updateTimeline();
        }
    });

    // Draws first frame
    this.video.addEventListener('canplay', cvpHandlers.videoCanPlayHandler = function() {
        self.drawFrame();
    });

    var self = this;
        
    this.video.addEventListener('durationchange', function(){
        
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
        });
    });

    

    // To be sure 'canplay' event that isn't already fired
    if (this.video.readyState >= 2) {
        self.drawFrame();
    }

    if (self.options.autoplay) {
      self.play();
    }

    // Click on the video seek video
    if (self.options.timelineSelector) {
        this.timeline.addEventListener('click', function(e) {
            var offset = e.clientX - self.getOffset(self.canvas).left;
            var percentage = offset / self.timeline.offsetWidth;
            self.jumpTo(percentage);
        });
    }

    // Cache canvas size on resize (doing it only once in a second)
    window.addEventListener('resize', cvpHandlers.windowResizeHandler = function() {
        clearTimeout(self.resizeTimeoutReference);

        self.resizeTimeoutReference = setTimeout(function() {
            self.setCanvasSize();
            self.drawFrame();
        }, self.RESIZE_TIMEOUT);
    });

    this.unbind = function() {
        this.canvas.removeEventListener('click', cvpHandlers.canvasClickHandler);
        this.video.removeEventListener('timeupdate', cvpHandlers.videoTimeUpdateHandler);
        this.video.removeEventListener('canplay', cvpHandlers.videoCanPlayHandler);
        window.removeEventListener('resize', cvpHandlers.windowResizeHandler);

        if (this.options.audio) {
            this.audio.parentNode.removeChild(this.audio);
        }
    };
};

CanvasVideoPlayer.prototype.updateProgress = function() {
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

CanvasVideoPlayer.prototype.updateTimeline = function() {
    var percentage = (this.video.currentTime * 100 / this.video.duration).toFixed(2);
    this.timelinePassed.style.width = percentage + '%';

    this.graph.set_position( this.frame_index() );
};

CanvasVideoPlayer.prototype.setCanvasSize = function() {
    this.width  = this.canvas.clientWidth;
    this.height = this.canvas.clientHeight;

    this.canvas.setAttribute('width',  this.width);
    this.canvas.setAttribute('height', this.height);
};

CanvasVideoPlayer.prototype.play = function() {
    this.lastTime = Date.now();
    this.playing = true;
    this.loop();

    if (this.options.audio) {
        // Resync audio and video
        this.audio.currentTime = this.video.currentTime;
        this.audio.play();
    }
};

CanvasVideoPlayer.prototype.pause = function() {
    this.playing = false;

    if (this.options.audio) {
        this.audio.pause();
    }
};

CanvasVideoPlayer.prototype.playPause = function() {
    if (this.playing) {
        this.pause();
    }
    else {
        this.play();
    }
};

CanvasVideoPlayer.prototype.loop = function() {
    var self = this;

    var time = Date.now();
    var elapsed = (time - this.lastTime) / 1000;

    // Render
    if(elapsed >= (1 / this.options.framesPerSecond)) {
        this.video.currentTime = this.video.currentTime + elapsed;
        this.lastTime = time;
        // Resync audio and video if they drift more than 300ms apart
        if(this.audio && Math.abs(this.audio.currentTime - this.video.currentTime) > 0.3){
            this.audio.currentTime = this.video.currentTime;
        }
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
        this.animationFrame = requestAnimationFrame(function(){
            self.loop();
        });
    }
    else {
        cancelAnimationFrame(this.animationFrame);
    }
};

CanvasVideoPlayer.prototype.current_draws = function() {
    var idx = this.frame_index();
    
    if( idx>=this.draws.length ) return undefined;
    return this.draws[idx];
};

CanvasVideoPlayer.prototype.frame_index = function() {
    return (this.video.currentTime*this.options.framesPerSecond) | 0;
};

CanvasVideoPlayer.prototype.circle = function(x,y,radius,color) {
    
};

CanvasVideoPlayer.prototype.line = function(x,y,xx,yy,color) {
    this.ctx.beginPath();
    this.ctx.moveTo(x,y);
    this.ctx.lineTo(xx,yy);
    this.ctx.stroke();
};

CanvasVideoPlayer.prototype.contours = function(contours,color) {
    
};

CanvasVideoPlayer.prototype.rect = function(x,y,xx,yy,color) {
    
};

CanvasVideoPlayer.prototype.drawFrame = function() {
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
