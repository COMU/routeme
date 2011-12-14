# Create your views here.

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

def index(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/email/login')
    return render_to_response("route/index.html")
