from datetime import date

import matplotlib.pyplot as plt
import numpy as np

import pandas as pd
import datetime
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

    text = response.json()
    text =  text['features']
    
    final_dict = {}
    for i in range(len(text)):
        element = {}
        dictionary = text[i]
        element = {'id': dictionary['id']}
# .update() is an inplace function
        element.update(dictionary['properties'])
        element.update(dictionary['geometry'])
        final_dict[i] = element
    
    
    df = pd.DataFrame.from_dict(final_dict).transpose()
    
    df = df.drop(columns=['tz', 'url', 'detail', 'sources', 'types', "mmi","alert","status", "type", "title", 'ids'])
    
    df = df.set_index("id")
    df.mag = pd.to_numeric(df.mag)
    df.time = pd.to_numeric(df.time)
    
    df.time = df.time.apply(lambda x: datetime.datetime.fromtimestamp(x/1000.0))

    return df

class Earthquake:
    def __init__(self, id):
        self.time = df.loc[[id]]['time'].item()
        self.mag = df.loc[[id]]['mag'].item()
        self.place = df.loc[[id]]['place'].item()
        self.coordinates = df.loc[[id]]['coordinates'].item()

def get_year(earthquake):
    """Extract the year in which an earthquake happened."""
    year = earthquake.time.year
    return year


def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    return earthquake.mag


def get_magnitudes_per_year(df):
    """Retrieve the magnitudes of all the earthquakes in a given year.
    
    Returns a dictionary with years as keys, and lists of magnitudes as values.
    """
    result = {}

    for id in df.index.tolist():
        result[df.loc[[id]]['time'].item().year] = []

    for id in df.index.tolist():
        year = df.loc[[id]]['time'].item().year
        mag = df.loc[[id]]['mag'].item()
        result[year].append(mag)

    return result


def plot_average_magnitude_per_year(data):
    
    d = get_magnitudes_per_year(data)

    # make data:
    x = [key for key in d.keys()]
    
    y = [sum(d[key])/len(d[key]) for key in d.keys()]

    # plot
    fig, ax = plt.subplots()

    ax.bar(x, y, width=1, edgecolor="black", linewidth=1)
    ax.set_title('average_magnitude_per_year')

    return plt.show()


def plot_number_per_year(data):
    d = get_magnitudes_per_year(data)

    # make data:
    x = [key for key in d.keys()]
    
    y = [len(d[key]) for key in d.keys()]

    # plot
    fig, ax = plt.subplots()

    ax.bar(x, y, edgecolor="black")
    ax.set_title('number_per_year')

    return plt.show()


# # Get the data we will work with
quakes = get_data()

# # Plot the results - this is not perfect since the x axis is shown as real
# # numbers rather than integers, which is what we would prefer!
plot_number_per_year(quakes)
plt.clf()  # This clears the figure, so that we don't overlay the two plots
plot_average_magnitude_per_year(quakes)
