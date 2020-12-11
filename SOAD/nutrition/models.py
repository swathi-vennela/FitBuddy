from django.db import models
from datetime import date
from fitbuddy.models import Customer
from django.utils import timezone

class Sleep(models.Model):
    duration = models.FloatField(default = 0)
    date = models.DateTimeField(auto_now = timezone.now())

    def __str__(self):
        return str(self.duration) + " of sleep on " + str(self.date)

class Water(models.Model):
    glasses = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now = timezone.now())

    def __str__(self):
        return str(self.glasses) + " glasses of water consumed on " + str(self.date)

class Calorie(models.Model):
    calories = models.FloatField(default=0)
    date = models.DateTimeField(auto_now = timezone.now())

    def __str__(self):
        return str(self.calories) + " kcal consumed on " + str(self.date)

class BodyMass(models.Model):
    weight = models.FloatField(default=0)
    height = models.FloatField(default=1)
    date = models.DateTimeField()
    bmi = models.FloatField(default=0)
    category = models.CharField(default="Normal",max_length=10)

    def __str__(self):
        return self.category

    def calculateBMI(height,weight,heightUnit,weightUnit):
        self.weight = weightToKgs(weight,weightUnit)
        self.height = heightToMeters(height,heightUnit)
        result = self.weight/(self.height*self.height)
        print(result)
        self.bmi = result
        self.findCategoryOfBMI()

    def heightToMeters(height,heightUnit):
        if heightUnit == 'cm':
            height = height/100.0
        elif heightUnit == 'inch':
            height = height * 0.02
        print(height)
        self.height = height

    def weightToKgs(weight,weightUnit):
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

class NutritionOfCustomer(models.Model):
    customer = models.OneToOneField(Customer,on_delete=models.CASCADE,primary_key=True)
    bodyMass = models.ForeignKey(BodyMass,on_delete=models.CASCADE,blank=True,null=True)
    sleep = models.ForeignKey(Sleep,on_delete=models.CASCADE,blank=True,null=True)
    water = models.ForeignKey(Water,on_delete=models.CASCADE,blank=True,null=True)
    calories = models.ForeignKey(Calorie,on_delete=models.CASCADE,blank=True,null=True)
    gender = models.CharField(default="Female",max_length=7)
    dateOfBirth = models.DateField(default=timezone.now())

    def __str__(self):
        return "Nutrition of " + self.customer.user.username