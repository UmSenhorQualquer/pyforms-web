function ControlItemList(name, properties) {
    ControlBase.call(this, name, properties);
};
ControlItemList.prototype = Object.create(ControlBase.prototype);


////////////////////////////////////////////////////////////////////////////////

ControlItemList.prototype.get_value = function () {
    return this.properties.value;
};

////////////////////////////////////////////////////////////////////////////////

ControlItemList.prototype.init_control = function () {
    var html = '<div class="ui container" id="' + this.place_id() + '"  >';
    html += '<div class="ui relaxed divided items">';
    html += '<div class="ui small image">';
    html += '<img src="assets/images/wireframe/server.svg">';
    html += '</div>';
    html += '<div class="content">';
    html += '<a class="header">' + this.properties.hname + '</a>';

    html += '<div class="meta">';
    specs = this.properties.specs;
    for (var i = 0; i < specs.length; i++) {
        html += '<a>' + specs[i] + '</a>';
    }
    html += '</div>';

    html += '<div class="description">';
    options = this.properties.options;
    for (var i = 0; i < options.length) {
        html += '<p><b>' + options[i][0] + ':</b> ' + options[i][1] + '</p>';
    }
    html += '</div>';

    html += '</div>';
    html += '</div>';
    html += '</div>';
    html += '</div>';
    html += '<div class="ui divider"></div>'

    this.jquery_place().replaceWith(html);


    if (!this.properties.visible) this.hide();
};

////////////////////////////////////////////////////////////////////////////////

ControlItemList.prototype.set_value = function (value) {
    this.init_control();
};

////////////////////////////////////////////////////////////////////////////////
