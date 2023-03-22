import numpy as np
import pandas as pd

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
    ],
)

merged["larea"] = np.log(merged["Country 1 area"] * merged["Country 2 area"])
merged = merged.assign(pair_id=list(map(frozenset, zip(merged.ISO3_x, merged.ISO3_y))))
merged.to_csv("../../../bld/python/data/cia_distance.csv")
