import numpy as np
import pandas as pd

dot = pd.read_csv("../data/DOT_03-08-2023 16-25-54-79_panel.csv")

dot.columns

dot = dot[
    [
        "Country Name",
        "Country Code",
        "Counterpart Country Name",
        "Counterpart Country Code",
        "Time Period",
        "Goods, Value of Exports, Free on board (FOB), US Dollars (TXG_FOB_USD)",
        "Goods, Value of Imports, Cost, Insurance, Freight (CIF), US Dollars (TMG_CIF_USD)",
    ]
]

cpi = pd.read_csv("../data/cpi_urban_consumers.csv")

cpi_annual = cpi.groupby(["Year"]).mean()

dot = pd.merge(dot, cpi_annual, how="left", left_on="Time Period", right_on="Year")

dot = dot.rename(
    columns={
        "Goods, Value of Exports, Free on board (FOB), US Dollars (TXG_FOB_USD)": "FOB Exports",
        "Goods, Value of Imports, Cost, Insurance, Freight (CIF), US Dollars (TMG_CIF_USD)": "CIF Imports",
        "Value": "CPI",
        "Time Period": "Year",
        "Country Name": "Country",
        "Counterpart Country Name": "Counterpart Country",
    },
)

dot["pair_id"] = (
    dot.groupby(
        dot[["Country", "Counterpart Country"]].apply(frozenset, axis=1),
    ).ngroup()
    + 1
)

g = dot.groupby(["pair_id", "Year"]).cumcount().add(1)
dot = (
    dot.set_index(["pair_id", "Year", g])
    .unstack(fill_value=0)
    .sort_index(axis=1, level=1)
)
dot.columns = [f"{a}{b}" for a, b in dot.columns]

dot = dot[""]

dot["c1_id"] = dot.groupby("Country Name").ngroup() + 1
dot["c2_id"] = dot.groupby("Counterpart Country Name").ngroup() + 1

m = dot["c1_id"].lt(dot["c2_id"])

names = {
    "c1_id": "c2_id",
    "c2_id": "c1_id",
    "Country Name": "Counterpart Country Name",
    "Counterpart Country Name": "Country Name",
    "FOB Exports": "FOB Exports 2",
    "CIF Imports": "CIF Imports 2",
}

out = dot[m].merge(dot[~m].rename(columns=names), how="outer")

dot["pair_id"] = (
    dot.groupby(
        dot[["Country Name", "Counterpart Country Name"]].apply(frozenset, axis=1),
    ).ngroup()
    + 1
)


dot["id"] = dot.groupby(["pair_id", "Time Period"]).ngroup()

out_df = dot.set_index(["id", dot.groupby("id").cumcount()]).unstack()
out_df.columns = [f"{a}{b}" for a, b in out_df.columns]


dot["grp"] = dot.groupby(["Country Name", "Counterpart Country Name"]).ngroup()

dot["subgrp"] = dot.groupby(["pair_id", "grp"]).ngroup()

dot = dot.set_index(["pair_id", "subgrp"])

dot.pivot_table(
    index=["pair_id", "Time Period"],
)

dot["direction"] = (
    dot.groupby(["Country Name", "Counterpart Country Name"]).ngroup() + 1
)

dot = dot.set_index(["pair_id", "direction"])

dot = dot.set_index(["pair_id", "Time Period"])


dot["subgroup"] = dot.groupby(["pair_id", "direction_id"]).ngroup()

dot.groupby["pair_id", "direction_id"]

dot.to_csv("/Users/marcel/Desktop/dot.csv")

dot_wide = pd.pivot(
    dot,
    index=["pair_id", "Time Period"],
    columns=["Country Name", "Counterpart Country Name"],
    values=["FOB Exports", "CIF Imports"],
)

dot["countries"] = dot[["Country Name", "Counterpart Country Name"]].values.tolist()

dot["combinedid"] = dot["Country Name"] + dot["Counterpart Country Name"]

if (
    dot["Country Name"] in dot["countries"]
    and dot["Counterpart Country Name"] in dot["countries"]
):
    dot["pair_id"] = np.unique()

pd.DataFrame(np.sort(dot.values, 1), index=dot.index).groupby([0, 1]).ngroup()
