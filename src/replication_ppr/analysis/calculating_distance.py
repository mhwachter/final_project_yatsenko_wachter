from math import atan2, cos, radians, sin, sqrt

# Define the latitude and longitude coordinates of the countries in a dictionary
country_coordinates = {
    "Colombia": ("4 00 N", "72 00 W"),
    "Comoros": ("12 10 S", "44 15 E"),
    "Congo, Democratic Republic of the": ("0 00 N", "25 00 E"),
    "Congo, Republic of the": ("1 00 S", "15 00 E"),
}

# Define a function to convert coordinates from "4 00 N, 72 00 W" to "4, -72"
def convert_coordinates(coord_str):
    degrees, minutes, direction = coord_str.split()
    decimal_degrees = int(degrees) + float(minutes) / 60
    if direction in ["S", "W"]:
        decimal_degrees *= -1
    return decimal_degrees


# Define a function to calculate the distance between two points in km


def distance(coord1, coord2):
    # convert decimal degrees to radians
    lat1, lon1 = map(radians, coord1)
    lat2, lon2 = map(radians, coord2)

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return 6371 * c


# Loop over each pair of countries and calculate the distance between them
for _country1, coords1 in country_coordinates.items():
    lat1, lon1 = (convert_coordinates(c) for c in coords1)
    for _country2, coords2 in country_coordinates.items():
        lat2, lon2 = (convert_coordinates(c) for c in coords2)
        dist = distance((lat1, lon1), (lat2, lon2))
