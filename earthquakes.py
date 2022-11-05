# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
import requests
import json

def get_data():
    # With requests, we can ask the web service for the data.
    # Can you understand the parameters we are passing here?
    #paramters will be append to url and final url is ...geojson?starttime=2000-01-01...
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
    #loads() takes in a string and returns a json object. json. dumps() takes in a json object and returns a string.
    #save text as json file
    # To understand the structure of this text, you may want to save it
    earthquake_data = json.loads(text)
    with open('earthquake_data.json', 'w',encoding='utf-8') as f:
        f.write(text)
    # to a file and open it in VS Code or a browser.
    # See the README file for more information.
    # We need to interpret the text to get values that we can work with.
    # What format is the text in? How can we load the values?
    return earthquake_data

def count_earthquakes(data):
    """Get the total number of earthquakes in the response."""
    return len(data['features'])
# feature is one key in data which contains lists of information needed
#type(data) is dic, type(data['feature']) is list

def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    return earthquake["properties"]["mag"]
#print(data['features'][3]['properties']['mag'])
#need to notice, feature is the key of dictionary
#the earthquake here stand for list

def get_location(earthquake):
    """Retrieve the latitude and longitude of an earthquake item."""
    # There are three coordinates, but we don't care about the third (altitude)
    return [earthquake['geometry']['coordinates'][0], earthquake['geometry']['coordinates'][1]]


def get_maximum(data):
    """Get the magnitude and location of the strongest earthquake in the data."""
    # use max function to find max magnitude among every rows in list
    #e stand for earthquake
    # the data['feature'] nor get_magnitude returns the list of magnitude to run max()
    #Hence insteand of append a list of values by loops, we can put loop inside the max()
    max_mag = max(get_magnitude(e) for e in data['features'])
    max_loc = [get_location(e) for e in data['features'] if get_magnitude(e) == max_mag]
    return max_mag, max_loc



# With all the above functions defined, we can now call them and get the result
data = get_data()
print(get_magnitude(data['features'][1]))
print(f"Loaded {count_earthquakes(data)}")
max_magnitude, max_location = get_maximum(data)
print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")
