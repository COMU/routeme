import cgi, urllib, json

from django.conf import settings
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.urlresolvers import reverse
from userprofile.models import UserProfile
from facebook.models import FacebookProfile
import urllib
import Image


class FacebookBackend:

    def authenticate(self, request=None, token=None):
        """ Reads in a Facebook code and asks Facebook if it's valid and what user it points to. """
        args = {
            'client_id': settings.FACEBOOK_APP_ID,
            'client_secret': settings.FACEBOOK_APP_SECRET,
            'redirect_uri': request.build_absolute_uri(
                reverse('facebook_login_callback')),
            'code': token,
        }

        # Get a legit access token
        target = urllib.urlopen('https://graph.facebook.com/oauth/access_token?' + urllib.urlencode(args)).read()
        response = cgi.parse_qs(target)
        access_token = response['access_token'][-1]

        # Read the user's profile information
        fb_profile = urllib.urlopen(
          'https://graph.facebook.com/me?access_token=%s' % access_token)

        fb_profile = json.load(fb_profile)
	photo_url = "https://graph.facebook.com/" + str(fb_profile['id'])  +"/picture?type=large&access_token=" + access_token

        try:
          # Try and find existing user
          facebook_profile = FacebookProfile.objects.get(
              facebook_id=fb_profile['id'])

          # Update access_token
          facebook_profile.access_token = access_token
          facebook_profile.save()

        except FacebookProfile.DoesNotExist:
          # No existing user, create one
          facebook_profile = FacebookProfile(facebook_id=fb_profile['id'],
                                             access_token=access_token)
          facebook_profile.save()
        backend = facebook_profile.getLoginBackend(request)
        
        try:
          fb_username = fb_profile['username'] 
          fb_mail = fb_profile['email']
          user = backend.login(
            facebook_profile, related_name='facebook_profile',
            username=fb_profile['email'],first_name = fb_profile['first_name'], last_name = fb_profile['last_name'], email=fb_profile['email'])
    


	  userProfile,created = UserProfile.objects.get_or_create(user = user,
                            profilePhoto = 'images/default.png'
                )
          urllib.urlretrieve (photo_url,
                             '/'.join(userProfile.profilePhoto.path.split('/')[:-1])+"/"+str(user.id)+".jpg" )
          userProfile.profilePhoto='images/'+str(user.id)+".jpg"


          image = Image.open(userProfile.profilePhoto.path)
          image = image.resize((96, 96), Image.ANTIALIAS)
          image.save(userProfile.profilePhoto.path,"jpeg")

          userProfile.save()



        except:
          import sys
          print "error ", sys.exc_info()[0]
        return user


    def get_user(self, user_id):
        """ Just returns the user of a given ID. """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    supports_object_permissions = False
    supports_anonymous_user = False
