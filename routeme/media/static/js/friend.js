/*var show = function(a){
    userId = a.attr('id');
    $.get("/friend/showStatus/", { user_id: userId }, function(data){
        var myPopover = $('#' + userId).data('popover');
    	myPopover.options.content = data.content;
    	myPopover.options.title = data.title
        myPopover.options.delay = { show: 100, hide: 5000 };
    });
}*/

function friendshipRequest(userId){
 	$.get("/friend/request/" + userId + "/", function(data){
	    //$('#dialog').dialog('close');
            $.get("/friend/showStatus/u" + userId, function(data){
                $('[user]').each(function(){
                    var myPopover = $(this).data('popover');
                    myPopover.options.content = data.content;
                    myPopover.options.title = data.title
                    myPopover.options.delay = { show: 100, hide: 3500 };
	        });
    	    });
	});
}

var setRequests = function (){
    $('.user').each(function(){
	userId = $(this).attr('user');
        $.get("/friend/showStatus/" + userId, function(data){
            $('[user]').each(function(){
                var myPopover = $(this).data('popover');
                myPopover.options.content = data.content;
                myPopover.options.title = data.title
                myPopover.options.delay = { show: 100, hide: 3500 };
	    });
    	});
    });
}

var friendImport = function(){
    $.get("/contact/import/", function(data){
	$('#import').html(data.html);
    });
}

$(document).ready(function(){
    $('.user').popover({html: true});
    setRequests();
    friendImport();
});


/*
$(document).ready(function(){
    $('.user').hover(function(){
	userId = $(this).attr('id');
	x= $(this).position().left - document.scrollLeft;
	y= $(this).position().top - document.scrollTop ;
        $.get("/friend/showStatus/" + userId, function(data){
            $('#dialog').html(data.content);
	    //$('#dialog').dialog({title:data.title});
    	    $("#dialog").dialog('option', 'position', [y, x]);
	    $('#dialog').dialog('open');
    	});
    });
    $( "#dialog" ).dialog({
	autoOpen: false,
	show: "blind",
	hide: "explode",
	width: 250,
	height:85
    });
    //$('.friendshipRequest').hover(function(){friendshipRequest($(this))});
});
*/
