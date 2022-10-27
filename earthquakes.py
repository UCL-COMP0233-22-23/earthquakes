# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
import requests
import json
from datetime import date
from statistics import mean
import matplotlib.pyplot as plt

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
    # To understand the structure of this text, you may want to save it
    # to a file and open it in VS Code or a browser.
    # See the README file for more information.

    # We need to interpret the text to get values that we can work with.
    # What format is the text in? How can we load the values?
    return json.loads(text)

def count_earthquakes(data):
    """Get the total number of earthquakes in the response."""
    return data["metadata"]["count"]


def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    return earthquake["properties"]["mag"]


def get_location(earthquake):
    """Retrieve the latitude and longitude of an earthquake item."""
    # There are three coordinates, but we don't care about the third (altitude)
    coordinates = earthquake["geometry"]["coordinates"]

    return (coordinates[0], coordinates[1])


def get_maximum(data):
    """Get the magnitude and location of the strongest earthquake in the data."""
    current_max_magnitude = get_magnitude(data["features"][0])
    current_max_location = get_location(data["features"][0])
    for item in data["features"]:
        magnitude = get_magnitude(item)
        # Note: what happens if there are two earthquakes with the same magnitude?
        if magnitude > current_max_magnitude:
            current_max_magnitude = magnitude
            current_max_location = get_location(item)
    return current_max_magnitude, current_max_location


# With all the above functions defined, we can now call them and get the result
data = get_data()
print(f"Loaded {count_earthquakes(data)}")
max_magnitude, max_location = get_maximum(data)
print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")

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

def get_magnitudes_per_year(earthquakes):
    quake_dict = {}
    for quake in earthquakes:
        year = get_year(quake)
        if str(year) in quake_dict:
            quake_dict[str(year)].append(get_magnitude(quake))
        else:
            quake_dict[str(year)] = [get_magnitude(quake)]

    return quake_dict
      
def plot_average_magnitude_per_year(earthquakes):
    quakes_by_year = get_magnitudes_per_year(earthquakes)
    avg_quakes_year = {year: mean(quakes_by_year[year]) for year in quakes_by_year}
    
    fig1, ax = plt.subplots()
    ax.plot(list(avg_quakes_year.keys()), list(avg_quakes_year.values()))
    ax.set_title("Average magnitude per year")
    ax.set_xlabel("Year")
    ax.set_ylabel("Average Richter Magnitude ")
    plt.xticks(rotation=45)
    

def plot_number_per_year(earthquakes):
    quakes_by_year = get_magnitudes_per_year(earthquakes)
    num_quakes_year = {year: len(quakes_by_year[year]) for year in quakes_by_year}
    
    fig2, ax = plt.subplots()
    ax.plot(list(num_quakes_year.keys()), list(num_quakes_year.values()))
    ax.set_title("Number of earthquakes per year")
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of earthquakes")
    plt.xticks(rotation=45)
    

plot_average_magnitude_per_year(data["features"])

plot_number_per_year(data["features"])
plt.show()
