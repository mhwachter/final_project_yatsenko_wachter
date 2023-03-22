import numpy as np
import pandas as pd

dot = pd.read_csv("../../../bld/python/data/dot_final.csv")

rta = pd.read_csv("../../../bld/python/data/rta_final.csv")

dist = pd.read_csv("../../../bld/python/data/distance_final.csv")

wb_reg_inc = pd.read_csv("../../../bld/python/data/wb_reg_inc.csv")

cia_fact = pd.read_csv("../../../bld/python/data/cia_factbook.csv")


data_final = pd.merge(dot, rta, how="left", on="pair_year_id", suffixes=("", "_y"))
data_final = data_final.drop(data_final.filter(regex="_y$").columns, axis=1)

data_final = pd.merge(
    data_final,
    wb_reg_inc,
    left_on="ctry1_ISO3",
    right_on="ISO3",
    how="left",
)
data_final = pd.merge(
    data_final,
    wb_reg_inc,
    left_on="ctry2_ISO3",
    right_on="ISO3",
    how="left",
    suffixes=("_1", "_2"),
)

data_final = pd.merge(data_final, dist, on="pair_id", how="left", suffixes=("", "_y"))
data_final = data_final.drop(data_final.filter(regex="_y$").columns, axis=1)

data_final = data_final.drop(
    columns=["ISO3_1", "ISO3_2", "Country_1", "Country_2", "index"],
)

data_final = pd.merge(
    data_final,
    cia_fact,
    left_on="ctry1_ISO3",
    right_on="ISO3",
    how="left",
)
data_final = pd.merge(
    data_final,
    cia_fact,
    left_on="ctry2_ISO3",
    right_on="ISO3",
    how="left",
    suffixes=("_1", "_2"),
)

data_final = data_final.drop(columns=["ISO3_1", "ISO3_2", "country_1", "country_2"])

# Calculations
data_final["larea"] = np.log(data_final["area_1"] * data_final["area_2"])
data_final["comlang"] = 0
data_final.loc[data_final["language_1"] == data_final["language_2"], "comlang"] = 1
data_final["island"] = data_final["island_1"] + data_final["island_2"]
data_final["landlocked"] = data_final["landlocked_1"] + data_final["landlocked_2"]
data_final["border"] = 0
data_final.loc[
    data_final["ctry1_ISO3"].isin(data_final["border_countries_2"]),
    "border",
] = 1
