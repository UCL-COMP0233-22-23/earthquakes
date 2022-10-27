# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
import datetime
import requests
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
    import json
    data = json.loads(text)
    with open("earthquakes.json", "w") as f:
        f.write(json.dumps(data))

    # We need to interpret the text to get values that we can work with.
    # What format is the text in? How can we load the values?
    return data["features"]

def get_year(data):
    timestamp = data["properties"]["time"]
    year = datetime.date.fromtimestamp(timestamp / 1000).year
    return year

def count_earthquakes(data):
    """Get the total number of earthquakes in the response."""
    return len(data)


def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    return earthquake["properties"]["mag"]


def get_location(earthquake):
    """Retrieve the latitude and longitude of an earthquake item."""
    # There are three coordinates, but we don't care about the third (altitude)
    return earthquake["geometry"]["coordinates"][:2]


def get_maximum(data):
    """Get the magnitude and location of the strongest earthquake in the data."""
    strongest = max(data, key=lambda x: get_magnitude(x))
    return get_magnitude(strongest), get_location(strongest)


# With all the above functions defined, we can now call them and get the result
data = get_data()
print(f"Loaded {count_earthquakes(data)}")
max_magnitude, max_location = get_maximum(data)
print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")



def number_of_earthquakes_per_year(data):
    earthquakes_per_year = {}
    for earthquake in data:
        year = get_year(earthquake)
        if year in earthquakes_per_year:
            earthquakes_per_year[year] += 1
        else:
            earthquakes_per_year[year] = 1
    return earthquakes_per_year

print(number_of_earthquakes_per_year(data))

def average_magitude_per_year(data):
    earthquakes_per_year = {}
    for earthquake in data:
        year = get_year(earthquake)
        if year in earthquakes_per_year:
            earthquakes_per_year[year].append(get_magnitude(earthquake))
        else:
            earthquakes_per_year[year] = [get_magnitude(earthquake)]
    return {year: sum(magnitudes) / len(magnitudes) for year, magnitudes in earthquakes_per_year.items()}

print(average_magitude_per_year(data))

def plot_earthquakes_per_year(data):
    earthquakes_per_year = number_of_earthquakes_per_year(data)
    years = sorted(earthquakes_per_year.keys())
    plt.plot(years, [earthquakes_per_year[year] for year in years])
    plt.show()
plot_earthquakes_per_year(data)

def plot_average_magnitude_per_year(data):
    average_magnitude_per_year = average_magitude_per_year(data)
    years = sorted(average_magnitude_per_year.keys())
    plt.plot(years, [average_magnitude_per_year[year] for year in years])
    plt.show()
plot_average_magnitude_per_year(data)