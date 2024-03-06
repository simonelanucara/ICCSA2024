#!/usr/bin/env python
# coding: utf-8

# In[44]:


#!pip install geojsonio
import os
import json
import requests
import geojsonio
import time

# Helper function to printformatted JSON using the json module
def p(data):
    print(json.dumps(data, indent=2))

# if your Planet API Key is not set as an environment variable, you can paste it below
if os.environ.get('PL_API_KEY', ''):
    API_KEY = os.environ.get('PL_API_KEY', '')
else:
    API_KEY = 'YOUR_API_KEY'

    # construct auth tuple for use in the requests library
BASIC_AUTH = (API_KEY, '')

# Setup Planet Data API base URL
URL = "https://api.planet.com/data/v1"

# Setup the session
session = requests.Session()

# Authenticate
session.auth = (API_KEY, "")

# Make a GET request to the Planet Data API
res = session.get(URL)

# Response status code
res.status_code

# Response Body
res.text

# Print formatted JSON response
p(res.json())

# Print the value of the item-types key from _links
print(res.json()["_links"]["item-types"])


# Setup the stats URL
stats_url = "{}/stats".format(URL)

# Print the stats URL
print(stats_url)

# Specify the sensors/satellites or "item types" to include in our results
item_types = ["PSScene"]

# Create filter object for all imagery captured between 2013-01-01 and present.
date_filter = {
    "type": "DateRangeFilter", # Type of filter -> Date Range
    "field_name": "acquired", # The field to filter on: "acquired" -> Date on which the "image was taken"
    "config": {
        "gte": "2023-01-01T00:00:00.000Z", # "gte" -> Greater than or equal to
    }
}


# In[45]:


# Search for imagery only from 2023 and on
# Construct the request.
request = {
    "item_types" : item_types,
    "interval" : "year",
    "filter" : date_filter
}

# Send the POST request to the API stats endpoint
res = session.post(stats_url, json=request)

# Print response
p(res.json())


# In[46]:


# Search for imagery only from PlanetScope satellites that have a PSB.SD telescope (SuperDove)

# Setup item types
item_types = ["PSScene"]

# Setup a filter for instrument type
instrument_filter = {
    "type": "StringInFilter",
    "field_name": "instrument",
    "config": ["PSB.SD"]
}

request = {
    "item_types" : item_types,
    "interval" : "year",
    "filter" : instrument_filter
}

# Send the POST request to the API stats endpoint
res = session.post(stats_url, json=request)

# Print response
p(res.json())



# In[47]:


# Search for imagery regarding our study

# Setup GeoJSON 
geom = {"type": "Polygon",
    "features":[],
 "coordinates":[
          [
            [
              11.970561413875544,
              44.88757641989034
            ],
            [
              11.904770313945676,
              44.889311351256
            ],
            [
              11.911463701283111,
              44.84082925022912
            ],
            [
              11.978887334710038,
              44.82462087948082
            ],
            [
              11.990641575888617,
              44.83828252242304
            ],
            [
              12.008436191006325,
              44.86119902026684
            ],
            [
              12.009742217803876,
              44.866868867346625
            ],
            [
              11.970561413875544,
              44.88757641989034
            ]
          ]
        ]
}

# Setup Geometry Filter
geometry_filter = {
    "type": "GeometryFilter",
    "field_name": "geometry",
    "config": geom
}

# Setup the request
request = {
    "item_types" : item_types,
    "interval" : "year",
    "filter" : geometry_filter
}

# Send the POST request to the API stats endpoint
res=session.post(stats_url, json=request)

# Print response
p(res.json())


# In[54]:


#Search for images with cloud cover less than 20%

#
cloud_filter= {
  "type": "RangeFilter",
  "field_name": "cloud_cover",
  "config": {
    "lt": 0.1,
    "gt": 0
  }
}

request = {
    "item_types" : item_types,
    "interval" : "year",
    "filter" : cloud_filter
}

# Send the POST request to the API stats endpoint
res = session.post(stats_url, json=request)

# Print response
p(res.json())


# In[55]:


# PSB.SD imagery; over study area; captured between 2023 and present

# Setup an "AND" logical filter
and_filter = {
    "type": "AndFilter",
    "config": [instrument_filter, geometry_filter, date_filter,cloud_filter]
}

# Print the logical filter
p(and_filter)

# Setup the request
request = {
    "item_types" : item_types,
    "interval" : "year",
    "filter" : and_filter
}

# Send the POST request to the API stats endpoint
res=session.post(stats_url, json=request)

# Print response
p(res.json())


# In[ ]:




