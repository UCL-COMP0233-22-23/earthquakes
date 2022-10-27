# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
import requests


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
    ...
    import json
    with open('earthquakes_data.json', 'w') as f:
        f.write(text)   # On Mac Shift + Option + F to format automatically
    
    with open('earthquakes_data.json', 'r') as f:
        text_json = json.loads(f.read())    # return dict 

    # print(type(text_json))

    # We need to interpret the text to get values that we can work with.
    # What format is the text in? How can we load the values?
    return text_json

def count_earthquakes(data):
    """Get the total number of earthquakes in the response."""

    return len(data['features'])


def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""

    mag = []
    for eq in earthquake:
        mag.append(float(eq['properties']['mag']))
    return mag


def get_location(earthquake):
    """Retrieve the latitude and longitude of an earthquake item."""
    # There are three coordinates, but we don't care about the third (altitude)

    loc = []
    for eq in earthquake:
        loc.append((eq['geometry']['coordinates'][0], eq['geometry']['coordinates'][1]))

    return loc


def get_maximum(data):
    """Get the magnitude and location of the strongest earthquake in the data."""

    mag_max = max([float(eq['properties']['mag']) for eq in data['features']])
    mag_max_eq = [eq for eq in data['features'] if eq['properties']['mag'] == mag_max]
    print(mag_max)
    print(type(mag_max_eq))
    return get_magnitude(mag_max_eq), get_location(mag_max_eq)


# With all the above functions defined, we can now call them and get the result
data = get_data()
print(f"Loaded {count_earthquakes(data)}")
max_magnitude, max_location = get_maximum(data)
print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}") # The strongest earthquake was at [(-2.15, 52.52), (-0.332, 53.403)] with magnitude [4.8, 4.8]