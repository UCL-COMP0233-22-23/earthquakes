# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
from cmath import inf
import requests
import json

# set the working directory
import os
os.chdir("/Users/sisiduan/Documents/SGDS/Research Software Engineering/Week 4/earthquakes")

def get_data():
    # With requests, we can ask the web service for the data.
    # Can you understand the parameters we are passing here?
    response = requests.get(
        "http://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
        params={
            'starttime': "2000-01-01",
            "maxlatitude": "58.723",
            "minlatitude": "50.008",
            "maxlongitude": "1.67",
            "minlongitude": "-9.756",
            "minmagnitude": "1",
            "endtime": "2018-10-11",
            "orderby": "time-asc"}
    )

    # The response we get back is an object with several fields.
    # The actual contents we care about are in its text field:
    text = response.text

    # To understand the structure of this text, you may want to save it
    # to a file and open it in VS Code or a browser.
    # See the README file for more information.
    with open('earthquake_data.json', 'w') as f:
        f.write(text)    # automatically format the file with Shift + Option + F

    # load the json file
    with open('earthquake_data.json', 'r') as f:
        earthquake_data_json = json.loads(f.read())

    # We need to interpret the text to get values that we can work with.
    # What format is the text in? How can we load the values?
    return earthquake_data_json


def count_earthquakes(data):
    """Get the total number of earthquakes in the response."""
    return len(data['features'])


def get_magnitude(earthquake: int):
    """Retrive the magnitude of an earthquake item."""
    return data['features'][earthquake]['properties']['mag']


def get_location(earthquake: int):
    """Retrieve the latitude and longitude of an earthquake item."""
    # There are three coordinates, but we don't care about the third (altitude)
    return [data['features'][earthquake]['geometry']['coordinates'][0], data['features'][earthquake]['geometry']['coordinates'][1]]


def get_maximum(data):
    """Get the magnitude and location of the strongest earthquake in the data."""
    max_mag, index = -inf, 0
    cnt = count_earthquakes(data)
    for i in range(cnt):
        if get_magnitude(i) > max_mag:
            max_mag = get_magnitude(i)
            index = i
    return get_magnitude(index), get_location(index)


# With all the above functions defined, we can now call them and get the result
data = get_data()
print(f"Loaded {count_earthquakes(data)}")
max_magnitude, max_location = get_maximum(data)
print(
     f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")