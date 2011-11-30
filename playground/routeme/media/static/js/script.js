
$(function(){
    var form = $('#signupForm');
    form.submit(function(e){
      $('#sendButton').attr('disabled', true);
      $('#sendWrapper').prepend("<span>Sending Request. Please wait ...</span>");
      $('#ajaxWrapper').load(form.action() + ' #ajaxWrapper', 
                             form.serializeArray(),
                             function(requesstText, responseStatus){
                                $('#sendButton').attr('disabled', false);
      });
      e.preventDefault();
    });
});
























