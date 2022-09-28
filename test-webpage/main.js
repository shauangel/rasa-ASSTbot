//rasa webhook url
let myURL = "http://0.0.0.0:5005/webhooks/rest/webhook";

//send request to rasa
function send_to_bot(){
	
	var msg = $("#user_input").val();
	//display user input
    document.getElementById("content").innerHTML += '<font color="blue">'+$("#user_input").val()+'</font><br>';
    
	msg = encodeURI(msg); //ch to unicode
	
    //request msg
	var data = {"sender" : "tester", 
			    "message" : msg};
	
    console.log("rq: "+msg);
    $.ajax({
        url: myURL,
        type: "POST",
		data: data,
        dataType: "json",
        contentType: 'application/json; charset=utf-8',
        success: function(response){
            console.log(response.text);
            document.getElementById("content").innerHTML += '<font color="black">'+response.text+'</font><br>';
            $("#user_input").val("");
        },
        error: function(){
            console.log("error");
        }
    });
}

//window.addEventListener("load", start, false);