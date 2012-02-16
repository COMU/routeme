# Create your views here.
from django.contrib.auth.decorators import login_required
from models import Message
from django.utils import simplejson
from django.http import HttpResponse


@login_required
def unread_count(request):
    user = request.user
    count = Message.objects.count_unread(user)
    data = {'count': count}
    return HttpResponse(simplejson.dumps(data), mimetype='application/json')
