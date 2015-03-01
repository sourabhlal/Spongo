from django import forms
from spongoApp.models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput, Textarea, FileInput,HiddenInput,NumberInput

class spongoQuery(forms.Form):
	minimumBudget = forms.IntegerField(label='',widget=NumberInput(attrs={'class': 'form-control'}))
	maximumBudget =  forms.IntegerField(label='',widget=NumberInput(attrs={'class': 'form-control'}))
	duration = forms.IntegerField(label='',widget=NumberInput(attrs={'class': 'form-control','placeholder': 'Duration of trip'}))
	durationUnit = forms.ChoiceField(label='',choices=[(1,"Day(s)"),(2,"Week(s)"),(3,"Month(s)")], widget=forms.Select(attrs={'class':'form-control'}))
	startingPoint = forms.CharField(max_length=3,label='',widget=TextInput(attrs={'class': 'form-control','placeholder': 'Starting Destination'}))