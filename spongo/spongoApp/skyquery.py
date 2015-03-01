import requests
import time
import urlparse

__author__ = "Nick Lee"
__copyright__ = "Copyright (C) 2015 Nick Lee"
__license__ = "MIT License"

#Reminder to remove this before open sourcing
apikey = "ilw22874698541348193416710397562"

class FlightSegment:
   def __init__(self, arrivalDateTime, carrier, departureDateTime, destinationRNID, directionality, duration, flightnumber, operatingcarrier, originRNID):
      self.arrivalDateTime = arrivalDateTime
      self.departureDateTime = departureDateTime
      self.carrier = carrier
      self.destinationRNID = destinationRNID
      self.originRNID = originRNID
      self.directionality = directionality
      self.duration = duration
      self.flightnumber = flightnumber
      self.operatingcarrier = operatingcarrier
   def __str__(self):
      try:
         outstr = "".join(["[",self.directionality,"] ",airlineCache[self.carrier].iataCode,str(self.flightnumber),", Duration ",str(self.duration)," minutes from ",airportCache[self.originRNID].iataCode," to ",airportCache[self.destinationRNID].iataCode])
         return outstr
      except:
         return "err"


class FlightSet:
   def __init__(self, flightSegments, cost, currency, deeplink):
      self.flightSegments = flightSegments
      self.cost = round(cost, 2)
      self.currency = currency
      self.deeplink = deeplink
   def __str__(self):
      outstr = ""
      for s in self.flightSegments:
         if str(s) != "err":
            outstr += (str(s) + "\n")
      outstr+= "Trip Cost: "+self.currency+" "+str(self.cost)
      return outstr



#We can shoehorn places support if need be
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

#Tons of accessors
def airportObjectByKey(rnid):
   if rnid in airportCache:
      return airportCache[rnid]

def airlineObjectByKey(rnid):
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

#Takes JSON input, updates the cache
def buildAirportCache(results):
   airports = results['Places']
   for c in airports:
      #a = Airport(c['Code'], c['Id'], c['Name'], c['ParentId'], c['Type'])
      a = Airport(c['Code'], c['Id'], c['Name'], c['Type'])
      addAirportToCache(a)

def buildAirlineCache(results):
   carriers = results['Carriers']
   for c in carriers:
      a = Airline(c['Code'], c['DisplayCode'], c['Id'], c['ImageUrl'], c['Name'])
      addAirlineToCache(a)

#Also can be used as a modifier for the cache
def addAirportToCache(air):
   airportCache[air.rnid] = air

def addAirlineToCache(air):
   airlineCache[air.rnid] = air

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
   priceSum = 0.0
   count = 0
   for i in prices:
      priceSum += i['Price']
      count += 1
   return round(priceSum/count,2)
   #print itinerary['OutboundLegId'],itinerary['PricingOptions']

#Prints for now BC we don't understand the data struct
def getSkyScannerSegments_print(itinerary):
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
            print "\n"
            return False
      return True

def getSkyScannerSegments(itinerary):
   details = itinerary['BookingDetailsLink']
   r = requests.put("http://partners.api.skyscanner.net"+details['Uri']+"?apiKey="+apikey, data=urlparse.parse_qs("&"+details['Body']))
   if r.status_code == 201:
      results = requests.get(r.headers['Location']+"?apiKey="+apikey).json()
      segments = results['Segments']
      flightGroup = []
      for s in segments:
         try:
            if s['Directionality']=='Outbound':
               fs = FlightSegment(s['ArrivalDateTime'],s['Carrier'],s['DepartureDateTime'],s['DestinationStation'],"Outbound",s['Duration'],s['FlightNumber'],s['OperatingCarrier'],s['OriginStation'])
               flightGroup.append(fs)
            else:
               fs = FlightSegment(s['ArrivalDateTime'],s['Carrier'],s['DepartureDateTime'],s['DestinationStation'],"Inbound",s['Duration'],s['FlightNumber'],s['OperatingCarrier'],s['OriginStation'])
               flightGroup.append(fs)
         except:
            return False
      return flightGroup

def getSkyScannerSegments_raw(itinerary):
   details = itinerary['BookingDetailsLink']
   r = requests.put("http://partners.api.skyscanner.net"+details['Uri']+"?apiKey="+apikey, data=urlparse.parse_qs("&"+details['Body']))
   if r.status_code == 201:
      results = requests.get(r.headers['Location']+"?apiKey="+apikey)
      return results.text

#Add Endpoint to retrieve DeepLinks
#Return first DL
def getDeeplink(itinerary):
   for p in itinerary['PricingOptions']:
      #print "Debug:" + p['DeeplinkUrl']
      return p['DeeplinkUrl']


#Initiates Sessions for countries with PIA VPN endpoints
#configured to avoid rate limit issues. Experimental for use with
#multi-market searches. If we had time, money, and more servers,
#we'd actually operate proxies that would be used for purchasing from
#locations abroad.
def VPNResultSet(queryData):
   markets = {"US" : "United States", "UK" : "United Kingdom", "CH" : "Switzerland", "NL" : "Netherlands", "CA" : "Canada", "DE" : "Germany", "FR" : "France", "SE" : "Sweden", "RO" : "Romania", "HK" : "Hong Kong", "IL" : "Israel", "AU" : "Australia", "JP" : "Japan"}
   returnSet = []
   for m in markets:
      queryData['country'] = m
      res = getSkyScannerRoutes(queryData)
      returnSet.append(res)
      buildAirportCache(res)
      buildAirlineCache(res)
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

#Testing code
def demo():
   banner = '  /$$$$$$                                                    /$$           /$$       /$$        /$$$$$$  /$$$$$$$  /$$$$$$\n /$$__  $$                                                  | $$          |__/      | $$       /$$__  $$| $$__  $$|_  $$_/\n| $$  \\__/  /$$$$$$   /$$$$$$  /$$$$$$$   /$$$$$$   /$$$$$$ | $$  /$$$$$$  /$$  /$$$$$$$      | $$  \\ $$| $$  \\ $$  | $$  \n|  $$$$$$  /$$__  $$ /$$__  $$| $$__  $$ /$$__  $$ /$$__  $$| $$ /$$__  $$| $$ /$$__  $$      | $$$$$$$$| $$$$$$$/  | $$  \n \\____  $$| $$  \\ $$| $$  \\ $$| $$  \\ $$| $$  \\ $$| $$  \\ $$| $$| $$  \\ $$| $$| $$  | $$      | $$__  $$| $$____/   | $$  \n /$$  \\ $$| $$  | $$| $$  | $$| $$  | $$| $$  | $$| $$  | $$| $$| $$  | $$| $$| $$  | $$      | $$  | $$| $$        | $$  \n|  $$$$$$/| $$$$$$$/|  $$$$$$/| $$  | $$|  $$$$$$$|  $$$$$$/| $$|  $$$$$$/| $$|  $$$$$$$      | $$  | $$| $$       /$$$$$$\n \\______/ | $$____/  \\______/ |__/  |__/ \\____  $$ \\______/ |__/ \\______/ |__/ \\_______/      |__/  |__/|__/      |______/\n          | $$                           /$$  \\ $$                                                                        \n          | $$                          |  $$$$$$/                                                                        \n          |__/                           \\______/                                                                         '
   print banner
   time.sleep(1)
   #Fun fact: If the airport code doesn't exist, this app crashes
   #VPNResultSet(query)
   res = initiateSession("DE","EUR","HAM","PHL","2015-03-07","2015-03-14","Economy")
   itins = getItinerarySet(res)
   possibleRoutes = []
   
   #Non-Object Oriented
   for i in itins:
      price = getSkyScannerCosts(i)
      if(price!=None and getSkyScannerSegments_print(i)):
         print "Trip Cost: "+u"\u20AC"+str(getSkyScannerCosts(i))+"\n"

   #Avoids getting locked out for request flooding
   time.sleep(10)
   res = initiateSession("DE","EUR","HAM","PHL","2015-03-07","2015-03-14","Economy")
   itins = getItinerarySet(res)
   possibleRoutes = []
   for i in itins:
      price = getSkyScannerCosts(i)
      dl = getDeeplink(i)
      print "DEBUG: "+dl
      if(price!=None):
         segs = getSkyScannerSegments(i)
         if(segs != False and segs != None):
            possibleRoutes.append(FlightSet(segs, getSkyScannerCosts(i), "EUR"))
            print FlightSet(segs, getSkyScannerCosts(i), "EUR", dl)
            print ""



   #print getSkyScannerRoutes_raw(query)

demo()