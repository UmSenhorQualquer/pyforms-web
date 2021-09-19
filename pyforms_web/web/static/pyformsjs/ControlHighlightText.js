class ControlHighlightText extends ControlBase {

    init_control() {
        var html = `<div id='${this.place_id()}' class='field control ControlTextArea' >
		    <div class="ui compact menu  blue">
              <a class="item"> <i class="comment alternate outline icon"></i> Annotate </a>
              <a class="item"> <i class="i cursor icon"></i> Mark </a>
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

        var self = this;
        this.jquery().change(function () {
            self.basewidget.fire_event(this.name, 'update_control_event');
        });

        if(this.properties.error) this.jquery_place().addClass('error'); else this.jquery_place().removeClass('error');
		if(this.properties.required) this.set_required();

		document.onmouseup = document.onkeyup = function() {
            var selection = self.getSelectionText();
            if(selection){
                self.highLightText(
                    self.get_value(),
                    selection[0],
                    selection[1]
                );
                console.debug(selection);
            }
        };

		this.jquery_place().find('.menu .item').click(function(evt) {
		    $(this).parents().find('.menu .item').removeClass('active');
		    $(this).addClass('active');
        });
    };

    highLightText(text, start, end) {
        var newText = text.slice(0, start) + '<mark>' + text.slice(start, end) + '</mark>' + text.slice(end);
        this.set_value(newText)
    }


    getSelectionText() {
        var text = "";
        var activeEl = document.activeElement;
        var activeElTagName = activeEl ? activeEl.tagName.toLowerCase() : null;
        if (
          (activeElTagName == "textarea") || (activeElTagName == "input" &&
          /^(?:text|search|password|tel|url)$/i.test(activeEl.type)) &&
          (typeof activeEl.selectionStart == "number")
        ) {
            return [activeEl.selectionStart, activeEl.selectionEnd];
        } else if (window.getSelection) {
            var range = window.getSelection().getRangeAt(0),
            span = document.createElement('b');
            span.className = 'highlight';
            span.appendChild(range.extractContents());
            range.insertNode(span);
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

