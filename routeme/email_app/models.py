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

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    birthdate = models.DateField()
    gender = models.CharField(max_length = 1, choices = GENDER_CHOICES)
    experience = models.IntegerField(default = 0, null = True)
    profilePhoto = models.ImageField(upload_to = "images", null =True)


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

class Registration(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length = 50)

class Friendship(models.Model):
    from_person = models.ForeignKey(User, related_name='from_people')
    to_person = models.ForeignKey(User, related_name='to_people')
    status = models.IntegerField(choices=RELATIONSHIP_STATUSES)
