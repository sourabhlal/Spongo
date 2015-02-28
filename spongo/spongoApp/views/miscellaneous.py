from django.shortcuts import render
from spongoApp.forms import *
from spongoApp.views.skyquery import *
from spongoApp.views.getComparativeData import *

def home(request):
	context = {}
	return render(request, 'homepage.html')

def testing(request):
	context = {}
	if request.method == "GET":
		context['QueryForm'] = spongoQuery()
		return render(request, 'testing.html', context)
	form = spongoQuery(request.POST)
	context['QueryForm'] = form
	if not form.is_valid():
		return render(request, 'testing.html', context)
	data = form.cleaned_data

	#parameters for api query:
	#data['minimumBudget']
	#data['maximumBudget']
	#data['duration']
	#data['durationUnit']
	#data['startingDestination1']
	#data['startingDestination2']
	#data['startingDestination3']

	#get JSON
	context["results"] = data['minimumBudget']
	return render(request, 'testing.html', context)
