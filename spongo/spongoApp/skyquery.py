import requests
import time
import urlparse

apikey = "ilw22874698541348193416710397562"

#We can shoehorn places if need be
#Edge case, no time or sleep.
#Removed parentID because it was bugged
class Airport:
   #def __init__(self, code, nid, cname, pid, ctype):
   def __init__(self, code, nid, cname, ctype):
      self.iataCode = code
      self.rnid = nid
      self.colloquialName = cname
      #self.parentID = pid
      self.contentType = ctype

class Airline:
   def __init__(self, code, dcode, nid, logo, cname):
      self.iataCode = code
      self.displayCode = dcode
      self.rnid = nid
      self.carrierLogoURL = logo
      self.colloquialName = cname

airportCache = {}
airlineCache = {}

def addAirport(air):
   airportCache[air.rnid] = air

def addAirline(air):
   airlineCache[air.rnid] = air

#Both of these are pretty useless I think
#Raw dict access is usable, and I'm too tired to debug
def lookupAirportByKey(rnid):
   if rnid in airportCache:
      return airportCache[rnid]

def lookupAirlineByKey(rnid):
   if rnid in airportCache:
      return airportCache[rnid]

def iataAirportByKey(rnid):
   if rnid in airportCache:
      return airportCache[rnid].iataCode

def iataAirlineByKey(rnid):
   if rnid in airlineCache:
      return airlineCache[rnid].iataCode

def airlineLogoByKey(rnid):
   if rnid in airlineCache:
      return airlineCache[rnid].carrierLogoURL

def airlineNameByKey(rnid):
   if rnid in airlineCache:
      return airlineCache[rnid].colloquialName

def airportNameByKey(rnid):
   if rnid in airportCache:
      return airportCache[rnid].iataCode

#Takes JSON
def buildAirportCache(results):
   airports = results['Places']
   for c in airports:
      #a = Airport(c['Code'], c['Id'], c['Name'], c['ParentId'], c['Type'])
      a = Airport(c['Code'], c['Id'], c['Name'], c['Type'])
      addAirport(a)

def buildAirlineCache(results):
   carriers = results['Carriers']
   for c in carriers:
      a = Airline(c['Code'], c['DisplayCode'], c['Id'], c['ImageUrl'], c['Name'])
      addAirline(a)

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

def getSkyScannerRoutes_raw(queryData):
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
   return requests.get(r.headers['Location'] + "?apiKey="+apikey).text

def getSkyScannerCosts(itinerary):
   prices = itinerary['PricingOptions']
   for i in prices:
      print itinerary['OutboundLegId'],":",u"\u20AC",i['Price']
   #print itinerary['OutboundLegId'],itinerary['PricingOptions']

#Prints for now BC we don't understand the data struct
def getSkyScannerSegments(itinerary):
   details = itinerary['BookingDetailsLink']
   r = requests.put("http://partners.api.skyscanner.net"+details['Uri']+"?apiKey="+apikey, data=urlparse.parse_qs("&"+details['Body']))
   if r.status_code == 201:
      results = requests.get(r.headers['Location']+"?apiKey="+apikey).json()
      segments = results['Segments']
      for s in segments:
         try:
            if s['Directionality']=='Outbound':
               print "=> Flight",airlineCache[s['Carrier']].iataCode,s['FlightNumber'],"Lasting",s['Duration'],"minutes from",airportCache[s['OriginStation']].iataCode,"to",airportCache[s['DestinationStation']].iataCode
            else:
               print "<= Flight",airlineCache[s['Carrier']].iataCode,s['FlightNumber'],"Lasting",s['Duration'],"minutes from",airportCache[s['OriginStation']].iataCode,"to",airportCache[s['DestinationStation']].iataCode
         except:
            pass

def getSkyScannerSegments_raw(itinerary):
   details = itinerary['BookingDetailsLink']
   r = requests.put("http://partners.api.skyscanner.net"+details['Uri']+"?apiKey="+apikey, data=urlparse.parse_qs("&"+details['Body']))
   if r.status_code == 201:
      results = requests.get(r.headers['Location']+"?apiKey="+apikey)
      return results.text


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

#Wrapper to initiate session, run aux. functions, and return results
def initiateSession(country, currency, dep, dest, outdate, indate, cabin):
   query = buildQueryData(country, currency, dep, dest, outdate, indate, cabin)
   res = getSkyScannerRoutes(query)
   buildAirportCache(res)
   buildAirlineCache(res)
   return res

def getItinerarySet(initialResults):
   r = initialResults['Itineraries']
   return r

#print requests.get("http://partners.api.skyscanner.net/apiservices/reference/v1.0/countries/en-GB?apiKey="+apikey).json()

#Fun fact: If the airport code doesn't exist, this app crashes
#VPNResultSet(query)
res = initiateSession("DE","EUR","HAM","PHL","2015-03-07","2015-03-14","Economy")
#print airportCache
#print airlineCache
itins = getItinerarySet(res)
for i in itins:
   #print i['BookingDetailsLink']
   #getSkyScannerCosts(i)
   getSkyScannerSegments(i)
   #print getSkyScannerSegments_raw(i)

#print getSkyScannerRoutes_raw(query)





def get_airport(city):
   headers = {
      'User-Agent': 'kayakandroidphone/6.3.1',
      'Accept-Encoding': 'gzip,deflate',
      'Accept-Language': 'en-US',
      'Host': 'www.kayak.com',
      'Connection': 'Keep-Alive'
   }

   url = 'https://www.kayak.com/f/smarty?lc=en&lc_cc=US&s=1&where={city}&f=t'.format(city=city)

   r = requests.get(url, headers=headers)
   code = r.text.encode('ascii', 'ignore').split('\n')[0].split('[')[-1].split('/')[0].strip()
   return code


#http://partners.api.skyscanner.net/apiservices/pricing/v1.0/?apikey=ilw22874698541348193416710397562&inbounddate=2015-03-14&destinationplace=ULN&cabinclass=economy&adults=1&locale=en-GB&country=UK&outbounddate=2015-03-07&Accept=application%2Fjson&currency=GBP&originplace=IAD&locationSchema=iata&infants=0&grouppricing=false&Content-Type=application%2Fx-www-form-urlencoded&children=0
