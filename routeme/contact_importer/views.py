from django.template.context import RequestContext
from django.shortcuts import render_to_response
from contact_importer.utils import *
from django.contrib.auth.decorators import login_required
from facebook.models import FacebookProfile
from foursq.models import FoursqProfile
from userprofile.models import UserProfile
from twitter_app.models import TwitterProfile
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from userprofile.models import *
from django.template.loader import render_to_string
from django.http import HttpResponse

@login_required
def contact_importer_home(request, importing_profile=0):
      user = request.user
      profile = user.get_profile()
      friends_list = ""
      found_friends = []
      found_friends_profile = []
      if importing_profile == 'facebook':
        if profile.facebook_profile and True or False==True:
          friends_list = facebook_contact_import(request)
          for i in friends_list:
            try:
              facebook_id = FacebookProfile.objects.get(facebook_id=i)
              user_id = facebook_id.id
              user_data = UserProfile.objects.get(facebook_profile=user_id)
              profile = user_data.user.get_profile()
              found_friends.append(profile)
            except ObjectDoesNotExist:
              pass    
      elif importing_profile == 'foursquare':
        if profile.foursq_profile and True or False==True:
          friends_list = foursquare_contact_import(request)
          for i in friends_list:
            try:
              foursquare_id = FoursqProfile.objects.get(foursq_id=i)
              user_id = foursquare_id.id
              user_data = UserProfile.objects.get(foursq_profile=user_id)
              profile = user_data.user.get_profile()
              found_friends.append(profile)
            except ObjectDoesNotExist:
              pass    
      elif importing_profile == 'twitter':
        if profile.twitter_profile and True or False==True:
          friends_list = twitter_contact_import(request)
          for i in friends_list:
            try:
              twitter_id = TwitterProfile.objects.get(twitter_id=i)
              user_id = twitter_id.id
              user_data = UserProfile.objects.get(twitter_profile=user_id)
              profile = user_data.user.get_profile()
              found_friends.append(profile)
            except ObjectDoesNotExist:
              pass    
      elif importing_profile == 'google':
        if profile.google_profile and True or False==True:
          friends_list = google_contact_import(request)


      context = {
      'user' : user,
      'title': 'Import Contacts',
      'friends_list' : found_friends 
      }
      return render_to_response('import/listcontacts.html', context,  context_instance=RequestContext(request, ))

@login_required
def contact_importer(request):
      user = request.user
      profile = user.get_profile()
      context = {
      'facebook_profile_activated': profile.facebook_profile and True or False,
      'google_profile_activated': profile.google_profile and True or False,
      'twitter_profile_activated': profile.twitter_profile and True or False,
      'foursq_profile_activated': profile.foursq_profile and True or False,
      }

      html = render_to_string('import/import.html', context)
      return HttpResponse(simplejson.dumps({'html': html}), mimetype="application/json")
