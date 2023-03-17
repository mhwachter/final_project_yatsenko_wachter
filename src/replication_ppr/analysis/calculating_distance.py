import numpy as np
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
            dist_km = distance(
                (distance_data["Latitude"][i], distance_data["Longitude"][i]),
                (distance_data["Latitude"][j], distance_data["Longitude"][j]),
            ).km
            d_miles = dist_km * 0.621371  # Convert km to miles
            ldist_km = np.log2(dist_km)
            ldist = np.log2(d_miles)  # Take the logarithmic form
            pair_code = pair_id
            pair_id += 1
            distances.append(
                (
                    distance_data["country"][i],
                    distance_data["country"][j],
                    pair_code,
                    dist_km,
                    d_miles,
                    ldist_km,
                    ldist,
                ),
            )

# create new dataframe with distance values
distance_df = pd.DataFrame(
    distances,
    columns=[
        "Country 1",
        "Country 2",
        "Pair ID",
        "Distance (km)",
        "Distance (miles)",
        "Log Distance Km",
        "Log Distance Miles",
    ],
)
# print out dataframe
distance_df
# merginf dataset.
CIA_data = pd.read_csv(
    "../data/cia_factbook.csv",
)
CIA_data = pd.DataFrame(CIA_data)

merged = pd.merge(
    distance_df,
    CIA_data,
    left_on="Country 1",
    right_on="country",
    how="left",
)
merged = pd.merge(merged, CIA_data, left_on="Country 2", right_on="country", how="left")
merged = merged.rename(columns={"area_y": "Country 2 area", "area_x": "Country 1 area"})
#
merged = merged.drop(
    columns=[
        "country_x",
        "coordinates_x",
        "landlocked_x",
        "language_x",
        "island_x",
        "country_y",
        "coordinates_y",
        "landlocked_y",
        "language_y",
        "island_y",
        "Unnamed: 0_x",
        "Unnamed: 0_y",
    ],
)

merged["larea"] = np.log2(merged["Country 1 area"] * merged["Country 2 area"])
