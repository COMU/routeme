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

class ProfilePhoto(models.Model):
    photo = models.ImageField(upload_to = "images")

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    birthdate = models.DateField()
    gender = models.CharField(max_length = 1, choices = GENDER_CHOICES)
    route = models.ManyToManyField(RouteInformation)
    experience = models.IntegerField()
    friends = models.ManyToManyField('self', through='Friendship',
                                    symmetrical = False, related_name='related_to')

    def add_relationship(self, person, status):
        relationship, created = Friendship.objects.get_or_create(
            from_person=self,
            to_person=person,
            status=status)
        return relationship


    def remove_relationship(self, person, status):
        Friendship.objects.filter(
            from_person=self,
            to_person=person,
            status=status).delete()
        return

    def get_relationships(self, status):
        return self.relationships.filter(
            to_people__status=status,
            to_people__from_person=self)

    def get_related_to(self, status):
        return self.related_to.filter(
            from_people__status=status,
            from_people__to_person=self)

    def get_waiting(self,person,status):
        return self.get_relationships(RELATIONSHIP_WAITING)

    def get_following(self):
        return self.get_relationships(RELATIONSHIP_FOLLOWING)

    def get_followers(self):
        return self.get_related_to(RELATIONSHIP_FOLLOWING)

class Friendship(models.Model):
    from_person = models.ForeignKey(User, related_name='from_people')
    to_person = models.ForeignKey(User, related_name='to_people')
    status = models.IntegerField(choices=RELATIONSHIP_STATUSES)
