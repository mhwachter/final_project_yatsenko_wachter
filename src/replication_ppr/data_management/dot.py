import country_converter as coco
import numpy as np
import pandas as pd

cc = coco.CountryConverter()

dot = pd.read_csv("../data/DOT.csv")

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
        "Country Name": "ctry1",
        "Counterpart Country Name": "ctry2",
        "Country Code": "ctry1_code",
        "Counterpart Country Code": "ctry2_code",
    },
)


dot["pair_id"] = (
    dot.groupby(
        dot[["ctry1_code", "ctry2_code"]].apply(frozenset, axis=1),
    ).ngroup()
    + 1
)

dot = dot.groupby(["pair_id", "Year"]).agg(
    {
        "ctry1": "last",
        "ctry1_code": "last",
        "ctry2": "last",
        "ctry2_code": "last",
        "Year": "last",
        "FOB Exports": "mean",
        "CIF Imports": "mean",
        "CPI": "last",
        "pair_id": "last",
    },
)

dot = dot.drop_duplicates(["pair_id", "Year"])

dot["trade"] = (dot.loc[:, ["FOB Exports", "CIF Imports"]].mean(axis=1)) / dot["CPI"]

dot["ltrade"] = np.log(dot["trade"])

dot = dot[dot["trade"].notna()]

dot = dot[["pair_id", "Year", "ctry1", "ctry2", "trade", "ltrade"]]

dot["ctry1_ISO3"] = cc.pandas_convert(series=dot["ctry1"], to="ISO3")
dot["ctry2_ISO3"] = cc.pandas_convert(series=dot["ctry2"], to="ISO3")

countries_list = pd.read_csv("../data/countries_list.csv")
countries_list = countries_list.drop(175)
iso3 = countries_list["ISO3"].to_list()

dot = dot[dot["ctry1_ISO3"].isin(iso3)]
dot = dot[dot["ctry2_ISO3"].isin(iso3)]

dot["ctry1"] = cc.pandas_convert(series=dot["ctry1"], to="name_short")
dot["ctry2"] = cc.pandas_convert(series=dot["ctry2"], to="name_short")
