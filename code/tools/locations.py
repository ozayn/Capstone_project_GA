### Here is a class for handling fetching locations.



import pycountry_convert as pc
from geopy.geocoders import Nominatim

class LocH():
  def __init__(self):
    pass

  def get_longitude_latitude(self, address):
    """
    Extract longitude and latitude
    """
    geolocator = Nominatim(user_agent="http")
    location = geolocator.geocode(address)
    if location!=None:
      return {
          'latitude':location.latitude,
          'longitude':location.longitude
      }

  def country_to_continent(self, country_name):
    """
    Taken with modification from https://stackoverflow.com/questions/55910004/get-continent-name-from-country-using-pycountry
    example: country_to_continent('British Virgin Islands')
    """
    try:
      if len(country_name.split(';'))>1:
        return ';'.join([country_to_continent(c) for c in country_name.split(';')])
    except Exception as e:
      return country_name

    try:
      country_alpha2 = pc.country_name_to_country_alpha2(country_name)
      country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
      country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
      return country_continent_name
    except Exception as e:
      print(country_name, e)
      return ''