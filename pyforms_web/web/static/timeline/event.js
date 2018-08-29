class TimelineEvent{

    constructor(title, begin, end, color, track){
        this.title = title;
        this.begin = begin;
        this.end   = end;
        this.color = color?color:track.color;
        this.track = track;

        this.ctx = track.timeline.ctx;
        this.timeline = track.timeline;
    }

    draw(){
        var x  = this.timeline.frame2x(this.begin);
        var xx = (this.end-this.begin)*this.timeline.zoom;

        this.ctx.globalAlpha = 0.6;
        this.ctx.fillStyle   = this.color;
        this.ctx.fillRect(x, this.track.start_y+2, xx, this.track.timeline.options.y_step-3);
        this.ctx.globalAlpha = 1;

        this.ctx.fillStyle   = '#333';
        this.ctx.fillText(this.title, x+2, this.track.start_y+this.track.timeline.options.y_step/2);
    }
}