from django import forms
from spongoApp.models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput, Textarea, FileInput,HiddenInput,NumberInput


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='',widget=TextInput(attrs={'class': 'form-control','placeholder': 'Username'}))
    password = forms.CharField(label='',widget=PasswordInput(attrs={'class': 'form-control','placeholder':'Password'}))

class spongoQuery(forms.Form):
	minimumBudget = forms.IntegerField(label='MinimumBudget',widget=NumberInput(attrs={'class': 'form-control','placeholder': 'minimumBudget'}))
	maximumBudget =  forms.IntegerField(label='maximumBudget',widget=NumberInput(attrs={'class': 'form-control','placeholder': 'maximumBudget'}))

	duration = forms.IntegerField(label='Length of trip',widget=NumberInput(attrs={'class': 'form-control','placeholder': 'Duration of trip'}))
	durationUnit = forms.ChoiceField(label="unit",choices=[(1,"Day(s)"),(2,"Week(s)"),(3,"Month(s)")])

	startingDestination1 = forms.CharField(max_length=3,label='',widget=TextInput(attrs={'class': 'form-control','placeholder': 'Starting Destination 1'}))
	startingDestination2 = forms.CharField(max_length=3,label='',widget=TextInput(attrs={'class': 'form-control','placeholder': 'Starting Destination 2'}))
	startingDestination3 = forms.CharField(max_length=3,label='',widget=TextInput(attrs={'class': 'form-control','placeholder': 'Starting Destination 3'}))