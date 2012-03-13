from django.db import models
from django.contrib.auth.models import User
import urllib2

# Create your models here.
class MessageManager(models.Manager):
    def create_message(self, from_user, to_user, subject, message):
        message = self.create(from_user = from_user, to_user = to_user, subject = subject, message = message)
        #push to_user here
        #count = self.count_unread(to_user)
        #urllib2.urlopen("http://drivefor.me/message?user=%s" % (to_user.username))
	return message        
    
    def mark_read(self, id):
	message = self.get(id = id)
        if not message.read:
	    message.read = True
        message.save()
 	return True
    
    def count_unread(self, user):
        count = self.filter(to_user = user, read = False).count()
        return count
    
    def get_all(self, user):
	messages = self.filter(to_user = user)
        return messages

class Message(models.Model):
    from_user = models.ForeignKey(User, related_name = "from_user")
    to_user = models.ForeignKey(User, related_name = "to_user")
    subject = models.CharField(max_length = 100)
    message = models.CharField(max_length = 500)
    date_time = models.DateTimeField(auto_now_add = True, blank = True)
    read = models.BooleanField(default = False, blank = True)
    objects = MessageManager() 
