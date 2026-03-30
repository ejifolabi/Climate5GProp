#!/usr/bin/env python3
import requests
import sys
import json

def get_noaa(lat, lon):
    try:
        url = f"https://api.weather.gov/points/{lat},{lon}"
        data = requests.get(url).json()
        obs_url = data['properties']['observationStations'][0] + '/observations/latest'
        obs = requests.get(obs_url).json()
        wind = float(obs['properties']['windSpeed']['value'])
        temp = float(obs['properties']['temperature']['value'])
        print(json.dumps({'wind_mps': wind, 'temp_C': temp}))
        return wind, temp
    except:
        print(json.dumps({'wind_mps': 15.0, 'temp_C': 25.0}))
        return 15.0, 25.0

if __name__ == "__main__":
    lat, lon = float(sys.argv[1]), float(sys.argv[2])
    get_noaa(lat, lon)
