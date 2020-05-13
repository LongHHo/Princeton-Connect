import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyDQe5G3tqd5Vfwefn7w3Djrv1L1bmlKkTw')


# Geocoding an address
geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
print(geocode_result)

# Look up an address with reverse geocoding
reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

