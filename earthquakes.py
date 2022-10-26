# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
from itertools import count
from textwrap import indent
import requests
import json

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
    with open("data.json", "w") as file:
        file.write(text)

    # We need to interpret the text to get values that we can work with.
    # What format is the text in? How can we load the values?
    return json.loads(text)

def count_earthquakes(data):
    """Get the total number of earthquakes in the response."""
    return data["metadata"]["count"]


def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    return earthquake["properties"]["mag"]


def get_location(earthquake):
    """Retrieve the latitude and longitude of an earthquake item."""
    # There are three coordinates, but we don't care about the third (altitude)
    return tuple(earthquake["geometry"]["coordinates"][0:2])


def get_maximum(data):
    """Get the magnitude and location of the strongest earthquake in the data."""
    earthquake_magnitudes = [get_magnitude(earthquake) for earthquake in data["features"]]
    earthquake_locations = [get_location(earthquake) for earthquake in data["features"]]
    max_magnitude = max(earthquake_magnitudes)
    max_magnitude_indices = [i for i, j in enumerate(earthquake_magnitudes) if j == max_magnitude]
    max_magnitude_locations = [earthquake_locations[i] for i in max_magnitude_indices]
    return (max_magnitude, max_magnitude_locations)




# With all the above functions defined, we can now call them and get the result
data = get_data()
print(f"Loaded {count_earthquakes(data)}")
max_magnitude, max_locations = get_maximum(data)
for location in max_locations:
    print(f"One of the strongest earthquakes was at {location} with magnitude {max_magnitude}") if len(max_locations) > 1 else print(f"The strongest earthquake was at {location} with magnitude {max_magnitude}") 