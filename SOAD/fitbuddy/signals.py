from django.dispatch import receiver
from django.db.models.signals import post_save
from fitbuddy.models import Customer
from nutrition.models import NutritionOfCustomer

@receiver(post_save,sender=Customer,dispatch_uid="nutrition_unique_id")
def createNutritionObject(sender,**kwargs):
    customer = kwargs["instance"]
    nutritionObj = NutritionOfCustomer.objects.create(customer=customer)
    nutritionObj.save()
    print(nutritionObj)
    print("Object created")
