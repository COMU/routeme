# Create your views here.
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from models import Message
from django.utils import simplejson
from django.http import HttpResponse
from django.shortcuts import render_to_response
from forms import MessageForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from friend.models import Friendship

@login_required
def unread_count(request):
    user = request.user
    count = Message.objects.count_unread(user)
    data = {'count': count}
    return HttpResponse(simplejson.dumps(data), mimetype='application/json')

@login_required
def inbox(request, username = None):
    if request.method == "POST":
    	form = MessageForm(request.POST)
        if form.is_valid():
   	    to_user = form.cleaned_data['to']
   	    subject = form.cleaned_data['subject']
   	    message = form.cleaned_data['message']
            
	    to_user = User.objects.get(username = to_user)
	    Message.objects.create_message(request.user, to_user, subject, message)
            return HttpResponseRedirect("/message/inbox")
  
    messages = Message.objects.get_all(request.user)
    paginator = Paginator(messages, 10)
    
    page = 1
    if request.GET.has_key('page'):
	page = int(request.GET.get('page'))

    messages = paginator.page(page)
    friends = Friendship.objects.getFriends(request.user)
    kvargs = []    
    for friend in friends:
        kvargs.append((friend.username, friend.get_full_name()))
    form = MessageForm(kvargs)
    print len(kvargs)
    if username:
	data = {'to': username}
        form = MessageForm(initial=data)
    
    return render_to_response("message/inbox.html", {'messages': messages,'form': form, 'user': request.user, 'title':"Messages"})

@login_required
def mark_read(request):
    message_id = request.POST["id"]
    message = Message.objects.mark_read(id = message_id[5:])# id basinda modal yazarak geliyor
    return HttpResponse("1")
