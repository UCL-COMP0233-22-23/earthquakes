from datetime import date
import matplotlib.pyplot as plt
import requests
import json
import numpy as np

def get_data():
    """Retrieve the data we will be working with."""
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
    text = response.text
    out = json.loads(text)
    return out

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


def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    return earthquake['properties']['mag']


# This is function you may want to create to break down the computations,
# although it is not necessary. You may also change it to something different.
def get_magnitudes_per_year(earthquakes):
    """Retrieve the magnitudes of all the earthquakes in a given year.
    
    Returns a dictionary with years as keys, and lists of magnitudes as values.
    """
    output = {}
    for earthquake in earthquakes:
        year = get_year(earthquake)
        magnitude = get_magnitude(earthquake)
        try:
            output[year].append(magnitude)
        except:
            output[year] = [magnitude]
    return output

def plot_average_magnitude_per_year(earthquakes):
    magnitudes_per_year = get_magnitudes_per_year(earthquakes)
    x = magnitudes_per_year.keys()
    y = [np.average(i) for i in magnitudes_per_year.values()]
    fig = plt.subplots(figsize = (12, 6))
    plt.xticks(np.arange(np.min(list(x)), np.max(list(x))+1, 1.0))
    plt.plot(x, y)


def plot_number_per_year(earthquakes):
    magnitudes_per_year = get_magnitudes_per_year(earthquakes)
    x = magnitudes_per_year.keys()
    y = [len(i) for i in magnitudes_per_year.values()]
    fig = plt.subplots(figsize = (12, 6))
    plt.xticks(np.arange(np.min(list(x)), np.max(list(x))+1, 1.0))
    plt.yticks(np.arange(0, np.max(list(y))+1, 2.0))
    plt.plot(x, y)


# Get the data we will work with
quakes = get_data()['features']

# Plot the results - this is not perfect since the x axis is shown as real
# numbers rather than integers, which is what we would prefer!
plot_number_per_year(quakes)
plt.clf()  # This clears the figure, so that we don't overlay the two plots
plot_average_magnitude_per_year(quakes)