from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from .models import User, Customer,FitnessCenter, Program

class CustomerRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta(UserCreationForm.Meta):
        model = User
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.email=self.cleaned_data.get('email')
        user.save()
        customer = Customer.objects.create(user=user)
        customer.save()
        return user


class FitnessRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
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

class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ("title","category","number_of_sessions","hours_per_session","price","description","image")

         

    