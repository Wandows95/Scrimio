$(document).ready(function(){$('.expand-button').click(function(){$('.expandable').slideToggle('slow');});});$(document).ready(function(){var exampleSocket=new WebSocket("ws://127.0.0.1:8000/user/sockets/login/");});