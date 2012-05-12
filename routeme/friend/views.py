# Create your views here.
from models import Friendship
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.utils import simplejson
from django.template.loader import render_to_string
from django.shortcuts import render_to_response
from message.models import Message

@login_required
def friendship_request(request, user_id):
    from_user = request.user
    to_user = User.objects.get(id = int(user_id))
    
    if  from_user == to_user or Friendship.objects.requested(from_user, to_user):
	print "No way!"
    else:
	friendship = Friendship.objects.create(from_user=from_user, to_user=to_user, status='3')
	content = from_user.get_full_name() + " sent a friendship request to you."
	message = Message.objects.create_message(from_user, to_user, "Friendship Request", content)
    
    return HttpResponseRedirect(reverse('index'))

@login_required
def show_status(request, user_id):
    print user_id[1:]
    userId = int(user_id[1:])
    to_user = User.objects.get(id = userId)

    title = to_user.get_full_name()
    if Friendship.objects.requested(request.user, to_user):
	#TODO here have to show other options. For example other user requested before user may be accept here.
	#or user have requested before content maybe something about that
  	content = "You have requested before. Waiting confirmation."
    elif Friendship.objects.areFriends(request.user, to_user):
        content = render_to_string("friend/message.html", {'email':to_user.username})
    elif to_user == request.user:
	content = "Yourself :)"
    else:
	content = render_to_string("friend/request.html", {'user':to_user})
    
    data = {'title':title, 'content':content}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

@login_required
def list(request):
    requests = Friendship.objects.getRequestsToUser(request.user)
    friends = Friendship.objects.getFriends(request.user)
    #unread_message_count = Message.objects.count_unread(request.user)
    return render_to_response("friend/list.html", {'requests':requests, 'friends':friends, 'user': request.user})  

@login_required
def accept(request, request_id):
    to_user = Friendship.objects.acceptRequest(request_id)
    content = to_user.get_full_name() + " accepted your friendship request."
    message = Message.objects.create_message(request.user, to_user, "Friendship Request Accepted", content)
    return HttpResponseRedirect(reverse("friendship_list"))

@login_required
def reject(request, request_id):
    to_user = Friendship.objects.rejectRequest(request_id)
    content = to_user.get_full_name() + " accepted your friendship request."
    message = Message.objects.create_message(request.user, to_user, "Friendship Request Rejected", content)
    return HttpResponseRedirect(reverse("friendship_list"))
