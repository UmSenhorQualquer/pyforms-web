class ControlHighlightText extends ControlBase {

    init_control() {
        var html = `<div id='${this.place_id()}' class='field control ControlTextArea' >
		    <div class="ui compact mini menu blue toolbar" style="position: absolute; display: none; z-index: 999" >
              <a class="item mark"> <i class="i cursor icon"></i></a>
              <a class="item annotate"> <i class="comment alternate outline icon"></i></a>
            </div>
            <div class="ui compact mini menu blue toolbar-remove" style="position: absolute; display: none; z-index: 999" >
              <a class="item remove"> <i class="window close outline icon"></i></a>
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


        if(this.properties.error) this.jquery_place().addClass('error'); else this.jquery_place().removeClass('error');
		if(this.properties.required) this.set_required();

		// Setup the highlight and comment behavior
        this.count = 0;
		this.selection = undefined;
		var self = this;

        this.jquery_place().find('.toolbar .annotate').click( evt => {
            if( this.selection ){
                this.highLightText(this.selection);
                self.jquery_place().find('.toolbar').hide();
            }
        });

        this.jquery_place().find('.toolbar .mark').click( evt => {
            if( this.selection ){
                this.highLightText(this.selection);
                self.jquery_place().find('.toolbar').hide();
            }
        });

        this.jquery_place().find('.toolbar .clear').click( evt => {
            if( this.selection ){
                this.clearText(this.selection);
                self.jquery_place().find('.toolbar').hide();
            }
        });


		$(document).mouseup(function(evt) {

		    var selection = self.getSelectionText();
		    if(selection && selection.startOffset!==selection.endOffset){
		        console.debug(selection);
                var pos = self.jquery_place().offset();
                self.selection = selection;
                self.jquery_place().find('.toolbar').css({
                    left: evt.pageX - pos.left + 50,
                    top: evt.pageY - pos.top + 50
                }).show();
            }else{
		        var pos = self.jquery_place().offset();
		        self.selection = undefined;
                self.jquery_place().find('.toolbar').hide();
                self.jquery_place().find('.toolbar-remove').hide();
            }
        });

		this.jquery_place().find('.menu .item').click(function() {
		    $(this).parents().find('.menu .item').removeClass('active');
		    $(this).addClass('active');
        });
    };

    highLightText(range) {
        //var newText = text.slice(0, start) + '<mark>' + text.slice(start, end) + '</mark>' + text.slice(end);
        //this.set_value(newText)
        var span = document.createElement('b');
        //span.className = 'highlight';
        span.id = 'h'+this.count;
        span.appendChild(range.extractContents());
        range.insertNode(span);

        var self = this;

        $("#h"+this.count).click(function (evt){
            $(this).replaceWith($(this).html());
            var pos = self.jquery_place().offset();
            self.jquery_place().find('.toolbar').hide();
            self.jquery_place().find('.toolbar-remove').css({
                left: evt.pageX - pos.left + 50,
                top: evt.pageY - pos.top + 50
            }).show();
        });
        this.count++;

    }

    clearText(range) {
        //var newText = text.slice(0, start) + '<mark>' + text.slice(start, end) + '</mark>' + text.slice(end);
        //this.set_value(newText)
        $(range.extractContents()).find('span').remove();
        //var span = document.createElement('b');
        //span.className = 'highlight';
        var contents = range.extractContents();
        //span.appendChild(range.extractContents());
        //console.debug(range.extractContents());
        contents.removeChild(contents.querySelectorAll('span.highlight'));
        range.insertNode(contents);
    }


    getSelectionText() {
        var activeEl = document.activeElement;
        var activeElTagName = activeEl ? activeEl.tagName.toLowerCase() : null;
        if (
          (activeElTagName == "textarea") || (activeElTagName == "input" &&
          /^(?:text|search|password|tel|url)$/i.test(activeEl.type)) &&
          (typeof activeEl.selectionStart == "number")
        ) {
            return [activeEl.selectionStart, activeEl.selectionEnd];
        } else if (window.getSelection) {
            return window.getSelection().getRangeAt(0);
        }
        return undefined;
    }

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

