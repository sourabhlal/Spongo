from django.shortcuts import render
from spongoApp.forms import *
from spongoApp.views.getComparativeData import *
from spongoApp.skyquery import *
import datetime


def home(request):
	context = {}
	context['QueryForm'] = spongoQuery()
	return render(request, 'homepage.html', context)

def results(request):
	context = {}
	if request.method == "GET":
		return redirect('/home')
	
	form = spongoQuery(request.POST)
	context['QueryForm'] = form
	if not form.is_valid():
		return render(request, 'homepage.html', context)
	data = form.cleaned_data
	today = datetime.date.today()
	s = today + datetime.timedelta(days=1)
	if data['durationUnit'] == 1:
		tripDuration = data['duration']
	elif data['durationUnit'] == 2:
		tripDuration = 7*int(data['duration'])
	else:
		tripDuration = 30*int(data['duration'])
	f = s + datetime.timedelta(days=tripDuration)
	
	#parameters for api query:
	minBudget = data['minimumBudget']
	maxBudget = data['maximumBudget']
	start = s.strftime('%Y-%d-%m')
	finish = s.strftime('%Y-%d-%m')
	startIATACode = data['startingPoint']
	finalIATACode = data['landingPoint']

	query = buildQueryData("DE","EUR","HAM","BCN","2015-03-11","2015-03-14","Economy")
	getSkyScannerRoutes(query)
	res = getSkyScannerRoutes(query)
	prices = []
	fgOUT = []
	fgIN = []
	itins = res['Itineraries']
	for it in itins:
		Itincost = getSkyScannerCosts(it)
   		prices.append(Itincost)
   		fgOUT.append(getSkyScannerSegments(it)[0])
   		fgIN.append(getSkyScannerSegments(it)[1])

   	flightDetails = zip(prices,fgOUT)
   	context['flightDetails'] = flightDetails

	return render(request, 'results.html', context)



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
	fgOUT = []
	fgIN = []
	itins = res['Itineraries']
	for it in itins:
		Itincost = getSkyScannerCosts(it)
   		for i in Itincost:
   			prices.append(i['Price'])
   		fgOUT.append(str(getSkyScannerSegments(it)[0]))
   		fgIN.append(str(getSkyScannerSegments(it)[1]))

   	flightDetails = zip(prices,fgOUT)

	context['flightDetails'] = flightDetails

	return render(request, 'testing.html', context)

