from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

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
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    fitnesscenter_name = models.CharField(max_length=30)
    contact_number = models.CharField(max_length=10)
    email = models.EmailField(default = "")


    def __str__(self):
        return self.fitnesscenter_name

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
    price = models.IntegerField()
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

    def get_add_hiring_role_url(self):
        return reverse("add_hiring_role", kwargs={
            'slug' : self.slug
        })

    def get_delete_program_url(self):
        return reverse("delete_program", kwargs={
            'slug' : self.slug
        })


class HiringRole(models.Model):

    GYMTRAINER = 'Gym Trainer'
    GYMINSTRUCTOR = 'Gym Instructor'
    PERSONALTRAINER = 'Personal Trainer'
    FRONTDESKSTAFF = 'Front desk staff'
    SALESMANAGER = 'Sales Manager'
    NUTRITIONIST = 'Fitness Nutritionist'
    OTHER = 'Other'
    
    MALE = 'Male'
    FEMALE = 'Female'
    ANY = 'Any'

    ROLE_CHOICES = [
        (GYMTRAINER, 'GymTrainer'),
        (GYMINSTRUCTOR, 'GymInstructor'),
        (PERSONALTRAINER, 'PersonalTrainer'),
        (FRONTDESKSTAFF, 'FrontDeskStaff'),
        (SALESMANAGER, 'SalesManager'),
        (NUTRITIONIST, 'Nutritionist'),
        (OTHER, 'Other'),
    ]

    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (ANY, 'Any'),
    ]

    fprogram = models.ForeignKey(Program,on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default=OTHER)
    title = models.CharField(max_length=200)
    salary = models.FloatField()
    qualifications = models.TextField()
    responsibilities = models.TextField()
    gender = models.CharField(max_length=30, choices=GENDER_CHOICES, default=ANY)
    contact_email = models.EmailField(default="")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title 

    def get_absolute_url(self):
        return reverse("job_detail", kwargs={
            'slug' : self.slug
        })


class Review(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=5000)
    rating = models.FloatField(default=0)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.user.username

class EnrolledPrograms(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    created =  models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.program.title