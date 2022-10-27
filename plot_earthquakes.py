from datetime import date
import json
import matplotlib.pyplot as plt
from numpy import average
import requests
from sympy import rotations


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
    res = {}
    for eq in earthquakes:
        if str(get_year(eq)) not in res:
            
            res[str(get_year(eq))] = [get_magnitude(eq)]
        res[str(get_year(eq))].append(get_magnitude(eq))
    return res


def plot_average_magnitude_per_year(earthquakes):
    res = get_magnitudes_per_year(earthquakes)
    # years = []
    # num = []
    # for k,v in res.items():
    #     years.append(k[2:])
    #     num.append(average(v))
    years = res.keys()
    num = [average(i) for i in res.values()]
    plt.xticks(rotation=90)    
    plt.plot(years,num,'bo')
    plt.title('Plot: average magnitude')



def plot_number_per_year(earthquakes):
    res = get_magnitudes_per_year(earthquakes)
    # years = []
    # num = []
    # # print(type(res))
    # for k,v in res.items():
    #     years.append(k[2:])
    #     num.append(len(v))
    years = res.keys()
    num = [len(i) for i in res.values()]
    plt.xticks(rotation=90)
    plt.plot(years,num, 'ro')
    plt.title('Plot: number per year')

    # ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))




# Get the data we will work with
quakes = get_data()['features']
r = get_magnitudes_per_year(quakes)
# Plot the results - this is not perfect since the x axis is shown as real
# numbers rather than integers, which is what we would prefer!
# plot_average_magnitude_per_year(quakes)
plt.subplot(1, 2, 1)
plot_number_per_year(quakes)
# plt.clf()  # This clears the figure, so that we don't overlay the two plots
plt.subplot(1, 2, 2)
plot_average_magnitude_per_year(quakes)
plt.show()