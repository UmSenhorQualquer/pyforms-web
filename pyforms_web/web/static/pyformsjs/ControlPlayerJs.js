class ControlPlayerJs extends ControlBase{
    
    init_control(){
        var html = `
            <div id='`+this.place_id()+`' class='field control ControlPlayerJs' >
                <video class="video" id="`+this.control_id()+`" muted >
                    <source src="`+this.properties.value+`" type="video/mp4">
                    Your browser does not support HTML5 video.
                </video>
                <canvas class="canvas" id="canvas-`+this.control_id()+`" ></canvas>
                <div class="video-timeline" id="timeline-`+this.control_id()+`" >
                    <div class="video-timeline-passed"></div>
                    <div class="video-timeline-loaded"></div>
                </div>
                <div class='video-graph'></div>
            <div>`;

        this.jquery_place().replaceWith(html);

        var canvasVideo = new CanvasVideoPlayer({
            playerSelector:     '#'+this.place_id(),
            videoSelector:      '#'+this.control_id(),
            canvasSelector:     '#canvas-'+this.control_id(),
            timelineSelector:   '#timeline-'+this.control_id(),
            audio: false,
            video_width: this.properties.video_width,
            video_height: this.properties.video_height,
            draws_url: this.properties.draws_url
        });

        var self = this;
        $( "#timeline"+this.control_id() ).change(
            function(){ self.basewidget.fire_event( self.name, 'refresh' ); }
        );  
    };

    ////////////////////////////////////////////////////////////////////////////////

    get_value(){ 
        this.properties.video_index = $( "#timeline"+this.control_id()).val();
        return this.properties.value; 
    };

    ////////////////////////////////////////////////////////////////////////////////

    set_value(value){
        $( "#"+this.control_id()+' source').attr("src", value);
    };

    ////////////////////////////////////////////////////////////////////////////////

    update_server(){
        return this.properties.video_index != $( "#timeline"+this.control_id() ).val()
    }

    ////////////////////////////////////////////////////////////////////////////////

    serialize(){
        super.serialize();
        this.properties.base64content = null;
        return this.properties;
    }

}