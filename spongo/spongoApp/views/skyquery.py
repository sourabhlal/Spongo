import requests
import time
import urlparse

apikey = "ilw22874698541348193416710397562"

#Note: Postman is a nice extension

#Country is ISO code
#Currency is ISO code
#Departure is IATA code
#Destination is IATA code
#Date is YYYY-MM-DD
#Cabin is "Economy", "PremiumEconomy", "Business", "First"
def buildQueryData(country, currency, dep, dest, outdate, indate, cabin):
   data = {
   "Content-Type" : "application/x-www-form-urlencoded",
   "Accept" : "application/json",
   "country" : country,
   "currency" : currency,
   "locale" : "en-GB",
   "locationSchema" : "iata",
   "grouppricing" : "false",
   "originplace" : dep,
   "destinationplace" : dest,
   "outbounddate" : outdate,
   "inbounddate" : indate,
   "adults" : "1",
   "children" : "0",
   "infants" : "0",
   "cabinclass" : cabin}
   return data

def getSkyScannerRoutes(queryData):
   tries = 0
   r = requests.post("http://partners.api.skyscanner.net/apiservices/pricing/v1.0/?apikey="+apikey, data=queryData)
   try:
      results = requests.get(r.headers['Location'] + "?apiKey="+apikey).json()
   except:
      results = {}
      results['Status']="err"
   while results['Status']!="UpdatesComplete" and tries < 30:
      try:
         results = requests.get(r.headers['Location'] + "?apiKey="+apikey).json()
      except:
         results['Status']="err"
      tries+= 1
      time.sleep(1)
   return results

def getSkyScannerCosts(itinerary):
   prices = itinerary['PricingOptions']
   for i in prices:
      print itinerary['OutboundLegId'],":",u"\u20AC",i['Price']
   #print itinerary['OutboundLegId'],itinerary['PricingOptions']

def getSkyScannerSegments(itinerary):
   details = itinerary['BookingDetailsLink']
   r = requests.put("http://partners.api.skyscanner.net"+details['Uri']+"?apiKey="+apikey, data=urlparse.parse_qs("&"+details['Body']))
   if r.status_code == 201:
      results = requests.get(r.headers['Location']+"?apiKey="+apikey).json()
      segments = results['Segments']
      for s in segments:
         print "Flight",s['Carrier'],s['FlightNumber'],"Lasting",s['Duration']

#Initiates Sessions for countries with PIA VPN endpoints
#configured to avoid rate limit issues
def VPNResultSet(queryData):
   markets = {"US" : "United States", "UK" : "United Kingdom", "CH" : "Switzerland", "NL" : "Netherlands", "CA" : "Canada", "DE" : "Germany", "FR" : "France", "SE" : "Sweden", "RO" : "Romania", "HK" : "Hong Kong", "IL" : "Israel", "AU" : "Australia", "JP" : "Japan"}
   returnSet = []
   for m in markets:
      queryData['country'] = m
      returnSet.append(getSkyScannerRoutes(queryData))
      time.sleep(6)
   return returnSet


#print requests.get("http://partners.api.skyscanner.net/apiservices/reference/v1.0/countries/en-GB?apiKey="+apikey).json()

#Fun fact: If the airport code doesn't exist, this app crashes
query = buildQueryData("DE","EUR","HAM","BCN","2015-03-07","2015-03-14","Economy")
#VPNResultSet(query)

res = getSkyScannerRoutes(query)
itins = res['Itineraries']
for i in itins:
   #print i['BookingDetailsLink']
   getSkyScannerCosts(i)
   getSkyScannerSegments(i)



#http://partners.api.skyscanner.net/apiservices/pricing/v1.0/?apikey=ilw22874698541348193416710397562&inbounddate=2015-03-14&destinationplace=ULN&cabinclass=economy&adults=1&locale=en-GB&country=UK&outbounddate=2015-03-07&Accept=application%2Fjson&currency=GBP&originplace=IAD&locationSchema=iata&infants=0&grouppricing=false&Content-Type=application%2Fx-www-form-urlencoded&children=0