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

	query = buildQueryData("DE","EUR","HAM","BCN","2015-03-11","2015-03-14","Economy")
	getSkyScannerRoutes(query)
	res = getSkyScannerRoutes(query)
	prices = []
	carrier = []
	flightNumber = []
	duration = []
	itins = res['Itineraries']
	for it in itins:
		Itincost = getSkyScannerCosts(it)
   		for i in Itincost:
   			prices.append(i['Price'])
		Itinsegm = getSkyScannerSegments(i)
		for i in Itinsegm:
			carrier.append(i['Carrier'])
			flightNumber.append(i['FlightNumber'])
			duration.append(i['Duration'])


   	flightDetails = zip(prices,carrier,flightNumber,duration)

	context['flightDetails'] = flightDetails

	return render(request, 'testing.html', context)

