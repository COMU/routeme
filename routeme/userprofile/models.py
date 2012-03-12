from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.utils.hashcompat import sha_constructor
import random 
import datetime

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    birthdate = models.DateField(null = True)
    gender = models.CharField(max_length = 1, choices = GENDER_CHOICES, null = True)
    experience = models.IntegerField(default = 0, null = True)
    profilePhoto = models.ImageField(upload_to = "images/%Y/%m/%d", default = "images/default.png", null =True)
    
    google_profile = models.OneToOneField(
      'google.GoogleProfile',
      blank=True, null=True, related_name='userprofile_set')
    facebook_profile = models.OneToOneField(
      'facebook.FacebookProfile',
      blank=True, null=True, related_name='userprofile_set')
    twitter_profile = models.OneToOneField(
      'twitter_app.TwitterProfile',
      blank=True, null=True, related_name='userprofile_set')
    foursq_profile = models.OneToOneField(
      'foursq.FoursqProfile',
      blank=True, null=True, related_name='userprofile_set')

    def __unicode__(self):
        return self.user.__unicode__()

    def addFriend(self, person, status):
        relationship, created = Friendship.objects.get_or_create(
            from_person=self.user,
            to_person=person,
            status=status)
        return created


    def removeFriend(self, person, status):
        Friendship.objects.filter(
            from_person=self.person,
            to_person=person,
            status=status).delete()
        return true

class RegistrationManager(models.Manager):
    def create_registration(self, user):
        salt = sha_constructor(str(random.random())).hexdigest()[:5]
	activation_key = sha_constructor(salt+user.username).hexdigest()
  	return self.create(user=user,
                           activation_key=activation_key)
    
    def activate_user(self, key):
        try:
	    r = self.get(activation_key = key) 
        except self.model.DoesNotExist:
	    return False
        if not r.activation_key_expried():
            user = r.user
            user.is_active = True
            user.save()
            return user
        return False
   
class Registration(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length = 50)
    objects = RegistrationManager()
   
    def send_activation_mail(self):
        import mail
        mail.send_activation_mail(self.user)

    def activation_key_expried(self):
        expiration_date = datetime.timedelta(days=7)
        return (self.user.date_joined + expiration_date <= datetime.datetime.now()) 
