function error_msg(msg){
	// 
	alert(msg);
};

function run_application(application, constructor_params, method_params){
	// run a aplication
	var data2send = {};
	if(method_params) 		data2send['method'] 	 = method_params;
	if(constructor_params) 	data2send['constructor'] = constructor_params;
	
	data2send = $.toJSON(data2send);

	$.ajax({
		method: 'post',
		cache: false,
		dataType: "json",
		data: data2send,
		url: '/pyforms/app/register/'+application+'/?nocache='+$.now(),
		contentType: "application/json; charset=utf-8",
		success: function(res){
			if( res.result=='error' )
				error_msg(res.msg);
			else{
				// open all the returned applications
				for(var i=0; i<res.length; i++)
					pyforms.open_application(res[i]);				
			};
		}
	}).fail(function(xhr){
		error_msg(xhr.status+" "+xhr.statusText+": "+xhr.responseText);
	});
};


function pyforms_checkhash(){
	//example: #/<class_fullname>/?<parameter name for the constructor>=<parameter value>   pass the parameter for the constructor
	//example call method: #/<class_fullname>/<method to call>/<name of the method to call>/<parameter name for the method>/<parameter value>/
	
	var hash = window.location.hash;
	if(hash.length==0) return;
	if(hash.slice(0,2)!='#/') return;
	
	var commands = hash.split("/");
	var app 	 = commands[1];
	var func 	 = (commands.length>2 && commands[2][0]!='?')?commands[2]:undefined;
	//find the method to execute and the method parameters

	if(!app) return; //the app was not defined

	var method_data = {};
	if( func ){
		method_data['method'] = func;
		method_data['params'] = {};
		for(var i=3; i<commands.length; i+=2){
			method_data['params'][commands[i]]=commands[i+1];
		};
	};

	//find the parameters for the app constructor
	var constructor_data = {}
	var query = hash.split('?');
	var search = '';
	if(query.length>=2) search = query[1];
	search.replace(/([^=&]+)=([^&]*)/g, function(m, key, value) {
		constructor_data[decodeURIComponent(key)] = decodeURIComponent(value);
	}); 
	
	run_application(app, constructor_data, method_data);
};



$(pyforms_checkhash);
$(window).bind('hashchange',pyforms_checkhash);