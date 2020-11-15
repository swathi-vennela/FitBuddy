from django.db import models
from fitbuddy.models import User

class Forum(models.Model):
    createdBy = models.ForeignKey(User,on_delete=models.CASCADE)
    topic= models.CharField(max_length=300)
    description = models.CharField(max_length=1000,blank=True)
    date_created=models.DateTimeField(auto_now_add=True,null=True)
    
    def __str__(self):
        return str(self.topic)
 
class Discussion(models.Model):
    forum = models.ForeignKey(Forum,on_delete=models.CASCADE,null=True,blank=True)
    discuss = models.CharField(max_length=1000)
 
    def __str__(self):
        return str(self.forum)