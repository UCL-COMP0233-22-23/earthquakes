# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
import pandas as pd
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

    text = response.json()
    text =  text['features']
    
    final_dict = {}
    for i in range(len(text)):
        element = {}
        dictionary = text[i]
        element = {'id': dictionary['id']}
        element.update(dictionary['properties'])
        element.update(dictionary['geometry'])
        final_dict[i] = element
    
    df = pd.DataFrame.from_dict(final_dict).transpose()
    df = df.drop_duplicates(subset=['id'])
    df = df.drop(columns=['tz', 'url', 'detail', 'sources', 'types', "mmi","alert","status", "type", "title", 'ids'])
    df = df.set_index("id")
    df.mag = pd.to_numeric(df.mag)

    return df

class Earthquake:
    def __init__(self, id):
        self.time = df.loc[[id]]['time'].item()
        self.mag = df.loc[[id]]['mag'].item()
        self.place = df.loc[[id]]['place'].item()
        self.coordinates = df.loc[[id]]['coordinates'].item()

def count_earthquakes(data):
    count = len(data)
    return count

def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    return earthquake.mag

def get_location(earthquake):
    """Retrieve the latitude and longitude of an earthquake item."""
    # There are three coordinates, but we don't care about the third (altitude)
    return (earthquake.coordinates[0], earthquake.coordinates[1])

def get_maximum(data):
    """Get the magnitude and location of the strongest earthquake in the data."""
    index = data[['mag']].idxmax().item()
    earthquake = Earthquake(index)
    mag = get_magnitude(earthquake)
    loc = get_location(earthquake)
    return mag, loc

# With all the above functions defined, we can now call them and get the result
data = get_data()
print(f"Loaded {count_earthquakes(data)}")
max_magnitude, max_location = get_maximum(data)
print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")
