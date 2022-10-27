# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
import requests
import os
import json


def get_data(dest_path):
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
    with open(os.path.join(dest_path,'response.json'), 'w') as f:
        f.write(str(text) + '\n')   

    # We need to interpret the text to get values that we can work with.
    # What format is the text in? How can we load the values?
    return json.loads(text)

### EDA

path = os.getcwd()
data = get_data(dest_path = path)



def count_earthquakes(data):
    """Get the total number of earthquakes in the response."""
    eq_count = data["metadata"]["count"]
    return eq_count

count_earthquakes(data)


def get_magnitude(earthquake, data):
    """
    Retrive the magnitude of an earthquake item. 
    Retrieves a specific earthquake by ID given all the data.
    """
    all_eq = [earthquake for earthquake in data["features"]]
    all_id = [entry["id"] for entry in all_eq]
    ind = all_id.index(earthquake)
    magnitude = all_eq[ind]["properties"]["mag"]


    return magnitude

get_magnitude("usp000bf1x", data)

def get_location(earthquake, data):
    """
    Retrieve the latitude and longitude of an earthquake item.
    Retrieves a specific earthquake by ID given all the data.
    Returns longtitude, latitude.
    """
    # There are three coordinates, but we don't care about the third (altitude)
    all_eq = [earthquake for earthquake in data["features"]]
    all_id = [entry["id"] for entry in all_eq]
    ind = all_id.index(earthquake)
    (longtitude, latitude) = all_eq[ind]["geometry"]["coordinates"][:2]
    return longtitude, latitude

get_location("usp000bf1x", data)

## additional helper function bc i defined my functions poorly 
def get_eq_id_by_ind(ind, data):
    return data["features"][ind]["id"]

get_eq_id_by_ind(19, data)


def get_maximum(data):
    """Get the magnitude and location of the strongest earthquake in the data."""
    # all magnitudes
    all_mags = [entry["properties"]["mag"] for entry in data["features"]]
    max_mag = max(all_mags)
    ind = all_mags.index(max_mag)
    id = get_eq_id_by_ind(ind, data)
    loc = get_location(id, data)
    
    return max_mag, loc

get_maximum(data)


# With all the above functions defined, we can now call them and get the result
data = get_data(dest_path = os.path.join(path, "earthquakes"))
print(f"Loaded {count_earthquakes(data)}")
max_magnitude, max_location = get_maximum(data)
print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")

# Loaded 120
# The strongest earthquake was at (-2.15, 52.52) with magnitude 4.8


#### plotting the earthquakes ####

from datetime import date

import matplotlib.pyplot as plt


def get_data():
    """Retrieve the data we will be working with."""
    ...


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

get_year(data["features"][0])

all_years = [get_year(earthquake) for earthquake in data["features"]]

unique_years = list(set(all_years))

unique_years = sorted(unique_years)

count = 0
for earthquake in data["features"]:
    if get_year(earthquake) == 2017:
        count += 1
    
print(count)

frequency ={}
for i in unique_years:
    count = 0
    for j in all_years:
        if j == i:
            count += 1
    frequency[i] = count
    print(i, count)

print(frequency)

import matplotlib.pyplot as plt

plt.plot(frequency.keys(), frequency.values(), "o")
plt.show()




#num_earthquakes = {}
#num_earthquakes['year1'] = 
2000: 1, 2001: 3
# {year1: count1, year2: count2,...}
#[{'year': x, 'count': y},...]


def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    ...


# This is function you may want to create to break down the computations,
# although it is not necessary. You may also change it to something different.
def get_magnitudes_per_year(earthquakes):
    """Retrieve the magnitudes of all the earthquakes in a given year.
    
    Returns a dictionary with years as keys, and lists of magnitudes as values.
    """
    ...


def plot_average_magnitude_per_year(earthquakes):
    ...


def plot_number_per_year(earthquakes):
    ...



# Get the data we will work with
quakes = get_data()['features']

# Plot the results - this is not perfect since the x axis is shown as real
# numbers rather than integers, which is what we would prefer!
plot_number_per_year(quakes)
plt.clf()  # This clears the figure, so that we don't overlay the two plots
plot_average_magnitude_per_year(quakes)