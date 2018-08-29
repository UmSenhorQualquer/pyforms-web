class TimelineTrack{

    constructor(row, title, color, timeline){
        this.row      = row;
        this.title    = title;
        this.color    = color?color:'red';
        this.timeline = timeline;

        this.events = []

        this.start_y = timeline.options.top_margin + row*timeline.options.y_step;
        this.end_y   = timeline.options.top_margin + (row+1)*timeline.options.y_step;
    }

    add_event(title, begin, end, color){
        var evt = new TimelineEvent( title, begin, end, color , this);

        if( this.events.length==0 ) 
            this.events.push(evt)
        else{
            var b = 0;
            var e = this.events.length-1;
            var idx = 0;

            while( true ){
                idx = (b+(e-b)/2) | 0;
                if( (e-b)<=1 ){
                    if( begin>this.events[idx].begin )
                        idx++;
                    this.events.splice(idx, 0, evt);
                    break;
                }

                if( begin<this.events[idx].begin )
                    e = idx;
                else
                    b = idx;
            }
        }        
    }

    draw(){
        var begin = this.timeline.offset;
        var end   = this.timeline.offset+this.timeline.width;

        for(var i in this.events)
            if( begin<=this.events[i].begin<=end || begin<=this.events[i].end<=end ){
                this.events[i].draw();
            }
    }


}