from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class MessageManager(models.Manager):
    def create_message(self, from_user, to_user, message):
        self.create(from_user = from_user, to_user = to_user, message = message)
        #TODO if to_user online push here
    
    def count_unread(self, user):
        count = self.filter(to_user = user, read = False).count()
        return count

class Message(models.Model):
    from_user = models.ForeignKey(User, related_name = "from_user")
    to_user = models.ForeignKey(User, related_name = "to_user")
    message = models.CharField(max_length = 300)
    date_time = models.DateTimeField(auto_now_add = True, blank = True)
    read = models.BooleanField(default = False, blank = True)
    objects = MessageManager() 
