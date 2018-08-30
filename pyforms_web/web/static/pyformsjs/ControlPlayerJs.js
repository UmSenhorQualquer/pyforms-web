class ControlPlayerJs extends ControlBase{
    
    init_control(){
        this.set_value(this.properties.value);
    };

    ////////////////////////////////////////////////////////////////////////////////

    get_value(){ 
        this.properties.video_index = $( "#timeline"+this.control_id()).val();
        return this.properties.value; 
    };

    ////////////////////////////////////////////////////////////////////////////////

    set_value(value){
        if( this.canvasVideo ) this.canvasVideo.unbind();

        var html = `
            <div id='`+this.place_id()+`' class='field control ControlPlayerJs' >
                <video class="video" id="`+this.control_id()+`" muted >
                    <source src="`+this.properties.value+`">
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

        var self = this;
        $(document).ready(function(){
            self.canvasVideo = new CanvasVideoPlayer({
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