class ControlSearch extends ControlBase {

    ////////////////////////////////////////////////////////////////////////////////

    get_value() {
        return this.properties.value;
    };

    ////////////////////////////////////////////////////////////////////////////////

    init_control() {
        var html = `<div class="ui field '${this.properties.css}' control ControlSearch" id="${this.place_id()}"  >
            <div ${this.control_id()} class="ui labeled icon top right pointing dropdown button">
              <i class="filter icon"></i>
              <span class="text">Filter Posts</span>
              <div class="menu">
                <div class="ui search icon input">
                  <i class="search icon"></i>
                  <input type="text" name="search" placeholder="Search issues...">
                </div>
                <div class="divider"></div>
                <div class="header">
                  <i class="tags icon"></i>
                  Filter by tag
                </div>
                <div class="item">
                  <div class="ui red empty circular label"></div>
                  Important
                </div>
                <div class="item">
                  <div class="ui blue empty circular label"></div>
                  Announcement
                </div>
                <div class="item">
                  <div class="ui black empty circular label"></div>
                  Discussion
                </div>
                <div class="divider"></div>
                <div class="header">
                  <i class="calendar icon"></i>
                  Filter by date
                </div>
                <div class="item">
                  <i class="olive circle icon"></i>
                  This Week
                </div>
                <div class="item">
                  <i class="violet circle icon"></i>
                  This Month
                </div>
                <div class="item">
                  <i class="orange circle icon"></i>
                  This Year
                </div>
              </div>
            </div>
        </div>`;
        this.jquery_place().replaceWith(html);

        // get the items from an url
        this.jquery().dropdown({
            apiSettings: { url: this.properties.items_url },
            saveRemoteData:   false,
            placeholder: false,
            forceSelection: false
        });
		if(this.properties.required) this.set_required();
    };

    ////////////////////////////////////////////////////////////////////////////////

    set_value(value) {
        this.init_control();
    };

    ////////////////////////////////////////////////////////////////////////////////

}
