from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    email = models.EmailField()
    is_customer = models.BooleanField(default=False)
    is_fitnesscenter = models.BooleanField(default=False)

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
 
    def __str__(self):
        return self.user.username

class FitnessCenter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    fitnesscenter_name = models.CharField(max_length=30)
    contact_number = models.CharField(max_length=10)

    def __str__(self):
        return self.fitnesscenter_name

class Program(models.Model):

    WEIGHTLOSS = 'WL'
    WEIGHTGAIN = 'WG'
    BODYBUILDING = 'AB'
    REGULAR = 'RG'
    DANCE = 'DC'
    YOGA = 'YG'
    
    CATEGORY_CHOICES = [
        (WEIGHTLOSS, 'Weightloss'),
        (WEIGHTGAIN, 'WeightGain'),
        (BODYBUILDING, 'BodyBuilding'),
        (REGULAR, 'Regular'),
        (DANCE, 'Dance'),
        (YOGA, 'Yoga'),
    ]

    fcenter = models.ForeignKey(FitnessCenter,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=REGULAR,)
    number_of_sessions = models.IntegerField()
    hours_per_session = models.FloatField()
    price = models.FloatField()
    description = models.TextField()
    image = models.ImageField(default='default.jpg',upload_to = 'program_pics')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title