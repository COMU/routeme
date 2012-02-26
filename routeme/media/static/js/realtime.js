onmessage = function (data) {
    if (window.location.pathname == "/message/inbox/"){
	location.reload();
    }else{
        $('#unread').html(data);
    }
};

onclose = function (){
}
socket = io.connect("http://localhost:8090");

socket.on('connect', function (){
    $.get("/email/username/", function(data){
        socket.emit("adduser", data.username);
    });
});

socket.on('message', onmessage);
socket.on('disconnect', onclose);
