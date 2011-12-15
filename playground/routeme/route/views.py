# Create your views here.

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

def index(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/email/login")
    return render_to_response("route/index.html")

def createRoute(request):
    return render_to_response("route/searchRoute.html")
