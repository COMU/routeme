# Create your views here.
from models import Friendship
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.utils import simplejson
from django.template.loader import render_to_string

@login_required
def friendship_request(request, user_id):
    print "Here"
    from_user = request.user
    to_user = User.objects.get(id = int(user_id[-1:]))
    
    if  from_user == to_user and Friendship.objects.requested(from_user, to_user):
	print "No way!"
    else:
	friendship = Friendship.objects.create(from_user=from_user, to_user=to_user, status='3')

    return HttpResponseRedirect(reverse('list-route'))

def show_status(request, user_id):
    print user_id[1:]
    userId = int(user_id[1:])
    to_user = User.objects.get(id = userId)

    title = to_user.get_full_name()
    if Friendship.objects.requested(request.user, to_user):
	#TODO here have to show other options. For example other user requested before user may be accept here.
	#or user have requested before content maybe something about that
  	content = "#TODO"
    elif to_user == request.user:
	content = "Yourself :)"
    else:
	content = render_to_string("friend/request.html", {'user':to_user})
    
    data = {'title':title, 'content':content}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")
            
