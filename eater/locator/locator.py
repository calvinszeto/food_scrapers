import json
import math
import urllib
import pprint
from urllib2 import urlopen

class Locator:

    _locations = []

    def __init__(self, locations_file):
        with open(locations_file, "r") as f:
            self._locations = json.JSONDecoder().decode(json.load(f))

    def _geocode(self, address):
        url = ("https://maps.googleapis.com/maps/api/geocode/json?"
               "address={}&sensor=false&key=AIzaSyDoxUfm0UVU8vMbto7lXPKDDTD2BbAYFAI").format(urllib.quote(address))
        return json.loads(urlopen(url).read())

    def _deg2rad(self, deg):
        return deg * (math.pi/180)

    def _distance(self, loc1, loc2):
        R = 6371 # Radius of the earth in km
        lat1 = loc1["geometry"]["location"]["lat"]
        lon1 = loc1["geometry"]["location"]["lng"]
        lat2 = loc2["geometry"]["location"]["lat"]
        lon2 = loc2["geometry"]["location"]["lng"]
        d_lat = self._deg2rad(lat2-lat1)  
        d_lon = self._deg2rad(lon2-lon1) 
        a = math.sin(d_lat/2) * math.sin(d_lat/2) + math.cos(self._deg2rad(lat1)) * math.cos(self._deg2rad(lat2)) * math.sin(d_lon/2) * math.sin(d_lon/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        d = R * c 
        return d

    def nearest(self, address):
        curr_location = self._geocode(address)["results"][0]
        nearest_locations = [(location, self._distance(curr_location, location)) for location in self._locations] 
        nearest_locations.sort(key=lambda t: t[-1])
        return nearest_locations

if __name__ == "__main__":
    locator = Locator("../data/geocoded_restaurants.json")
    pprint.PrettyPrinter(indent=4).pprint([location[0]["name"] for location in locator.nearest(sys.argv[1])])
    
