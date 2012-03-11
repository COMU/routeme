/*var show = function(a){
    userId = a.attr('id');
    $.get("/friend/showStatus/", { user_id: userId }, function(data){
        var myPopover = $('#' + userId).data('popover');
    	myPopover.options.content = data.content;
    	myPopover.options.title = data.title
        myPopover.options.delay = { show: 100, hide: 5000 };
    });
}*/


$(document).ready(function(){
    $('.user').popover({html: true});
    $('.user').each(function(){
	userId = $(this).attr('id');
        $.get("/friend/showStatus/" + userId, function(data){
            var myPopover = $('#' + userId).data('popover');
            myPopover.options.content = data.content;
            myPopover.options.title = data.title
            myPopover.options.delay = { show: 100, hide: 3500 };
    	});
    });
    $('.friendShipRequest').click(function(){
        url = $(this).attr('href');
        alert(url);
 	$.get(url, function(data){
	    //TODO
	});
    });

});
