from django.db import models
from fitbuddy.models import *

# Create your models here.
class FitnessEquipment(models.Model):
    title = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=30)
    description = models.TextField()
    owner = models.ForeignKey(User,on_delete=models.CASCADE, default=None)
    price = models.FloatField()

    def __str__(self):
        return self.title
