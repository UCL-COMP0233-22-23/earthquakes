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
            "orderby": "time-asc"})
    text = response.text
    earthquakes = json.loads(text)
    return earthquakes


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
    mags_per_year = {}
    for quake in earthquakes:
        if str(get_year(quake)) not in mags_per_year.keys():
            mags_per_year[str(get_year(quake))] = []
        mags_per_year[str(get_year(quake))].append(get_magnitude(quake))
    return mags_per_year


def plot_average_magnitude_per_year(earthquakes):
    mags_per_year = get_magnitudes_per_year(earthquakes)
    years = []
    avg_mags = []
    for year in mags_per_year.keys():
        years.append(int(year))
        avg_mags.append(np.mean(mags_per_year[year]))
    plt.figure()
    plt.plot(years, avg_mags)
    plt.title('Average earthquake magnitude per year')
    plt.ylabel('Average magnitude')
    plt.xlabel('Year')
<<<<<<< HEAD
=======
    plt.xticks(np.arange(np.min(list(years)), np.max(list(years))+1, 1.0), rotation=45)
>>>>>>> plots-pkruzikova-jtcl24
    plt.show()

def plot_number_per_year(earthquakes):
    mags_per_year = get_magnitudes_per_year(earthquakes)
    years = []
    no = []
    for year in mags_per_year.keys():
        years.append(int(year))
        no.append(len(mags_per_year[year]))
    plt.figure()
    plt.plot(years, no)
    plt.title('Number of earthquakes per year')
    plt.ylabel('Earthquakes')
    plt.xlabel('Year')
<<<<<<< HEAD
=======
    plt.xticks(np.arange(np.min(list(years)), np.max(list(years))+1, 1.0), rotation=45)
>>>>>>> plots-pkruzikova-jtcl24
    plt.show()


# Get the data we will work with
quakes = get_data()['features']

# Plot the results - this is not perfect since the x axis is shown as real
# numbers rather than integers, which is what we would prefer!
plot_number_per_year(quakes)
#plt.clf()  # This clears the figure, so that we don't overlay the two plots
plot_average_magnitude_per_year(quakes)