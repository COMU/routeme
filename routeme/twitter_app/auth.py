#!/usr/bin/python
# -*- coding: utf-8 -*-

from openid.consumer.consumer import SUCCESS

from django.contrib.auth.models import User
from django.core.mail import mail_admins

from routeme.google.models import GoogleProfile
from routeme.userprofile.models import UserProfile
from routeme.twitter_app.models import TwitterProfile
import settings
import urllib
import Image

class TwitterAuthBackend(object):
  def authenticate(self, request, credentials):

    if credentials is None:
      return None

    twitter_id = credentials['id']
    twitter_screenname = credentials['screen_name']
    twitter_username = credentials['name']


    try:
      twitter_profile = TwitterProfile.objects.get(twitter_id=twitter_id)

    except TwitterProfile.DoesNotExist:
      twitter_profile = TwitterProfile(
          twitter_id = twitter_id,
          screenname = twitter_screenname,
          firstname = twitter_username.rsplit()[0],
          lastname = twitter_username.rsplit()[1])

    twitter_profile.save()
    backend = twitter_profile.getLoginBackend(request)
    user = backend.login(
        twitter_profile, related_name='twitter_profile',
        username=twitter_screenname, email=settings.DEFAULT_EMAIL)

    userProfile,created = UserProfile.objects.get_or_create(user = user,
                            profilePhoto = 'images/default.png'
                )
    urllib.urlretrieve (credentials['profile_image_url'],
                   '/'.join(userProfile.profilePhoto.path.split('/')[:-1])+"/"+str(user.id)+".jpg" )
    userProfile.profilePhoto='images/'+str(user.id)+".jpg"
    image = Image.open(userProfile.profilePhoto.path)
    image = image.resize((96, 96), Image.ANTIALIAS)
    image.save(userProfile.profilePhoto.path,"jpeg")

    userProfile.save()

    return user


  def get_user(self, user_id):
    try:
      return User.objects.get(pk=user_id)
    except User.DoesNotExist:
      return None
