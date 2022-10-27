from datetime import date
import requests
import json
import matplotlib.pyplot as plt
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
    return json.loads(text)


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
    magnitudes_per_year = {}
    for earthquake in earthquakes:
            eq_year = int(get_year(earthquake))
            eq_mag = get_magnitude(earthquake)
            if (eq_year in magnitudes_per_year):
                magnitudes_per_year[eq_year].append(eq_mag)
            else:
                magnitudes_per_year[eq_year] = [eq_mag]
    return magnitudes_per_year


def plot_average_magnitude_per_year(earthquakes):
    magnitudes_per_year = get_magnitudes_per_year(earthquakes)
    aver_magnitudes_per_year = {}
    for year in magnitudes_per_year:
        mags = np.array(magnitudes_per_year[year])
        keep_indices = np.where(mags != None)[0]
        aver_magnitudes_per_year[year] = np.mean(mags[keep_indices])
    x = list(aver_magnitudes_per_year.keys())
    y = list(aver_magnitudes_per_year.values())
    plt.plot(x, y)
    plt.show()


def plot_number_per_year(earthquakes):
    magnitudes_per_year = get_magnitudes_per_year(earthquakes)
    freq_per_year = {}
    for year in magnitudes_per_year:
        freq_per_year[year] = len(magnitudes_per_year[year])
    x = list(freq_per_year.keys())
    y = list(freq_per_year.values())
    plt.plot(x, y)
    plt.show()


# Get the data we will work with
#magnitudes_per_year = {}
quakes = get_data()['features']

# Plot the results - this is not perfect since the x axis is shown as real
# numbers rather than integers, which is what we would prefer!
plot_number_per_year(quakes)
plt.clf()  # This clears the figure, so that we don't overlay the two plots
plot_average_magnitude_per_year(quakes)