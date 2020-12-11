from django.db import models
from datetime import date
from fitbuddy.models import Customer
from django.utils import timezone

class NutritionOfCustomer(models.Model):
    customer = models.OneToOneField(Customer,on_delete=models.CASCADE,primary_key=True)
    latestHeight = models.FloatField(default=0,blank=True,null=True)
    latestWeight = models.FloatField(default=0,blank=True,null=True)
    latestBMI = models.FloatField(default=0,blank=True,null=True)
    gender = models.CharField(default="Female",max_length=7,blank=True,null=True)
    day = models.IntegerField(default=1,blank=True,null=True)
    month = models.IntegerField(default=1,blank=True,null=True)
    year = models.IntegerField(default=1,blank=True,null=True)

    def __str__(self):
        return "Nutrition of " + self.customer.user.username

    def calculateAge(self):
        today = date.today()
        if today.month < self.month:
            age = today.year - self.year - 1
        elif today.month == self.month:
            if today.day < self.day:
                age = today.year - self.year - 1
            else:
                age = today.year - self.year
        else:
            age = today.year - self.year
        return age

class Sleep(models.Model):
    nutrition = models.ForeignKey(NutritionOfCustomer,on_delete=models.CASCADE,blank=True,null=True)
    duration = models.FloatField(default = 0,blank=True,null=True)
    date = models.DateTimeField(auto_now = timezone.now())

    def __str__(self):
        return str(self.duration) + " of sleep on " + str(self.date)

class Water(models.Model):
    nutrition = models.ForeignKey(NutritionOfCustomer,on_delete=models.CASCADE,blank=True,null=True)
    glasses = models.IntegerField(default=0,blank=True,null=True)
    date = models.DateTimeField(auto_now = timezone.now())

    def __str__(self):
        return str(self.glasses) + " glasses of water consumed on " + str(self.date)

class Calorie(models.Model):
    nutrition = models.ForeignKey(NutritionOfCustomer,on_delete=models.CASCADE,blank=True,null=True)
    calories = models.FloatField(default=0,blank=True,null=True)
    date = models.DateTimeField(auto_now = timezone.now())

    def __str__(self):
        return str(self.calories) + " kcal consumed on " + str(self.date)

class BodyMass(models.Model):
    nutrition = models.ForeignKey(NutritionOfCustomer,on_delete=models.CASCADE,blank=True,null=True)
    date = models.DateTimeField(auto_now=timezone.now())
    weight = models.FloatField(default=0,blank=True,null=True)
    height = models.FloatField(default=1,blank=True,null=True)
    bmi = models.FloatField(default=0,blank=True,null=True)
    category = models.CharField(default="Normal",max_length=10,blank=True,null=True)

    def __str__(self):
        return self.category

    def calculateBMI(self,height,weight,heightUnit,weightUnit):
        self.weightToKgs(weight,weightUnit)
        self.heightToMeters(height,heightUnit)
        result = self.weight/(self.height*self.height)
        print(result)
        self.bmi = result
        self.findCategoryOfBMI()

    def heightToMeters(self,height,heightUnit):
        if heightUnit == 'cm':
            height = height/100.0
        elif heightUnit == 'inch':
            height = height * 0.02
        print(height)
        self.height = height

    def weightToKgs(self,weight,weightUnit):
        if weightUnit == 'lb':
            weight = weight * 0.45
        self.weight = weight

    def findCategoryOfBMI(self):
        if self.bmi <= 18.5:
            result = "underweight"
        elif self.bmi <=24.9 and self.bmi >= 18.5:
            result =  "normal weight"
        elif self.bmi >= 25 and self.bmi <= 29.9:
            result = "overweight"
        else:
            result = "obese"
        self.category = result