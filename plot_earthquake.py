from datetime import date
import requests
import json
import matplotlib.pyplot as plt
from statistics import mean
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

def get_year(earthquake, int):
    """Extract the year in which an earthquake happened."""
    timestamp = earthquake[int]['properties']['time']
    # The time is given in a strange-looking but commonly-used format.
    # To understand it, we can look at the documentation of the source data:
    # https://earthquake.usgs.gov/data/comcat/index.php#time
    # Fortunately, Python provides a way of interpreting this timestamp:
    # (Question for discussion: Why do we divide by 1000?)
    #The fromtimestamp() function is used to return the date corresponding to a specified timestamp.
    #timestamp in milliseconds, but fronttimestamp expect it in second.divided by 1000
    year = date.fromtimestamp(timestamp/1000).year
    return year

def get_magnitude(earthquake, int):
    """Retrive the magnitude of an earthquake item."""
    return earthquake[int]["properties"]["mag"]
#print(data['features'][3]['properties']['mag'])
#need to notice, feature is the key of dictionary
#the earthquake here stand for list


# This is function you may want to create to break down the computations,
# although it is not necessary. You may also change it to something different.
def get_magnitudes_per_year(earthquakes):
    """Retrieve the magnitudes of all the earthquakes in a given year.
    Returns a dictionary with years as keys, and lists of magnitudes as values.
    """
    count = len(earthquakes)
    mag_per_y = {}
    for i in range(count): 
        mag = get_magnitude(earthquakes,i)
        year = get_year(earthquakes,i)
        if year in mag_per_y:
            mag_per_y[year] += [mag]
        else:
            mag_per_y[year] = [mag]
    return mag_per_y
data = get_data()


def plot_average_magnitude_per_year(earthquakes):
    mag_year = get_magnitudes_per_year(earthquakes)
    year = []
    mag = []
    for key, value in mag_year.items():
        year += [key]
        mag += [mean(value)]
    plt.plot(year, mag)    
    plt.title("Averaged magnitude per year")
    plt.xlabel("Years")
    plt.ylabel("Averaged magnitude")
    plt.savefig("Averaged magnitude per year.png")
    plt.show()

plot_average_magnitude_per_year(data['features'])
'''
def plot_number_per_year(earthquakes):
    ...



# Get the data we will work with
quakes = get_data()['features']

# Plot the results - this is not perfect since the x axis is shown as real
# numbers rather than integers, which is what we would prefer!
plot_number_per_year(quakes)
plt.clf()  # This clears the figure, so that we don't overlay the two plots
plot_average_magnitude_per_year(quakes)
'''