
class BaseControlStreaming extends ControlBase{

    xmlhttp = undefined;

    stream_end(){
        super.stream_end();
    }

    stream_update(oEvent){
        this.set_value(oEvent.target.responseText);
    }

    deserialize(data) {
        super.deserialize(data);

        if(this.properties.abort_streaming===true) {
            if( this.xmlhttp ){
                this.xmlhttp.abort()
            }
            this.xmlhttp = undefined;
        }
        if(this.properties.start_streaming===true){
            this.xmlhttp = new XMLHttpRequest();
            this.xmlhttp.addEventListener('load', this.stream_end);
            this.xmlhttp.addEventListener('progress', (evt) => this.stream_update(evt), false);
            this.xmlhttp.open("get", `/pyforms/field-stream/${this.app_id()}/${this.name}/`, true);
            this.xmlhttp.send();
        }
    }
}

