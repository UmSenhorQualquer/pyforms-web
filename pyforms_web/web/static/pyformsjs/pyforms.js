

var PYFORMS_CHECKER_LOOP_INTERVAL = 1000;

(function($) {
  $.getStylesheet = function(href) {
    var $d = $.Deferred();
    var $link = $('<link/>', {
       rel: 'stylesheet',
       type: 'text/css',
       href: href
    }).appendTo('head');
    $d.resolve($link);
    return $d.promise();
  };
})(jQuery);


$.ajaxSetup({cache:true});
if(typeof(loading)!="function")     var loading = function(){};
if(typeof(not_loading)!="function") var not_loading = function(){};


class PyformsManager{
    /**
     PyformsManager is the class than manages all the pyforms client side interaction.
     */

    constructor(){
        this.loop_checks  = [];
        this.loop         = undefined;

        this.layout_places = [];

        this.applications = [];
        $.ajaxSetup({async: false, cache: true});

        $.getStylesheet("/static/pyforms.css");
        $.getScript("/static/jquery.json-2.4.min.js");
        $.getScript("/static/base64.js");
        $.getScript("/static/gmaps.min.js");
        $.getScript("/static/pyformsjs/ControlBase.js");
        $.getScript("/static/pyformsjs/ControlAutoComplete.js");
        $.getScript("/static/pyformsjs/ControlText.js");
        $.getScript("/static/pyformsjs/ControlTextArea.js");
        $.getScript("/static/pyformsjs/ControlBreadcrumb.js");
        $.getScript("/static/pyformsjs/ControlButton.js");
        $.getScript("/static/pyformsjs/ControlFile.js");
        $.getScript("/static/pyformsjs/ControlFileUpload.js");
        $.getScript("/static/pyformsjs/ControlDir.js");
        $.getScript("/static/pyformsjs/ControlMultipleChecks.js");
        $.getScript("/static/pyformsjs/ControlMultipleSelection.js");
        $.getScript("/static/pyformsjs/ControlSlider.js");
        $.getScript("/static/pyformsjs/ControlCheckBox.js");
        $.getScript("/static/pyformsjs/ControlCheckBoxList.js");
        $.getScript("/static/pyformsjs/ControlCheckBoxListQuery.js");
        $.getScript("/static/pyformsjs/ControlTemplate.js");
        $.getScript("/static/pyformsjs/ControlCombo.js");
        $.getScript("/static/pyformsjs/ControlInteger.js");
        $.getScript("/static/pyformsjs/ControlFloat.js");
        $.getScript("/static/pyformsjs/ControlCalendar.js");
        $.getScript("/static/pyformsjs/ControlPieChart.js");
        $.getScript("/static/pyformsjs/ControlDate.js");
        $.getScript("/static/pyformsjs/ControlDateTime.js");
        $.getScript("/static/pyformsjs/ControlImage.js");
        $.getScript("/static/pyformsjs/ControlImg.js");
        $.getScript("/static/pyformsjs/ControlHtml.js");
        $.getScript("/static/pyformsjs/ControlEmail.js");
        $.getScript("/static/pyformsjs/ControlItemsList.js");
        $.getScript("/static/pyformsjs/ControlList.js");
        $.getScript("/static/pyformsjs/ControlQueryCombo.js");
        $.getScript("/static/pyformsjs/ControlQueryList.js");
        $.getScript("/static/pyformsjs/ControlFeed.js");    
        $.getScript("/static/pyformsjs/ControlQueryCards.js");
        $.getScript("/static/pyformsjs/ControlPassword.js");
        $.getScript("/static/pyformsjs/ControlPlayer.js");
        $.getScript("/static/pyformsjs/ControlProgress.js");
        $.getScript("/static/pyformsjs/ControlBoundingSlider.js");
        $.getScript("/static/pyformsjs/ControlVisVis.js");
        $.getScript("/static/pyformsjs/ControlLabel.js");
        $.getScript("/static/pyformsjs/ControlSimpleLabel.js");
        $.getScript("/static/pyformsjs/ControlTimeout.js");
        $.getScript("/static/pyformsjs/ControlEmptyWidget.js");
        $.getScript("/static/pyformsjs/ControlMenu.js");
        $.getScript("/static/pyformsjs/ControlWorkflow.js");
        $.getScript("/static/pyformsjs/BaseWidget.js");


        $.getScript("/static/jquery.flowchart/jquery.panzoom.min.js");
        $.getScript("/static/jquery.flowchart/jquery.mousewheel.min.js");
        $.getScript("/static/jquery.flowchart/jquery.flowchart.min.js");
        $.getStylesheet("/static/jquery.flowchart/jquery.flowchart.min.css");

        $.getScript("/static/datetimepicker/jquery.datetimepicker.full.min.js");
        $.getStylesheet("/static/datetimepicker/jquery.datetimepicker.min.css");

        $.getScript("/static/jqplot/jquery.jqplot.js");
        $.getScript("/static/jqplot/plugins/jqplot.cursor.js");
        $.getScript("/static/jqplot/plugins/jqplot.logAxisRenderer.js");
        $.getScript("/static/jqplot/plugins/jqplot.canvasTextRenderer.js");
        $.getScript("/static/jqplot/plugins/jqplot.canvasAxisLabelRenderer.js");
        $.getScript("/static/jqplot/plugins/jqplot.blockRenderer.js");
        $.getScript("/static/jqplot/plugins/jqplot.enhancedLegendRenderer.js");
        $.getScript("/static/jqplot/plugins/jqplot.logAxisRenderer.js");
        $.getScript("/static/jqplot/plugins/jqplot.dateAxisRenderer.js");
        $.getScript("/static/jqplot/plugins/jqplot.categoryAxisRenderer.js");
        $.getScript("/static/jqplot/plugins/jqplot.barRenderer.js");
        $.getScript("/static/jqplot/plugins/jqplot.pointLabels.js");
        $.getScript("/static/jqplot/plugins/jqplot.pieRenderer.js");
        $.getStylesheet("/static/jqplot/jquery.jqplot.css");

        $.getScript("/static/filer/js/jquery.filer.js");
        $.getStylesheet("/static/filer/css/jquery.filer.css");
        $.getStylesheet("/static/filer/css/jquery.filer-dragdropbox-theme.css");

        $.ajaxSetup({async: true, cache: false});


        setInterval(this.garbage_collector, 5000); //Run the garbage collector for times to times.
    }

    ////////////////////////////////////////////////////////////


    /**
    Add an app to the manager.
    @param {BaseWidget} app - BaseWidget instance.
    */
    add_app(app){
        
        //remove the application first
        for(var i=0; i<this.applications.length; i++)
            if( this.applications[i]!=undefined && this.applications[i].widget_id==app.widget_id ){
                this.applications[i].close_sub_apps();
                delete this.applications[i];
                this.applications.slice(i,1);
                break;
            }

        this.applications.push(app);
    }

    ////////////////////////////////////////////////////////////

    /**
    Remove an app from the manager. If the app_index parameter is not defined it will search for the index using the app_id parameter.

    @param {str} app_id - BaseWidget id.
    @param {int} app_index - BaseWidget index (optional).
    */
    remove_app(app_id, app_index){
        var app = null;
        if(app_index==undefined)
            for(var i=0; i<this.applications.length; i++)
                if( this.applications[i]!=undefined && this.applications[i].widget_id==app_id )
                    app_index = i;
                
        app = this.applications[app_index];
        if(app!=undefined && app!=null){
            $.ajax({
                method: 'get',
                cache: false,
                dataType: "json",
                url: '/pyforms/app/remove/'+app.widget_id+'/?nocache='+$.now(),
                contentType: "application/json; charset=utf-8"
            }).always(function(){
                app.close();
                delete pyforms.applications[app_index];
                pyforms.applications.slice(app_index,1);
            });
        }
    };


    ////////////////////////////////////////////////////////////
    /**
    Search an app using the id.
    @param {str} app_id - BaseWidget id.
    */
    find_app(app_id){
        for(var i=0; i<this.applications.length; i++){
            if( this.applications[i]!=undefined && this.applications[i].widget_id==app_id )
                return this.applications[i];

        }
        return undefined;
    };

    /**
    Search for a control by its id.
    @param {str} control_id - Control id.
    */
    find_control(control_id){
        var ids             = this.split_id(control_id);
        var widget_id       = ids[0];
        var control_name    = ids[1];

        var widget = this.find_app(widget_id);
        return widget.find_control(control_name);
    };


    /**
    Parse the control id
    @param {str} control_id - Control id.
    @returns {list(str)} [widget_id, control_name]
    */
    split_id(control_id){
        var split_in        = control_id.lastIndexOf("-");
        var widget_id       = control_id.substring(0, split_in);
        var control_name    = control_id.substring(split_in+1);

        return [widget_id, control_name];
    };


    /**
    Contact the server to submit and receive updates.

    @param {BaseWidget} basewidget - BaseWidget object.
    @param {object} data2send - Object with the data to send.
    @param {bool} show_loading - Flag to activate the app loading (optional).
    */
    query_server(basewidget, data2send, show_loading){
        if(data2send===undefined)       data2send = {};
        if(show_loading===undefined)    show_loading = true;

        if(basewidget.parent_id!==undefined){
            // if the widget is a child of another widget
            var parent_widget = basewidget.parent_widget();
            this.query_server(parent_widget, data2send);
        }else{
            if(show_loading) basewidget.loading();
            data2send = basewidget.serialize_data(data2send);
            
            var jsondata =  $.toJSON(data2send);
            var self = this;
            
            $.ajax({
                method: 'post',
                cache: false,
                dataType: "json",
                url: '/pyforms/app/update/'+basewidget.widget_id+'/?nocache='+$.now(),
                data: jsondata,
                contentType: "application/json; charset=utf-8",
                success: function(res){
                    if( res.result=='error' )
                        error_msg(res.msg);
                    else{
                        $.ajaxSetup({async: false, cache: true});
                        for(var i=0; i<res.length; i++){
                            self.open_application(res[i]);                      
                        };
                        $.ajaxSetup({async: true, cache: true});
                    };
                }
            }).fail(function(xhr){
                error_msg(xhr.status+" "+xhr.statusText+": "+xhr.responseText);
            }).always(function(){
                if(show_loading) basewidget.not_loading();
            });

            // check if there are more events to process ///////////////////////////
            if(  basewidget.events_queue.length>0 ) 
                this.query_server(basewidget, basewidget.events_queue.pop(0) );
            ////////////////////////////////////////////////////////////////////////
        }
    }


    /**
    Check what it does
    */
    register_checkloop(check_event){
        this.loop_checks.push(check_event);
        if(this.loop===undefined){
            this.loop = setInterval(pyforms.checker_loop, PYFORMS_CHECKER_LOOP_INTERVAL);
        };
    };

    /**
    check what it do
    */
    checker_loop(){

        for(var i=pyforms.loop_checks.length-1; i>=0; i--){
            if( !pyforms.loop_checks[i]() ){
                pyforms.loop_checks.splice(i,1);
            }
        };
        if(pyforms.loop_checks.length==0){
            clearInterval(pyforms.loop);
            pyforms.loop = undefined;
        }
    };

    /**
    Register a new layout for the applications.

    @param {str} place_id - App id.
    @param {function} place_generator - Function that will generate the html container for the applications.
    @param {function} place_activator - Function to active the layout when it exists.
    @param {function} place_closer - Function to destroy the layout.
    */
    register_layout_place(place_id, place_generator, place_activator, place_closer){
        var insert = true;
        for(var i=0; i<this.layout_places.length; i++)
            if( this.layout_places[i].place_id == place_id ){
                this.layout_places[i].open_handler = place_generator;
                this.layout_places[i].activate_handler = place_activator;
                this.layout_places[i].close_handler = place_closer;
                insert = false;
                break;
            };
        if(insert) this.layout_places.push({
            place:place_id, open_handler:place_generator, 
            activate_handler:place_activator, close_handler: place_closer
        })
    };

    /**
    Open an application.

    @param {object} app_data - App data.
    */
    open_application(app_data){
        var app = pyforms.find_app(app_data['uid']);
        
        var layout_position = app_data['layout_position'];
        var application_id  = app_data['uid'];
        
        // if the application exists activate the layout
        if( app!=undefined){
            app.deserialize(app_data);
            
            if(!app_data['close_widget']){ 
                for(var i=0; i<this.layout_places.length; i++){
                    if( this.layout_places[i].place==layout_position && this.layout_places[i].activate_handler ){
                        this.layout_places[i].activate_handler(application_id);
                        break;
                    }
                };
            };
            
            not_loading();
            return;
        }

        
        var application_id  = app_data['uid'];
        var application_url = "/pyforms/app/open/"+application_id+"/";
        var application_title = app_data['title'];
        var found_place = false;
        for(var i=0; i<this.layout_places.length; i++){
            if( this.layout_places[i].place==layout_position ){
                this.layout_places[i].open_handler(application_id, application_title, application_url);
                found_place = true;
                break;
            }
        };

        if(!found_place){
            $.ajax({
                method:     'get',
                cache:      false,
                dataType:   "json",
                url: application_url,
                contentType: "application/json; charset=utf-8",
                success: function(res){
                    if( res.result=='error' )
                        error_msg(res.msg);
                    else{
                        var html = "<form class='ui form "+res.css+"' id='app-"+res.app_id+"' >";
                        html += res.code;
                        html += '</form>';

                        $('#'+layout_position).html(html);
                    };
                }
            }).fail(function(xhr){
                error_msg(xhr.status+" "+xhr.statusText+": "+xhr.responseText);
            }).always(function(){
                pyforms.garbage_collector();
            });
        };
    };

    /**
    Check if applications are still in use, if not remove them
    */
    garbage_collector(){
        /*
        check if the html elements of the application exists,
        otherwise remove the application.
        */
        for(var i=pyforms.applications.length-1; i>=0; i--)
            if( pyforms.applications[i]!=undefined && pyforms.applications[i].jquery().length==0 )
                pyforms.remove_app(null, i);
    };

   /**
    Close a layout.

    @param {int} layout_position - Layout id.
    */
    close_layout_place(app_data){
        var app = pyforms.find_app(app_data['uid']);
        
        var layout_position = app_data['layout_position'];
        var application_id  = app_data['uid'];
        
        if( app!=undefined)
            for(var i=0; i<this.layout_places.length; i++){
                if( this.layout_places[i].place==layout_position && this.layout_places[i].close_handler ){
                    this.layout_places[i].close_handler(application_id);
                    break;
                }
            };
    };
    
}


////////////////////////////////////////////////////////////
if(pyforms==undefined) var pyforms = new PyformsManager()
////////////////////////////////////////////////////////////
