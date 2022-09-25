# https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}
# SAMPLE
#https://api.openweathermap.org/data/2.5/weather?lat=44.34&lon=10.99&appid={API key}

# opvragen locatie van sprang-capelle
# appid = clientID, verkregen na inloggen op openweather
 # https://api.openweathermap.org/geo/1.0/direct?q=sprang-capelle&limit=5&appid=c0374ffd6e363378fae57558a2e47be4

# eerst lat +  lon ophalen: 
# [
#    {
#         "name": "Sprang-Capelle",
#        "lat": 51.6705258,
#        "lon": 5.0252983,
#        "country": "NL",
#        "state": "North Brabant"
#    }
# ]

# dan opnemen in call:

# https://api.openweathermap.org/data/2.5/weather?lat=51.67&lon=5.02&appid=c0374ffd6e363378fae57558a2e47be4
# retourneert weerbericht lokaal
import requests

api_key = 'c0374ffd6e363378fae57558a2e47be4' 
city = 'sprang-capelle'
city = 'waalwijk'
# url = "http://api.openweathermap.org/geo/1.0/direct?q="{city name}&limit=5&appid=c0374ffd6e363378fae57558a2e47be4
url = "http://api.openweathermap.org/geo/1.0/direct?q="+ city + "&limit=5&appid=" + api_key +"&units=imperial"

#request = requests.get(url)
#json= request.json()
#print(json)

# for city in json:
#    print (city.get('name'))

#for city in json:
#    print (city.get('lat'))

# de eerste
#for i in json:
#    print(i.get('lon'))
lat = str(51.68)
lon =str(5.07)
url = "https://api.openweathermap.org/data/2.5/weather?lat=" + lat + "&lon=" + lon + "&appid=" + api_key  +"&units=imperial"

print(url)

request = requests.get(url)
json = request.json()
print (json)

description = json.get("weather")[0].get("description")
print ("weather forecast: " , description)

# let op syntax: eerste element van key weather, en dan key binnen element

temp_min= json.get("main").get("temp_min")
temp_max= json.get("main").get("temp_max")

print (temp_min, temp_max)
    