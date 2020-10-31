from django.contrib import admin
from .models import User,Customer,FitnessCenter, Program
# Register your models here.
admin.site.register(User)
admin.site.register(Customer)
admin.site.register(FitnessCenter)
admin.site.register(Program)