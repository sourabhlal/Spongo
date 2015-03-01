import urllib2
import json



ip_address = '80.169.79.69'
#Need to include ip_find function

usr_url = 'http://api.hostip.info/get_html.php?ip=%s&position=true' %ip_address

position = urllib2.urlopen(usr_url)
position.read() 
#returns ip location

print(position)

print('What is your current city?'),
location = 'barcelona' #as example


img_url = ('https://ajax.googleapis.com/ajax/services/search/images?' +
       'v=1.0&q=%s+city+hd+wallpaper&imgsz=xxlarge&as_filetype=jpg&userip=INSERT-USER-IP')%location #or position

request = urllib2.Request(img_url, None)
response = urllib2.urlopen(request)

# Process the JSON string.
results = json.load(response)
#print(results)
#print(results.keys())

imageArray= results['responseData']['results']

for image in imageArray:
	print(image['url'])