# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
import requests
import json

from datetime import date

import matplotlib.pyplot as plt
import numpy as np


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

    earthquakes = json.loads(text)
    with open("earthquakes.json", "w") as file:
        file.write(json.dumps(earthquakes))

    return earthquakes

    # We need to interpret the text to get values that we can work with.
    # What format is the text in? How can we load the values?

## The strongest earthquake was at [[-2.15, 52.52], [-0.332, 53.403]] with magnitude 4.8


def count_earthquakes(data):
    """Get the total number of earthquakes in the response."""
    return len(data["features"])


def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    return earthquake["properties"]["mag"]


def get_location(earthquake):
    """Retrieve the latitude and longitude of an earthquake item."""
    # There are three coordinates, but we don't care about the third (altitude)
    return [earthquake['geometry']['coordinates'][0], earthquake['geometry']['coordinates'][1]]


def get_maximum(data):
    """Get the magnitude and location of the strongest earthquake in the data."""
    max_mag = max([get_magnitude(eq) for eq in data['features']])
    max_loc = [get_location(eq) for eq in data['features'] if get_magnitude(eq) == max_mag]
    return max_mag, max_loc


# With all the above functions defined, we can now call them and get the result
data = get_data()
print(f"Loaded {count_earthquakes(data)}")
max_magnitude, max_location = get_maximum(data)
print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")

##The strongest earthquake was at [[-2.15, 52.52], [-0.332, 53.403]] with magnitude 4.8


def get_year(earthquake):
    """Extract the year in which an earthquake happened."""
    timestamp = earthquake['properties']['time']
    # The time is given in a strange-looking but commonly-used format.
    # To understand it, we can look at the documentation of the source data:
    # https://earthquake.usgs.gov/data/comcat/index.php#time
    # Fortunately, Python provides a way of interpreting this timestamp:
    # (Question for discussion: Why do we divide by 1000?)
    year = date.fromtimestamp(timestamp/1000).year
    return year




# This is function you may want to create to break down the computations,
# although it is not necessary. You may also change it to something different.
def get_magnitudes_per_year(earthquakes):
    """Retrieve the magnitudes of all the earthquakes in a given year.
    
    Returns a dictionary with years as keys, and lists of magnitudes as values.
    """
    #hi = []
    # return {  get_year(i):  hi.append(get_magnitude(i)) for i in earthquakes }
    years = [get_year(i) for i in earthquakes]
    magnitudes = [get_magnitude(i) for i in earthquakes]
    output = {}
    for i in range(len(years)):
        if years[i] not in output.keys():
            output[years[i]] = [magnitudes[i]]
        else:
            output[years[i]] += [magnitudes[i]]
    
    
    return output



def plot_average_magnitude_per_year(earthquakes):
    magntiudes_per_year = get_magnitudes_per_year(earthquakes)
    x = magntiudes_per_year.keys()
    y = [np.average(magntiudes_per_year[i]) for i in x]
    plt.figure()
    plt.plot(x,y)
    plt.show()
    


def plot_number_per_year(earthquakes):
    ...



# Get the data we will work with
quakes = get_data()['features']
# Plot the results - this is not perfect since the x axis is shown as real
# numbers rather than integers, which is what we would prefer!
# plot_number_per_year(quakes)
# plt.clf()  # This clears the figure, so that we don't overlay the two plots
# plot_average_magnitude_per_year(quakes)

print(plot_average_magnitude_per_year(quakes))