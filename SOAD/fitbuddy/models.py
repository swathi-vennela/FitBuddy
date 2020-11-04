from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image

from django.urls import reverse
from django.conf import settings

# Create your models here.
class User(AbstractUser):

    email = models.EmailField()
    is_customer = models.BooleanField(default=False)
    is_fitnesscenter = models.BooleanField(default=False)
class Profile(models.Model):
    email = models.EmailField(default="")

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
 
    def __str__(self):
        return self.user.username

class FitnessCenter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    fitnesscenter_name = models.CharField(max_length=30)
    contact_number = models.CharField(max_length=10)
    email = models.EmailField()
    def __str__(self):
        return self.fitnesscenter_name

# class listfc(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
#     fitnesscenter_name = models.CharField(max_length=30)
#     contact_number = models.CharField(max_length=10)
#     email = models.EmailField(default="")


class Program(models.Model):

    WEIGHTLOSS = 'Weight Loss'
    WEIGHTGAIN = 'Weight Gain'
    BODYBUILDING = 'Body Building'
    REGULAR = 'Regular'
    DANCE = 'Dance'
    YOGA = 'Yoga'
    PHYSIOTHERAPY = 'Physiotherapy'
    MASSAGETHERAPY = 'Massage Therapy'
    
    CATEGORY_CHOICES = [
        (WEIGHTLOSS, 'Weightloss'),
        (WEIGHTGAIN, 'WeightGain'),
        (BODYBUILDING, 'BodyBuilding'),
        (REGULAR, 'Regular'),
        (DANCE, 'Dance'),
        (YOGA, 'Yoga'),
        (PHYSIOTHERAPY, 'Physiotherapy'),
        (MASSAGETHERAPY, 'MassageTherapy'),
    ]

    fcenter = models.ForeignKey(FitnessCenter,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default=REGULAR,)
    number_of_sessions = models.IntegerField()
    hours_per_session = models.FloatField()
    price = models.FloatField()
    description = models.TextField()
    image = models.ImageField(default='default.jpg',upload_to = 'program_pics')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse("program_detail",kwargs={
            'slug' : self.slug
        })

    def get_edit_program_url(self):
        return reverse("edit_program", kwargs={
            'slug' : self.slug
        })

    def get_delete_program_url(self):
        return reverse("delete_program", kwargs={
            'slug' : self.slug
        })