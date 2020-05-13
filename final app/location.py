#!/usr/bin/python
import psycopg2
from sys import argv, stderr, exit
import entryInfo
import googlemaps
import requests
import secrets
import math
import time 



def coordinateOffset(latitude, longitude):
    radius = 6371000.0 #radius of earth 
    sign = secrets.choice(range(0, 2)) #used to determine sign of the offset
    oLat = secrets.choice(range(500, 1200)) #offset in metres (700m - 1 mile)
    if (sign == 0):
        oLat = -1 * oLat
    sign = secrets.choice(range(0, 2)) #used to determine sign of the offset
    oLong = secrets.choice(range(500, 1200)) #offset in metres (700m - 1 mile)
    if (sign == 0):
        oLong = -1 * oLong
    new_latitude  = latitude  + (oLat / radius) * (180 / math.pi)
    new_longitude = longitude + (oLong / radius) * (180 / math.pi) / math.cos(latitude * math.pi/180)
    coordinates = [new_latitude, new_longitude]
    return coordinates





# returns latitude and longitude of a given address
def geocode(address):
    try:
        url = ('https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}'
            .format(address.replace(' ','+'), 'AIzaSyDQe5G3tqd5Vfwefn7w3Djrv1L1bmlKkTw'))

        response = requests.get(url)
        resp_json_payload = response.json()
        lat = resp_json_payload['results'][0]['geometry']['location']['lat']
        lng = resp_json_payload['results'][0]['geometry']['location']['lng']
        return lat, lng
    except Exception as e:
        print(e)