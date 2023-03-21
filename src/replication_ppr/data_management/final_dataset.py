import pandas as pd

dot = pd.read_csv("../../../bld/python/data/dot_final.csv")


cia_dist = pd.read_csv("../../../bld/python/data/cia_distance.csv")

rta = pd.read_csv("../../../bld/python/data/rta_final.csv")

comb = pd.merge(dot, rta, how="left", on="pair_year_id", suffixes=("", "_y"))
comb = comb.drop(comb.filter(regex="_y$").columns, axis=1)

comb = pd.merge(
    comb,
    cia_dist,
    how="left",
    left_on="pair_id",
    right_on="pair_id",
    suffixes=("", "_y"),
)
comb = comb.drop(comb.filter(regex="_y$").columns, axis=1)

comb = comb[
    [
        "pair_id",
        "Year",
        "ctry1",
        "ctry2",
        "ctry1_ISO3",
        "ctry2_ISO3",
        "ltrade",
        "Log Distance Miles",
        "larea",
    ]
]
