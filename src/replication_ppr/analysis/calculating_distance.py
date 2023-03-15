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

distance_data = pd.read_csv(
    "../data/cia_factbook.csv",
)


# create new columns for latitude and longitude

distance_data["Latitude"] = distance_data["country"].apply(
    lambda x: get_lat_long(x)[0] if get_lat_long(x) is not None else None,
)
distance_data["Longitude"] = distance_data["country"].apply(
    lambda x: get_lat_long(x)[1] if get_lat_long(x) is not None else None,
)

# calculate distance between each pair of countries
distances = []
pair_id = 1
for i in range(len(distance_data)):
    for j in range(i + 1, len(distance_data)):
        if (
            distance_data["Latitude"][i] is not None
            and distance_data["Longitude"][i] is not None
            and distance_data["Latitude"][j] is not None
            and distance_data["Longitude"][j] is not None
        ):
            d = distance(
                (distance_data["Latitude"][i], distance_data["Longitude"][i]),
                (distance_data["Latitude"][j], distance_data["Longitude"][j]),
            ).km
            pair_code = pair_id
            pair_id += 1
            distances.append(
                (
                    distance_data["country"][i],
                    distance_data["country"][j],
                    pair_code,
                    d,
                ),
            )

# create new dataframe with distance values
distance_df = pd.DataFrame(
    distances,
    columns=["Country 1", "Country 2", "Pair ID", "Distance (km)"],
)
# print out dataframe
