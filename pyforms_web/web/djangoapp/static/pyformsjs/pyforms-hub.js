function error_msg(msg){
	// 
	alert(msg);
};

function run_application(application, parameters){
	// run a aplication
	$.ajax({
		method: 'get',
		cache: false,
		dataType: "json",
		data: parameters,
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
	var hash 	 = window.location.hash;
	if(hash.length==0) return;

	if(hash.slice(0,2)!='#/') return;

	var commands = hash.split("/");
	var app 	 = commands[1];
	var func 	 = commands.length>2?commands[2]:undefined;
	var params   = commands.length>3?commands.slice(3):undefined;
	var data 	 = { method: func, parameters: params };

	console.log(data);
	run_application(app, data);
};



$(pyforms_checkhash);
$(window).bind('hashchange',pyforms_checkhash);