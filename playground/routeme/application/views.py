# Create your views here.

from django.shortcuts import render_to_response
from forms import UserForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from models import UserProfile

def error404(request):
    return render_to_response("application/404.html")

def index(request):
    return render_to_response("application/index.html")

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
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

            return HttpResponseRedirect(reverse("index"))

    else:
        form = UserForm()

    data = {
        'form': form
    }
    return render_to_response("application/signup.html", data)

