import pandas as pd
from geopy.distance import distance
from geopy.geocoders import Nominatim

# create geocoder object
geolocator = Nominatim(user_agent="my-app")

# define function to get latitude and longitude values for a country
def get_lat_long(country):
    location = geolocator.geocode(country)
    if location is not None:
        return (location.latitude, location.longitude)
    else:
        return None


# create dataframe
df = pd.DataFrame(
    {
        "Country": ["Angola", "Algeria"],
        "Coordinates": ["12 30 S, 18 30 E", "28 00 N, 3 00 E"],
    },
)

# create new columns for latitude and longitude
df["Latitude"] = df["Country"].apply(
    lambda x: get_lat_long(x)[0] if get_lat_long(x) is not None else None,
)
df["Longitude"] = df["Country"].apply(
    lambda x: get_lat_long(x)[1] if get_lat_long(x) is not None else None,
)

# calculate distance between each pair of countries
distances = []
for i in range(len(df)):
    for j in range(i + 1, len(df)):
        if (
            df["Latitude"][i] is not None
            and df["Longitude"][i] is not None
            and df["Latitude"][j] is not None
            and df["Longitude"][j] is not None
        ):
            d = distance(
                (df["Latitude"][i], df["Longitude"][i]),
                (df["Latitude"][j], df["Longitude"][j]),
            ).km
            distances.append((df["Country"][i], df["Country"][j], d))

# create new dataframe with distance values
distance_df = pd.DataFrame(
    distances, columns=["Country 1", "Country 2", "Distance (km)"],
)

# print out dataframe
