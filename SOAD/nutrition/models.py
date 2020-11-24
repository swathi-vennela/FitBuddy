from django.db import models
from datetime import date
from fitbuddy.models import Customer

class NutritionOfCustomer(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,blank=True,null=True)
    height = models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    weight = models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    bmi = models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    sleepDuration = models.IntegerField(default=0)
    waterIntake = models.IntegerField(default=0)
    date = models.DateField(auto_now=date.today())
    calories = models.IntegerField(default=0)
    gender = models.CharField(default="Female",max_length=7)
    age = models.IntegerField(default=19)

    def __str__(self):
        print(self.date)
        return str(self.date)