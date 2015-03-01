from django.shortcuts import render
from spongoApp.forms import *
from spongoApp.views.getComparativeData import *
from spongoApp.views.skyquery import *


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

	query = buildQueryData("DE","EUR","HAM","BCN","2015-03-07","2015-03-14","Economy")
	getSkyScannerRoutes(query)
	res = getSkyScannerRoutes(query)
	p = []
	s = []
	itins = res['Itineraries']
	for i in itins:
   		#print i['BookingDetailsLink']
   		p.append(getSkyScannerCosts(i))
   		s.append(getSkyScannerSegments(i))

   	flightDetails = zip(s,p)

	context['flightDetails'] = flightDetails

	return render(request, 'testing.html', context)

