from bs4 import BeautifulSoup
import urllib2
from django.shortcuts import render
from spongoApp.forms import *
import xml.etree.ElementTree as ET
from django.http import HttpResponse

currencyCode = {}

#Returns list with {name, url} objects
def getCountries(url):
	response=urllib2.urlopen(url)
	html = response.read()
	soup = BeautifulSoup(html)

	placeContainer = soup.findAll("ul", { "class" : "placelist flow" })
	containerSoup = BeautifulSoup(' '.join([str(x) for x in placeContainer]))
	places = containerSoup.findAll('a')

	placeList=[]

	for tags in places:
		entries = {
					  'name' : tags.text,
					  'url' : tags.get('href')[2:] #ignore leading //
					}
		placeList.append(entries)
	return placeList


#country: {'name': , 'url': }
def getCountryInfo(country):
	url = "http://"+country['url']
	name = country['name']
	response=urllib2.urlopen(url)
	html = response.read()
	soup = BeautifulSoup(html)
	dataTableHtml = soup.findAll('div', {'class':'datatable'})
	
	brokenCategoriesSoup = BeautifulSoup(' '.join([str(x) for x in dataTableHtml]))
	
	average = brokenCategoriesSoup.select('tr.country')
	if len(average) > 0:
		average = average[0].find('span', {'class':'curvalue'})
	else:
		average = None
	if average is not None:
		average = average.text
	else:
		average = "0.0"
	countryDetails = {'average' : average}
	rows = brokenCategoriesSoup.select('tr.category')

	#first one is average so ignore
	for row in rows[1:]:
		category = row.find('td', {'class' : 'category'}).text[:-1]
		price = row.find('td', {'class' : 'value'})
		price = price.find('span', {'class': 'curvalue'}).text
		countryDetails[category] = price 

	return countryDetails


def getAll(baseurl):
	countries = getCountries(baseurl)
	for country in countries:
		print country['name']
		print getCountryInfo(country)




def getCurrencyCodes():
	tree = ET.ElementTree(file='spongoApp/views/CurrencyCodes.xml')
	root = tree.getroot()
	#get the first child
	currencyTable = root.getchildren()[0]
	for tags in currencyTable.findall('CcyNtry'):
		name = tags.find('CtryNm').text
		ccode = tags.find('Ccy')
		if ccode is None:
			continue
		currencyCode[name.lower()] = ccode


def populate(arg):
	#baseurl = 'http://www.budgetyourtrip.com/countrylist.php'
	#countries = getCuontries(baseurl)
	#for country in countries:
	getCurrencyCodes()
	countries = getCountries('http://www.budgetyourtrip.com/countrylist.php')
	for country in countries:
		details = getCountryInfo(country)
		CostOfLiving(
				country_name = country['name'].lower(),
				averageCost = float(details['average'].replace(',','')) if 'average' in details.keys() else 0,
				accomodation = float(details['Accomodation'].replace(',','')) if 'Accomodation' in details.keys() else 0,
				food = float(details['Food'].replace(',','')) if 'Food' in details.keys() else 0,
				water = float(details['Water'].replace(',','')) if 'Water' in details.keys() else 0,
				local_transportation = float(details['Local Transportation'].replace(',','')) if 'Local Transportation' in details.keys() else 0,
				entertainment = float(details['Entertainment'].replace(',','')) if 'Entertainment' in details.keys() else 0,
				communication = float(details['Communication'].replace(',','')) if 'Communication' in details.keys() else 0,
				tips = float(details['Tips and Handouts'].replace(',','')) if 'Tips and Handouts' in details.keys() else 0,
				intercity_transport = float(details['Intercity Transportation'].replace(',','')) if 'Intercity Transportation' in details.keys() else 0, 
				souvenirs = float(details['Souvenirs'].replace(',','')) if 'Souvenirs' in details.keys() else 0,
				scams_robberies_mishaps = float(details['Scams, Robberies, and Mishaps'].replace(',','')) if 'Scams, Robberies, and Mishaps' in details.keys() else 0,
				alcohol = float(details['Alcohol'].replace(',','')) if 'Alcohol' in details.keys() else 0
		)
	testhtml = '<html><body>Yo!</body></html>' #coz yo
	return HttpResponse(testhtml)