import pandas as pd

dot = pd.read_csv("../../../bld/python/data/dot_final.csv")
cia_dist = pd.read_csv("../../../bld/python/data/cia_distance.csv")

comb = pd.merge(
    dot,
    cia_dist,
    how="left",
    left_on=["ctry1_ISO3", "ctry2_ISO3"],
    right_on=["ISO3_x", "ISO3_y"],
)

dot = dot.assign(ref=list(map(frozenset, zip(dot.ctry1_ISO3, dot.ctry2_ISO3))))
cia_dist = cia_dist.assign(
    ref=list(map(frozenset, zip(cia_dist.ISO3_x, cia_dist.ISO3_y))),
)

comb = pd.merge(dot, cia_dist, on="ref")

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
