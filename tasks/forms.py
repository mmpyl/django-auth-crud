#from   django.forms import ModelForm
from django import forms
from .models import Task

#Mediante esta clase se puede otorgar estilos a los imputs importando forms
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']
        widgets = {
            "title": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write a Tittle'}),
            "description": forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write a description'}),
            "important": forms.CheckboxInput(attrs={'class': 'form-check-input m-auto'}),
        }