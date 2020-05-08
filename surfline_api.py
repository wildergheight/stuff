import time
from datetime import date
from datetime import datetime
import requests
import json
import pytemperature


class tide:
    def __init__(self):
        self.hi_lo = ''
        self.height = ''
        self.timestamp = 0


def getSurf():
    tides = []

    url = "https://services.surfline.com//kbyg/spots/reports?spotId=5842041f4e65fad6a77088cc"
    response = requests.get(url)

    surf_get = json.loads(response.text)
    surf_name = surf_get['spot']['name']
    surf_conditions = surf_get['forecast']['conditions']['value']
    surf_wind = surf_get['forecast']['wind']['speed']
    surf_wind_direction = surf_get['forecast']['wind']['direction']
    # convert direction to onshore, cross-wind, or offshore direction
    surf_wave_min = surf_get['forecast']['waveHeight']['min']
    surf_wave_max = surf_get['forecast']['waveHeight']['max']
    surf_wave_desc = surf_get['forecast']['waveHeight']['humanRelation']

    def getTide(tide_loads, prev_current_next):
        if prev_current_next == 0:
            indicator = 'previous'
        elif prev_current_next == 1:
            indicator = 'current'
        else:
            indicator = 'next'
        next_tide = tide()
        next_tide.hi_lo = tide_loads['forecast']['tide'][indicator]['type']
        next_tide.height = tide_loads['forecast']['tide'][indicator]['height']
        next_tide.timestamp = tide_loads['forecast']['tide'][indicator]['timestamp']

        return next_tide

    prev_tide = getTide(surf_get, 0)
    current_tide = getTide(surf_get, 1)
    future_tide = getTide(surf_get, 2)

    water_temp = round((surf_get['forecast']['waterTemp']['max'] + surf_get['forecast']['waterTemp']['min']) / 2, 0)

    air_temp = surf_get['forecast']['weather']['temperature']
    weather_description = surf_get['forecast']['weather']['condition']
    results = [surf_name, water_temp, surf_conditions, surf_wind, surf_wave_min, surf_wave_max, surf_wave_desc,
               prev_tide, current_tide, future_tide, air_temp]
    return results


stats = getSurf()

print('\n')
print('Last Updated at: {}'.format(datetime.now()))
print('\nCurrent Spot: {}'.format(stats[0].upper()))
print('Current Water Temp: {}'.format(stats[1]))
print('Current Air Temp: {}'.format(stats[10]))
print('Conditions: {}'.format(stats[2]))
print('Wind: {} mph'.format(stats[3]))
print('Wave Min: {} ft'.format(stats[4]))
print('Wave Max: {} ft'.format(stats[5]))
print('Wave Description: {}'.format(stats[6]))
print('Previous Tide: {} {}'.format(stats[7].hi_lo, datetime.fromtimestamp(stats[7].timestamp)))
print('Current Tide: {} {}'.format(stats[8].hi_lo, datetime.fromtimestamp(stats[8].timestamp)))
print('Next Tide: {} {}'.format(stats[9].hi_lo, datetime.fromtimestamp(stats[9].timestamp)))
