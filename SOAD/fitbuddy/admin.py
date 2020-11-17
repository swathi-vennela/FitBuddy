from django.contrib import admin
from .models import User,Customer,FitnessCenter, Program, Review, HiringRole, EnrolledPrograms
# Register your models here.
admin.site.register(User)
admin.site.register(Customer)
admin.site.register(FitnessCenter)
admin.site.register(Program)
admin.site.register(Review)
admin.site.register(HiringRole)
admin.site.register(EnrolledPrograms)