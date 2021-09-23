class ControlHighlightText extends ControlBase {

    init_control() {
        var html = `<div id='${this.place_id()}' class='field control ControlHighlightText' >
            <div class="ui compact mini menu blue toolbar-edit" style="position: absolute; display: none; z-index: 999" >
              <a class="item remove"> <i class="window close outline icon"></i></a>
              <a class="item comment"> <i class="comment alternate outline icon"></i></a>
            </div>
            <br/>
            <br/>
		    <label for='${this.control_id()}'>${this.properties.label}</label>
		    <div placeholder='${this.properties.placeholder}' type='text'
		    rows='${this.properties.rows}' cols='${this.properties.cols}'
		    name='${this.name}' id='${this.control_id()}' ></div>
		</div>`;
        this.jquery_place().replaceWith(html);
        this.set_value(this.properties.value);

        var hltr = new TextHighlighter(
            $('#'+this.control_id())[0],
            {
                onAfterHighlight: elems =>{
                    $('.highlighted').unbind("click");
                    $('.highlighted').click(evt => {
                        var pos = this.jquery_place().offset();
                        this.jquery_place().find('.toolbar-edit').css({
                            left: evt.pageX - pos.left , top: evt.pageY - pos.top + 45
                        }).show();
                        this.jquery_place().find('.toolbar-edit .remove').unbind('click');
                        this.jquery_place().find('.toolbar-edit .remove').click(e=>{
                            hltr.removeHighlights(evt.currentTarget);
                            this.jquery_place().find('.toolbar-edit').hide();
                        });
                    });
                }
            }
        );



        if(this.properties.error) this.jquery_place().addClass('error'); else this.jquery_place().removeClass('error');
		if(this.properties.required) this.set_required();



		this.jquery_place().find('.menu .item').click(function() {
		    $(this).parents().find('.menu .item').removeClass('active');
		    $(this).addClass('active');
        });
    };

    ////////////////////////////////////////////////////////////////////////////////

    /**
    Enable the control.
    */
    enable(){
        this.jquery().removeAttr('readonly');
        this.jquery().removeClass('disabled');
    }

    ////////////////////////////////////////////////////////////////////////////////

    /**
    Disable the control.
    */
    disable(){
        this.jquery().attr('readonly', 'readonly');
        this.jquery().addClass('disabled');
    }

    ////////////////////////////////////////////////////////////////////////////////

    /**
    Sets the value of the control.
    @param {object} value - Value to set.
    */
    set_value(value){
        if(this.jquery().length>0)
            if(this.properties.value!=null)
                this.jquery().html(this.properties.value);
            else
                this.jquery().html('');
    }

    get_value(){
        if(this.jquery().length==0) return this.properties.value;
        var value = this.jquery().html();
        if(value=='null') return null;
        else return value;
    }
}

