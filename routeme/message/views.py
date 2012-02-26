# Create your views here.
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from models import Message
from django.utils import simplejson
from django.http import HttpResponse
from django.shortcuts import render_to_response

@login_required
def unread_count(request):
    user = request.user
    count = Message.objects.count_unread(user)
    data = {'count': count}
    return HttpResponse(simplejson.dumps(data), mimetype='application/json')

@login_required
def inbox(request):
    messages = Message.objects.get_all(request.user)
    
    unread_message_count = Message.objects.count_unread(request.user)
    profil = render_to_string("include/profil.html", {'user': request.user, 'unread': unread_message_count})
    
    return render_to_response("message/inbox.html", {'messages': messages, 'profil':profil})

def mark_read(request):
    message_id = request.POST["id"]
    message = Message.objects.mark_read(id = message_id[5:])# id basinda modal yazarak geliyor
    return HttpResponse("1")
