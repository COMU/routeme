# Create your views here.

from django.shortcuts import render_to_response
from forms import UserForm,LoginForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from models import UserProfile
from django.contrib.auth import authenticate,login as auth_login
from django.contrib.auth import logout as user_logout
from django.contrib.auth.decorators import login_required

def error404(request):
    return render_to_response("application/404.html")

@login_required
def index(request):
    return render_to_response("application/index.html")

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username,password=password)
            if user is not None:
                if user.is_active:
                    auth_login(request,user)

            return HttpResponseRedirect(reverse("index"))
        else:
            return render_to_response('application/login.html',{'form':LoginForm()})
    else:
        return render_to_response('application/login.html',{'form':LoginForm()})
def foursq(request):
    HttpResponseRedirect(reverse("foursq"))
def logout(request):
    user_logout(request)
    return HttpResponseRedirect(reverse("login-user"))

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = User(email = form.cleaned_data['email'])
            user.first_name = form.cleaned_data['firstName']
            user.last_name = form.cleaned_data['lastName']
            user.username = user.email
            user.set_password(form.cleaned_data['password'])
            user.is_active = True
            user.save()

            userProfile = UserProfile.objects.create(user = user,
                            birthdate = form.cleaned_data['birthdate'],
                            gender = form.cleaned_data['gender'])

            return HttpResponseRedirect(reverse("login-user"))

    else:
        form = UserForm()

    data = {
        'form': form
    }
    return render_to_response("application/signup.html", data)

