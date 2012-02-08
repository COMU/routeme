# Create your views here.

from django.shortcuts import render_to_response
from forms import UserForm,LoginForm,UserUpdateForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from models import UserProfile
from django.contrib.auth import authenticate,login as auth_login
from django.contrib.auth.models import check_password
from django.contrib.auth import logout as user_logout
from django.contrib.auth.decorators import login_required
import Image
def error404(request):
    return render_to_response("email_app/404.html")

@login_required
def index(request):
    return render_to_response("email_app/index.html")

@login_required
def update(request):
  if request.method == "POST":
        form = UserUpdateForm(request.POST,request.FILES)
        if form.is_valid():
                firstname = form.cleaned_data['firstName']
                lastname = form.cleaned_data['lastName']
                email = form.cleaned_data['email']
                user_profile = UserProfile.objects.get(user=request.user)

                request.user.first_name = firstname
                request.user.last_name = lastname
                request.user.username = email
                request.user.email = email
                if request.FILES:
                        photo = request.FILES['photo']
                        user_profile.profilePhoto = photo
                        user_profile.save()
                        #user_profile.profilePhoto.name='/images/'+str(request.user.id)+'.jpeg'
                        image = Image.open(user_profile.profilePhoto.path)
                        image = image.resize((96, 96), Image.ANTIALIAS)
                        image.save(user_profile.profilePhoto.path,"jpeg")
                        user_profile.save()
                request.user.save()
                return HttpResponseRedirect("/email/update")

  else:
        user_profile = UserProfile.objects.get(user=request.user)

        initial_data = {
                'email': request.user.email,
                'firstName':request.user.first_name,
                'lastName':request.user.last_name
        }
        form = UserUpdateForm(initial=initial_data)

  data={
           'form':form,
           'title':"Profile",
           'img': request.user.userprofile.profilePhoto.url
   }
  return render_to_response("email_app/update.html", data)



	
def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user=authenticate(username=username,password=password)
            u=User.objects.get(username=username)
            if user is not None and u.check_password(password):
                if user.is_active:
                    auth_login(request,user)
                else:
                    return render_to_response('email_app/login.html',{'title':'Login', 'form'   :LoginForm()})
            else:
                return render_to_response('email_app/login.html',{'title':'Login', 'form':LoginForm()})
            return HttpResponseRedirect('/')
        else:
            return render_to_response('email_app/login.html',{'title':'Login', 'form':LoginForm()})
    else:
        return render_to_response('email_app/login.html',{'title':'Login', 'form':LoginForm()})
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

            userProfile = UserProfile.objects.get_or_create(user = user,
                            birthdate = form.cleaned_data['birthdate'],
                            gender = form.cleaned_data['gender'],
			    profilePhoto = 'images/default.png'
				)

            return HttpResponseRedirect(reverse("login-user"))

    else:
        form = UserForm()

    data = {
        'form': form,
        'title': 'SignUp'
    }
    return render_to_response("email_app/signup.html", data)

