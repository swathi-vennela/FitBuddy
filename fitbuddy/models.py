from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    email = models.EmailField()
    is_customer = models.BooleanField(default=False)
    is_fitnesscenter = models.BooleanField(default=False)

class Customer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

class FitnessCenter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    fitnesscenter_name = models.CharField(max_length=30)
    contact_number = models.CharField(max_length=10)