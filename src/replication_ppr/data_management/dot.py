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

dot["countries"] = dot[["Country", "Counterpart Country"]].values.tolist()

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

dot["trade"] = (
    dot.loc[:, ["FOB Exports1", "FOB Exports2", "CIF Imports1", "CIF Imports2"]].mean(
        axis=1,
    )
    / dot["CPI1"]
)

dot["ltrade"] = np.log(dot["trade"])

dot = dot[dot["trade"].notna()]

dot = dot.reset_index()

dot = dot[["pair_id", "Year", "countries1", "trade", "ltrade"]]

dot["ctry1"] = dot["countries1"].str[0]
dot["ctry2"] = dot["countries1"].str[1]

dot = dot[["pair_id", "Year", "ctry1", "ctry2", "trade", "ltrade"]]

dot.to_csv("/Users/marcel/Desktop/dot.csv")
