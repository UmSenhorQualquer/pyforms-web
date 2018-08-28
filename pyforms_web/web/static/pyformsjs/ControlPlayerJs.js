class ControlPlayerJs extends ControlBase{

    
    get_value(){ 
        this.properties.video_index = $( "#timeline"+this.control_id()).val();
        return this.properties.value; 
    };

    ////////////////////////////////////////////////////////////////////////////////

    set_value(value){
        if(this.properties.base64content){
            $("#display"+this.control_id()).attr("src", "data:image/png;base64,"+this.properties.base64content);
            
            $( "#timeline"+this.control_id()).val(this.properties.video_index);
            $( "#timeline"+this.control_id()).attr("min", 0);
            $( "#timeline"+this.control_id()).attr("max", this.properties.endFrame);
        }
    };

    ////////////////////////////////////////////////////////////////////////////////

    init_control(){

        var html = "<div id='"+this.place_id()+"' class='field control ControlPlayer' >";
        html += `
        <video id="example_video_1" class="video-js vjs-default-skin" controls preload="auto" width="640" height="264"
            poster="//vjs.zencdn.net/v/oceans.png"
            data-setup="{}">
          <source src="//vjs.zencdn.net/v/oceans.mp4" type='video/mp4' />
          <source src="//vjs.zencdn.net/v/oceans.webm" type='video/webm' />
          <source src="//vjs.zencdn.net/v/oceans.ogv" type='video/ogg' />
          <track kind="captions" src="captions.vtt" srclang="en" label="English"></track><!-- Tracks need an ending tag thanks to IE9 -->
          <p class="vjs-no-js">
            To view this video please enable JavaScript, and consider upgrading to a web browser that
            <a href="http://videojs.com/html5-video-support/" target="_blank">supports HTML5 video</a>
          </p>
        </video>`
        html += "<div class='ui card "+this.properties.css+"' id='card"+this.control_id()+"' >";
        html += "<div class='image'>";
        html += "<img style='width:100%;' class='image' src='data:image/png;base64,"+this.properties.base64content+"' id='display"+this.control_id()+"' />";
        html += "</div>";
        html += "<div class='content'>";
        html += "<input style='width:100%;' type='range' name='"+this.name+"' value='"+this.properties.value+"' id='timeline"+this.control_id()+"' max='"+this.properties.endFrame+"'>";
        html += "</div>";
        html += "</div>";
        html += "</div>";

        this.jquery_place().replaceWith(html);

        
        var self = this;
        $( "#timeline"+this.control_id() ).change(
            function(){ self.basewidget.fire_event( self.name, 'refresh' ); }
        );  
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