from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from .models import User, Customer,FitnessCenter, Program, Review, HiringRole
from nutrition.models import NutritionOfCustomer

class CustomerRegistrationForm(UserCreationForm):
    email = forms.CharField(required=True)
    class Meta(UserCreationForm.Meta):
        model = User
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.email=self.cleaned_data.get('email')
        user.save()
        customer = Customer.objects.create(user=user)
        customer.email = self.cleaned_data.get('email')
        customer.save()
        nutrition = NutritionOfCustomer.objects.create(customer=customer)
        nutrition.save()
        print(nutrition)
        return user


class FitnessRegistrationForm(UserCreationForm):
    email = forms.CharField(required=True)
    fitnesscenter_name = forms.CharField(required=True)
    contact_number = forms.CharField(required=True)
    class Meta(UserCreationForm.Meta):
        model = User  

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_fitnesscenter=True
        user.email=self.cleaned_data.get('email')
        user.save()
        fitnesscenter = FitnessCenter.objects.create(user=user)
        fitnesscenter.fitnesscenter_name=self.cleaned_data.get('fitnesscenter_name')
        fitnesscenter.contact_number=self.cleaned_data.get('contact_number')
        fitnesscenter.email=self.cleaned_data.get('email')
        fitnesscenter.save()
        return user 
## FitnessCenter Profile Update Form
class FitnessCenterProfileUpdateForm(forms.ModelForm):
    class Meta():
        model = FitnessCenter
        fields = ['fitnesscenter_name','email','contact_number','fitnesscenter_profile_pic']

## Customer profile update form
class CustomerProfileUpdateForm(forms.ModelForm):
    class Meta():
        model = Customer
        fields = ['email','contact_number','customer_profile_pic']
class HiringRoleForm(forms.ModelForm):
    class Meta:
        model = HiringRole
        fields = ("title","role","salary","qualifications","responsibilities","gender")

class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ("title","category","number_of_sessions","hours_per_session","price","description","image")
       
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("comment", "rating")
    