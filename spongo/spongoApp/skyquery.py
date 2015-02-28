import requests
import time

apikey = "ilw22874698541348193416710397562"

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

def getSkyScannerResults(queryData):
   tries = 0
   r = requests.post("http://partners.api.skyscanner.net/apiservices/pricing/v1.0/?apikey="+apikey, data=queryData)
   try:
      results = requests.get(r.headers['Location'] + "?apiKey="+apikey).json()
   except E:
      results['Status']="err"
   while results['Status']!="UpdatesComplete" and tries < 30:
      try:
         results = requests.get(r.headers['Location'] + "?apiKey="+apikey).json()
      except:
         results['Status']="err"
      tries+= 1
      time.sleep(1)
   return results

query = buildQueryData("DE","EUR","BRE","ULN","2015-03-07","2015-03-14","economy")
print getSkyScannerResults(query)

#http://partners.api.skyscanner.net/apiservices/pricing/v1.0/?apikey=ilw22874698541348193416710397562&inbounddate=2015-03-14&destinationplace=ULN&cabinclass=economy&adults=1&locale=en-GB&country=UK&outbounddate=2015-03-07&Accept=application%2Fjson&currency=GBP&originplace=IAD&locationSchema=iata&infants=0&grouppricing=false&Content-Type=application%2Fx-www-form-urlencoded&children=0
