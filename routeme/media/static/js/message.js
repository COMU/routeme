$("#messageTable tr").click(function () { 
            var modalId = "modal" + $(this).attr("id");
            $.post("/message/markRead/", { "id": modalId }, "html");
            $("#" + modalId).modal('show');
});

