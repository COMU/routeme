# Create your views here.

from django.shortcuts import render_to_response
from forms import UserForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from models import UserProfile, ProfilePhoto
from django.contrib.auth import authenticate,login as auth_login

def error404(request):
    return render_to_response("application/404.html")

def index(request):
    return render_to_response("application/index.html")

def loginpage(request):
    return render_to_response('application/login.html',{'user':user})

def login(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
   # print username
   # print password
    user = authenticate(username=username,password=password)
    if user is not None:
        if user.is_active:
            auth_login(request,user)

        else:
            print "olmadi1"
    else:
        print "olmadi2"

    return render_to_response('application/login.html',{'user':user})

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            user = User(email = form.cleaned_data['email'])
            user.first_name = form.cleaned_data['firstName']
            user.last_name = form.cleaned_data['lastName']
            user.username = user.email
            user.set_password(form.cleaned_data['password'])
            user.save()

            userProfile = UserProfile.objects.create(user = user,
                            birthdate = form.cleaned_data['birthdate'],
                            gender = form.cleaned_data['gender'])
            if form.cleaned_data['photo']:
                photo = ProfilePhoto.objects.create(photo = form.cleaned_data['photo'])
                userProfile.profilePhoto = photo
                userProfile.save()

            return HttpResponseRedirect(reverse("index"))

    else:
        form = UserForm()

    data = {
        'form': form
    }
    return render_to_response("application/signup.html", data)

