import country_converter as coco
import numpy as np
import pandas as pd
from geopy.distance import distance
from geopy.geocoders import Nominatim

cc = coco.CountryConverter()

# create geocoder object
geolocator = Nominatim(user_agent="my-app")

# define function to get latitude and longitude values for a country
def get_lat_long(country):
    location = geolocator.geocode(country, timeout=None)
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
            ldist_km = np.log(dist_km)
            ldist = np.log(d_miles)  # Take the logarithmic form
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
        "Log Distance (km)",
        "Log Distance (miles)",
    ],
)

distance_df = distance_df.rename(columns={"Country 1": "ctry1", "Country 2": "ctry2"})

distance_df["ctry1_ISO3"] = cc.pandas_convert(series=distance_df["ctry1"], to="ISO3")
distance_df["ctry2_ISO3"] = cc.pandas_convert(series=distance_df["ctry2"], to="ISO3")

distance_df["pair_id"] = distance_df[["ctry1_ISO3", "ctry2_ISO3"]].values.tolist()
distance_df["pair_id"] = distance_df["pair_id"].apply(sorted).str.join("")

distance_df = distance_df.drop("Pair ID", axis=1)
distance_df = distance_df[
    [
        "pair_id",
        "ctry1",
        "ctry2",
        "ctry1_ISO3",
        "ctry2_ISO3",
        "Distance (km)",
        "Distance (miles)",
        "Log Distance (km)",
        "Log Distance (miles)",
    ]
]

distance_df = distance_df.reset_index()

distance_df.to_csv("../../../bld/python/data/distance_final.csv", index=False)
