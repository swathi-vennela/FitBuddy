from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from fitbuddy.models import *

# Create your models here.
class FitnessProduct(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    # owner = models.ForeignKey(User,on_delete=models.CASCADE, default=None)
    directions_to_use = models.TextField()
    composition = models.TextField()
    price = models.FloatField()

    def __str__(self):
        return self.title
