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

#     "../data/cia_factbook.csv",


def get_coordinates(data):
    data["Latitude"] = data["country"].apply(
        lambda x: get_lat_long(x)[0] if get_lat_long(x) is not None else None,
    )
    data["Longitude"] = data["country"].apply(
        lambda x: get_lat_long(x)[1] if get_lat_long(x) is not None else None,
    )
    return data


def calculate_distance(data):
    distances = []
    pair_id = 1
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            if (
                data["Latitude"][i] is not None
                and data["Longitude"][i] is not None
                and data["Latitude"][j] is not None
                and data["Longitude"][j] is not None
            ):
                dist_km = distance(
                    (data["Latitude"][i], data["Longitude"][i]),
                    (data["Latitude"][j], data["Longitude"][j]),
                ).km
                d_miles = dist_km * 0.621371  # Convert km to miles
                ldist_km = np.log(dist_km)
                ldist = np.log(d_miles)  # Take the logarithmic form
                pair_code = pair_id
                pair_id += 1
                distances.append(
                    (
                        data["country"][i],
                        data["country"][j],
                        pair_code,
                        dist_km,
                        d_miles,
                        ldist_km,
                        ldist,
                    ),
                )
    return distances


def create_distance_data(data):
    distance_df = pd.DataFrame(
        data,
        columns=[
            "Country 1",
            "Country 2",
            "Pair ID",
            "Distance (km)",
            "Distance (miles)",
            "Log Distance (km)",
            "ldist",
        ],
    )
    return distance_df


def distance_data_cleaning(data):
    data = data.rename(columns={"Country 1": "ctry1", "Country 2": "ctry2"})

    data["ctry1_ISO3"] = cc.pandas_convert(series=data["ctry1"], to="ISO3")
    data["ctry2_ISO3"] = cc.pandas_convert(series=data["ctry2"], to="ISO3")

    data["pair_id"] = data[["ctry1_ISO3", "ctry2_ISO3"]].values.tolist()
    data["pair_id"] = data["pair_id"].apply(sorted).str.join("")

    data = data.drop("Pair ID", axis=1)
    data = data[
        [
            "pair_id",
            "ctry1",
            "ctry2",
            "ctry1_ISO3",
            "ctry2_ISO3",
            "Distance (km)",
            "Distance (miles)",
            "Log Distance (km)",
            "ldist",
        ]
    ]

    data = data.reset_index()
    return data
