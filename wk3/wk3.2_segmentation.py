##########################
# Week 3.2: segmentation #
##########################
# importing libraries
import numpy as np

import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

import json # library to handle json files

from geopy.geocoders import Nominatim

import requests
from pandas.io.json import json_normalize

import matplotlib.cm as cm
import matplotlib.colors as colors

from sklearn.cluster import KMeans

import folium

# print('Libraries imported.')

####################################
# 1. Downloading dataset, plus eda #
####################################
import wget

# downloading json
url = "https://cocl.us/new_york_dataset"
# wget.download(url, 'newyork_data.json')

# print('Data Downloaded')

# loading and exploring
with open('newyork_data.json') as json_data:
    newyork_data = json.load(json_data)

newyork_data

# most relevant info is listed under the features key
# subsetting accordingly
neighborhoods_data = newyork_data['features']
neighborhoods_data[0]

# transforming data to a pandas dataframe

# step 1, defining column names
column_names = ['Borough', 'Neighborhood', 'Latitude', 'Longitude']

# step 2, declaring empty dataframe
neighborhoods = pd.DataFrame(columns=column_names)
print(neighborhoods)

# step 3, filling rows and columns by looping
for data in neighborhoods_data:
    borough = neighborhood_name = data['properties']['borough']
    neighborhood_name = data['properties']['name']

    neighborhood_latlon = data['geometry']['coordinates']
    neighborhood_lat = neighborhood_latlon[1]
    neighborhood_lon = neighborhood_latlon[0]

    neighborhoods = neighborhoods.append({'Borough': borough,
                                          'Neighborhood': neighborhood_name,
                                          'Latitude': neighborhood_lat,
                                          'Longitude': neighborhood_lon}, ignore_index=True)

# checking correct transference
neighborhoods.head()

# ensuring all neighborhoods present in the dataset
# print('The dataframe has {} boroughs and {} neighborhoods.'.format(
#         len(neighborhoods['Borough'].unique()),
#         neighborhoods.shape[0]
#     )
# )

# pulling coordinates for nyc using geopy
address = 'New York City, NY'

geolocator = Nominatim(user_agent="ny_explorer")
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print('The geographical coordinate of New York City are {}, {}.'.format(latitude, longitude))

# creating a map of nyc, with neighborhoods superimposed on top
map_newyork = folium.Map(location=[latitude, longitude], zoom_start=10)

for lat, lng, borough, neighborhood in zip(neighborhoods['Latitude'], neighborhoods['Longitude'], neighborhoods['Borough'], neighborhoods['Neighborhood']):
    label = '{}, {}'.format(neighborhood, borough)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        popup=label,
        color='blue',
        fill=True,
        fill_color='#3186cc',
        fill_opacity=0.7,
        parse_html=False).add_to(map_newyork)

map_newyork
map_newyork.save('map_newyork.html')

# slicing original dataframe to obtain only manhatten
manhattan_data = neighborhoods[neighborhoods['Borough'] == 'Manhattan'].reset_index(drop=True)
manhattan_data.head()

# grabbing geographical coordinates of Manhattan
address = "Manhattan, NY"

geolocator = Nominatim(user_agent="ny_explorer")
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print('The geographical coordinates of Manhattan are {}, {}.'.format(latitude, longitude))

# visualizing Manhattan plus neighborhoods in it
map_manhattan = folium.Map(location=[latitude, longitude], zoom_start=11)

# adding markers to map, ie plotting pts
for lat, lng, label in zip(manhattan_data['Latitude'], manhattan_data['Longitude'], manhattan_data['Neighborhood']):
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        popup=label,
        color='blue',
        fill=True,
        fill_color='#3186cc',
        fill_opacity=0.7,
        parse_html=False).add_to(map_manhattan)

print(map_manhattan)
map_manhattan.save('map_manhattan.html')

# using default foursquare api example
CLIENT_ID = 'QMGQSECG4KCJPOPJQKYUTDK5ETIN5AEAZXTB4A5JS2EUHT5C'
CLIENT_SECRET = 'MP0PLFHFZKZWSIBTON3EDPKGORQA5UKWWSSVGZPB4RP30TQQ'
VERSION = '20180605' # foursquare api version

print('Your credentials:' )
print('CLIENT_ID: ' + CLIENT_ID)
print('CLIENT_SECRET:' + CLIENT_SECRET)

# exploring first neighborhood in dataframe
manhattan_data.loc[0, 'Neighborhood']

# getting neighborhoods lat long info
neighborhood_latitude = manhattan_data.loc[0, 'Latitude']
neighborhood_longitude = manhattan_data.loc[0, 'Longitude']

neighborhood_name = manhattan_data.loc[0, 'Neighborhood']

print('Latitude and longitude values of {} are {}, {}.'.format(neighborhood_name,
                                                               neighborhood_latitude,
                                                               neighborhood_longitude))

# now identifying top 100 venues in marble hill, radius of 500 meters



















# in order to display plot within window
# plt.show()
