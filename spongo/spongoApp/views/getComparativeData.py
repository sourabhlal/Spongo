from bs4 import BeautifulSoup
import urllib2
from django.shortcuts import render
from spongoApp.forms import *

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
	average = average[0].find('span', {'class':'curvalue'}).text
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



getAll('http://www.budgetyourtrip.com/countrylist.php')
