from django.contrib.gis.db import models
from django.contrib.auth.models import User


RELATIONSHIP_FOLLOWING = 1
RELATIONSHIP_BLOCKED = 2
RELATIONSHIP_WAITING = 3
RELATIONSHIP_STATUSES = (
    (RELATIONSHIP_FOLLOWING, 'Following'),
    (RELATIONSHIP_BLOCKED, 'Blocked'),
    (RELATIONSHIP_WAITING, 'Waiting')
)

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)
#Rota bilgileri

class RouteInformation(models.Model):
    date = models.DateField()
    time = models.TimeField()
    arrivalTime = models.CharField(max_length=10)
    vehicle = models.CharField(max_length=30)
    capacity = models.IntegerField()
    baggage = models.BooleanField()
    pet = models.BooleanField()
    route = models.LineStringField()
    people = models.ManyToManyField(User)
    owner = models.ManyToManyField(User, related_name = "owner")

class ProfilePhoto(models.Model):
    photo = models.ImageField(upload_to = "images")

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    birthdate = models.DateField()
    gender = models.CharField(max_length = 1, choices = GENDER_CHOICES)
    experience = models.IntegerField(default = 0, null = True)
    profilePhoto = models.ForeignKey(ProfilePhoto, null = True)

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

class Friendship(models.Model):
    from_person = models.ForeignKey(UserProfile, related_name='from_people')
    to_person = models.ForeignKey(UserProfile, related_name='to_people')
    status = models.IntegerField(choices=RELATIONSHIP_STATUSES)
