from django import forms
from .models import *
 
class CreateQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question','description']

class UpdateQuestionForm(forms.Form):
    question = forms.CharField(max_length=300,initial="",required=False)
    description = forms.CharField(max_length=1000,initial="",required=False)
 
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer']

class UpdateAnswerForm(forms.Form):
    answer = forms.CharField(max_length=1000)

