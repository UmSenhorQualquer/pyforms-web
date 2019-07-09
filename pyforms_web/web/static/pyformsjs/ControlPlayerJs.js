class ControlPlayerJs extends ControlBase{
    
    init_control(){
        var html = `
            <div id='`+this.place_id()+`' class='field control ControlPlayerJs' >
                <video class="video" id="`+this.control_id()+`" muted >
                    <source src="`+this.properties.value+`">
                    Your browser does not support HTML5 video.
                </video>
                <div style='background-color:black' ><canvas class="canvas" id="canvas-`+this.control_id()+`" ></canvas></div>
                <div class="video-timeline" id="timeline-`+this.control_id()+`" >
                    <div class="video-timeline-passed"></div>
                    <div class="video-timeline-loaded"></div>
                </div>
                <div class='video-graph'></div>
            <div>`;

        this.jquery_place().replaceWith(html);

        var self = this;
        
        $(document).ready(function(){
            self.video = new CanvasVideoPlayer({
                playerSelector:     '#'+self.place_id(),
                videoSelector:      '#'+self.control_id(),
                canvasSelector:     '#canvas-'+self.control_id(),
                timelineSelector:   '#timeline-'+self.control_id(),
                audio: false,
                video_width: self.properties.video_width,
                video_height: self.properties.video_height,
                draws_url: self.properties.draws_url
            });
        });
		if(this.properties.required) this.set_required();
    };

    ////////////////////////////////////////////////////////////////////////////////

    load_data(){ 
        if(!this.properties.data_url) return;

        var self = this;
        $.ajax({
            method: 'get',
            cache: false,
            dataType: "json",
            url: this.properties.data_url+'?nocache='+$.now(),
            contentType: "application/json; charset=utf-8",
            success: function(res){

                if(res.graphs){
                    for(var i in res.graphs)
                        self.video.add_graph(res.graphs[i].title, res.graphs[i].data, res.graphs[i].color);
                }

                if(res.events){
                    for(var i in res.events)
                        self.video.add_event(res.events[i][0], res.events[i][1], res.events[i][2], res.events[i][3], res.events[i][4]);
                    self.video.draw_timeline();
                }
                
            }
        }).always(function() {
            self.properties.data_url = undefined;
        });
    };
    ////////////////////////////////////////////////////////////////////////////////


    get_value(){ 
        return null;
    };

    ////////////////////////////////////////////////////////////////////////////////

    set_value(value){
        this.video.open(value);
    };

    ////////////////////////////////////////////////////////////////////////////////

    update_server(){
        return false;
    }

    ////////////////////////////////////////////////////////////////////////////////

    deserialize(data){
        super.deserialize(data);
        this.load_data();
    }
}