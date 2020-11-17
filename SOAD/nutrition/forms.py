from django import forms

class NutritionExtractionForm(forms.Form):
    title = forms.CharField(max_length=1000,label="Enter the name of food item")
    ingredients = forms.CharField(widget=forms.Textarea,label="Enter ingredients used. Enter each ingredient in a line")
