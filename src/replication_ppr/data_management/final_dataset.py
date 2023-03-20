import pandas as pd

dot = pd.read_csv("../../../bld/python/data/dot_final.csv")
cia_dist = pd.read_csv("../../../bld/python/data/cia_distance.csv")
rta = pd.read_csv("../../../bld/python/data/rta_final.csv")


cia_dist = cia_dist.assign(
    pair_id=list(map(frozenset, zip(cia_dist.ISO3_x, cia_dist.ISO3_y))),
)

comb = pd.merge(dot, rta, how="left", on="pair_year_id")
comb = pd.merge(comb, cia_dist, how="left", left_on="pair_id_x", right_on="pair_id_x")


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
