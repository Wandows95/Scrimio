$(document).ready(function(){
	var exampleSocket = new WebSocket("ws://127.0.0.1:8000/dota/sockets/status/Monochrome/");

	exampleSocket.onmessage = function(event){
 		console.log(event.data);
	}
});