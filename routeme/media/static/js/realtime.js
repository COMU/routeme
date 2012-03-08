onmessage = function (data) {
    if (window.location.pathname == "/message/inbox/"){
	location.reload();
    }else{
    	$.get("/message/unread_count/", function(data){
            if (!$('#unread').hasClass('label')){
            	$('#unread').addClass('label');
	    }
            $('#unread').html(data.count);
    	});
    }
};

onclose = function (){
}
socket = io.connect("http://drivefor.me");

socket.on('connect', function (){
    $.get("/email/username/", function(data){
	alert("data");
        socket.emit("adduser", data.username);
    });
});

socket.on('message', onmessage);
socket.on('disconnect', onclose);

//message
var reduceUnread = function(){
   	currentValue = parseInt($('#unread').html());
        
        if ( currentValue == 1){
	     $('#unread').removeClass("label");
	     $('#unread').html('');
             return;
	}
        $('#unread').html((currentValue -1));
}

var markAsRead = function (row){
	row.removeClass('well');
	row.css('font-weight', function(){ return "normal";});
        reduceUnread();
}

$("#messageTable tr").click(function () { 
        var modalId = "modal" + $(this).attr("id");
        $.post("/message/markRead/", { "id": modalId }, "html");
        $("#" + modalId).modal('show');
        if ( $(this).hasClass('well')){
            markAsRead($(this));
	}
});

$(document).ready(function() {
    $('#sendMessage').click(function(){
	to = $('#id_to').val();
	$('#newMessage').submit();
	alert("Ok");
        socket.emit("newMessage", to);
    });
}); 
