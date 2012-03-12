from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models import Q
# Create your models here.

FRIENDSHIP_STATUSES = (
    ('1', 'Friend'),
    ('2', 'Blocked'),
    ('3', 'Waiting')
)

class FriendShipManager(models.Manager):
    def areFriends(self, user1, user2):
	if self.filter(from_user=user1, to_user=user2, status='1').count() > 0 or \
	    self.filter(from_user=user2, to_user=user1, status='1').count() > 0:
		return True
	return False
    
    def requested(self, user1, user2):
	if self.filter(from_user=user1, to_user=user2, status="3").count() > 0 or \
    	    self.filter(from_user=user2, to_user=user1, status='3').count() > 0:
		return True
	return False
   
    def getFriends(self, user):
	return self.filter(Q(from_user = user, status='1') | Q(to_user=user, status='2'))
     
    def getRequestsToUser(self, user):
        return self.filter(to_user = user, status='3')

    def acceptRequest(self, requestId):
	request = self.get(id = requestId)
        request.status = "1"
	request.save()
        return True

    def rejectRequest(self, requestId):
        request = self.get(id = requestId)  
        request.status = "2"
	request.save()
        return True  

class Friendship(models.Model):
    from_user = models.ForeignKey(User, related_name="user1")
    to_user = models.ForeignKey(User, related_name="user2")
    status = models.CharField(max_length=1, choices=FRIENDSHIP_STATUSES, default='3')
    date_created = models.DateTimeField(default=datetime.now(), blank=True)
    
    objects = FriendShipManager()
