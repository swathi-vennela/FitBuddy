from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from .models import User, Customer,FitnessCenter

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
        customer.save()
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
        fitnesscenter.save()
        return user      