from datetime import date
import requests
import json
import matplotlib.pyplot as plt


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
    with open("text_data.json", 'w') as out:
        out.write(text)


    
    # We need to interpret the text to get values that we can work with.
    # What format is the text in? How can we load the values?
    print(type(json.loads(text)))
    #print(json.loads(text))
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
    
    magnitudes = [get_magnitude(quake) for quake in earthquakes]
    years = [int(get_year(quake)) for quake in earthquakes]
    
    result = {}
    
    for y, m in zip(years, magnitudes):
        if y in result:
            result[y].append(m)
        else:
            result[y] = [m]
            
    return result

def plot_average_magnitude_per_year(earthquakes):
    
    avg_mag_per_year = get_magnitudes_per_year(earthquakes)
    # Average years
    for keys in avg_mag_per_year:
        value = avg_mag_per_year[keys]
        avg_mag_per_year[keys] = sum(value)/len(value)

    plt.bar(avg_mag_per_year.keys(), avg_mag_per_year.values())

        
    tick_idx = list(range(
        min(avg_mag_per_year.keys()),
        max(avg_mag_per_year.keys())+1
    ))
    
    # Add an entry of 0 in the case that no earthquake occurs
    for idx in tick_idx:
        if idx not in avg_mag_per_year.keys():
            avg_mag_per_year[idx] = 0
    
    plt.xticks(tick_idx, list(avg_mag_per_year.keys()).sort(), rotation=90)
    plt.xlabel('Year')
    plt.ylabel('Average magnitude per year')
    plt.savefig('Average_Plot.jpeg')
    plt.show()
    


def plot_number_per_year(earthquakes):
    no_per_year = get_magnitudes_per_year(earthquakes)
    # Extract no. quakes per year
    for keys in no_per_year:
        value = no_per_year[keys]
        no_per_year[keys] = len(value)

    plt.bar(no_per_year.keys(), no_per_year.values())
    
    tick_idx = list(range(
        min(no_per_year.keys()),
        max(no_per_year.keys())+1
    ))
    
    # Add an entry of 0 in the case that no earthquake occurs
    for idx in tick_idx:
        if idx not in no_per_year.keys():
            no_per_year[idx] = 0
    
    plt.xticks(tick_idx, list(no_per_year.keys()).sort(), rotation=90)

    plt.xlabel('Year')
    plt.ylabel('Number of earthquakes')
    plt.grid()
    plt.savefig('Average_year_Plot.jpeg')
    plt.show()

# Get the data we will work with
quakes = get_data()['features']
get_magnitudes_per_year(quakes)
# Plot the results - this is not perfect since the x axis is shown as real
# numbers rather than integers, which is what we would prefer!
plot_number_per_year(quakes)
plt.clf()  # This clears the figure, so that we don't overlay the two plots
plot_average_magnitude_per_year(quakes)
