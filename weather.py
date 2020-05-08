import time
from datetime import date
from datetime import datetime
import requests
import json
import pytemperature



url = "http://api.openweathermap.org/data/2.5/weather?lat=32.871&lon=-117.202&appid=3294e2836901a1399a3c094dc825a1b2"
response = requests.get(url)
url2 = 'http://api.openweathermap.org/data/2.5/uvi?lat=32.871&lon=-117.202&appid=3294e2836901a1399a3c094dc825a1b2'
response2 = requests.get(url2)
weather_get = json.loads(response.text)
weather_get2 = json.loads(response2.text)

weather_type = weather_get['weather'][0]['main']
temperature = str(round(pytemperature.k2f(weather_get['main']['temp']), 1)) + "°F"
temp_feels_like = str(round(pytemperature.k2f(weather_get['main']['feels_like']), 1)) + "°F"
cloud_percentage = str(weather_get['clouds']['all']) + "%"
wind = str(round(weather_get['wind']['speed'] * 2.23694, 1)) + 'MPH / ' + str(weather_get['wind']['deg']) + "°"
humidity = str(weather_get['main']['humidity']) + "%"
uv = str(int(round(weather_get2['value'], 0)))

weather_stats = [weather_type, temperature, temp_feels_like, cloud_percentage, wind, humidity, uv]
current_date = date.today()


# Printing minutes into time: '{:02d}:{:02d}'.format(*divmod(minutes, 60))

print('\nCurrent Weather: {}'.format(weather_type.capitalize()))
print('Current Temp: {}'.format(temperature))
print('Feels Like: {}'.format(temp_feels_like))
print('Cloud %: {}'.format(cloud_percentage))
print('Wind: {}'.format(wind))
print('Humidity: {}'.format(humidity))
print('UV Index Max: {}'.format(uv))
