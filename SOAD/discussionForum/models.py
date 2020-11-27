from django.db import models
from fitbuddy.models import User

class Question(models.Model):
    # Also add topic here
    createdBy = models.ForeignKey(User,on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True,blank=True)
    question = models.CharField(max_length=300)
    description = models.CharField(max_length=1000,blank=True)

    def __str__(self):
        return str(self.question)
 
class Answer(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    answer = models.CharField(max_length=1000)
    answeredBy = models.ForeignKey(User,on_delete=models.CASCADE)
    date_answered = models.DateTimeField(auto_now_add=True,blank=True)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.question.question + " has the answers as " + self.answer

class Comment(models.Model):
    comment = models.TextField()
    answer = models.ForeignKey(Answer,on_delete=models.CASCADE)
    commentedBy = models.ForeignKey(User,on_delete=models.CASCADE)
    date_commented = models.DateTimeField(auto_now_add=True,blank=True)
    
    def __str__(self):
        return self.commentedBy.username+" commented "+self.comment