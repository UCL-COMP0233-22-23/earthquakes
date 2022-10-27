from datetime import date

import matplotlib.pyplot as plt
import json
import requests

def get_data():
    """Retrieve the data we will be working with."""
        # With requests, we can ask the web service for the data.
    # Can you understand the parameters we are passing here?
    with open('earthquakes_file.json') as inputfile:
        earthquakes_data = json.load(inputfile)
    return earthquakes_data


def get_year(earthquake):
    """Extract the year in which an earthquake happened."""
    timestamp = earthquake['properties']['time']
    # The time is given in a strange-looking but commonly-used format.
    # To understand it, we can look at the documentation of the source data:
    # https://earthquake.usgs.gov/data/comcat/index.php#time
    # Fortunately, Python provides a way of interpreting this timestamp:
    # (Question for discussion: Why do we divide by 1000?)
    year = date.fromtimestamp(timestamp/1000).year #split time into miliseconds
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
    legend = {}
    for eq in earthquakes:
        year = get_year(eq)
        if year in legend.keys():
            legend[year].append(get_magnitude(eq))
        else:
            legend[year] = [get_magnitude(eq)]
    return legend
            


def plot_average_magnitude_per_year(earthquakes):
    #quakes_year = get_magnitudes_per_year(earthquakes)
    #keys = quakes_year.keys()
    #mag_per_year = [sum([mag for mag in quakes_year[year] for year in keys])]
    #return plt.plot([mag_per_year for year in keys])
    return ...


def plot_number_per_year(earthquakes):
    quakes_year = get_magnitudes_per_year(earthquakes)
    keys = quakes_year.keys()
    plt.plot([len(quakes_year[i]) for i in keys])
    plt.show() #to show the plot!!! 

# Get the data we will work with
quakes = get_data()['features']

# Plot the results - this is not perfect since the x axis is shown as real
# numbers rather than integers, which is what we would prefer!
plot_number_per_year(quakes)
#plt.clf()  # This clears the figure, so that we don't overlay the two plots
#plot_average_magnitude_per_year(quakes)