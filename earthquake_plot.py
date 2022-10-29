from datetime import date
import requests
import matplotlib.pyplot as plt
import json
import numpy as np

def get_data():
    """Retrieve the data we will be working with."""
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


def get_magnitude(quakes, earthquake):
    """Retrive the magnitude of an earthquake item."""
    return quakes[earthquake]['properties']['mag']


# This is function you may want to create to break down the computations,
# although it is not necessary. You may also change it to something different.
def get_magnitudes_per_year(earthquakes):
    """Retrieve the magnitudes of all the earthquakes in a given year.
    
    Returns a dictionary with years as keys, and lists of magnitudes as values.
    """
    total = len(earthquakes)
    mag_per_year_dict = {}
    
    for i in range(total):
        year = get_year(earthquakes[i])
        mag = get_magnitude(earthquakes, i)
        if year not in mag_per_year_dict:
            mag_per_year_dict[year] = [mag]
        else:
            mag_per_year_dict[year].append(mag)
    return mag_per_year_dict             


def plot_average_magnitude_per_year(earthquakes):
    data = get_magnitudes_per_year(earthquakes)
    x_data = list(data.keys())
    y_data = [np.array(data[year]).mean() for year in x_data]
    plt.plot(x_data, y_data)    
    plt.title("Average Magnitude Per Year")
    plt.xlabel("Year")
    plt.ylabel("Average Magnitude of Earthquakes")
    plt.savefig("Average Magnitude Per Year.png")
    plt.show()


def plot_number_per_year(earthquakes):
    data = get_magnitudes_per_year(earthquakes)
    x_data = list(data.keys())
    y_data = [len(data[year]) for year in x_data]
    plt.plot(x_data, y_data)    
    plt.title("Earthquake Number Per Year")
    plt.xlabel('Year')
    plt.ylabel('Number of Earthquakes')
    plt.savefig("Earthquake Number Per Year.png")
    plt.show() 


data = get_data()
quakes = get_data()['features']

# Plot the results - this is not perfect since the x axis is shown as real
# numbers rather than integers, which is what we would prefer!
plot_number_per_year(quakes)
plt.clf()    # This clears the figure, so that we don't overlay the two plots
plot_average_magnitude_per_year(quakes)