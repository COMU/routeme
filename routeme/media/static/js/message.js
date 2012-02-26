var reduceUnread = function(){
   	currentValue = parseInt($('#unread').html());
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

 
