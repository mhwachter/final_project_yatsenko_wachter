"""Function to create Direction of Trade dataset."""
import country_converter as coco
import numpy as np
import pandas as pd

cc = coco.CountryConverter()


def create_dot_final(data, cpi, countries_list):
    """Creates a final data frame containing trade data, CPI data, and country ISO
    codes.

    Args:
        data (pd.DataFrame): A dataset containing raw trade data.
        cpi (pd.DataFrame): A dataset containing CPI data.
        countries_list (pd.DataFrame): A dataset containing country ISO codes.

    Returns:
        data (pd.DataFrame): A cleaned and merged dataset containing trade data, CPI data, and country ISO codes.

    """
    data = data[
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

    cpi_annual = cpi.groupby(["Year"]).mean()

    data = pd.merge(
        data,
        cpi_annual,
        how="left",
        left_on="Time Period",
        right_on="Year",
    )

    data = data.rename(
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

    data["pair"] = (
        data.groupby(
            data[["ctry1_code", "ctry2_code"]].apply(frozenset, axis=1),
        ).ngroup()
        + 1
    )

    data = data.groupby(["pair", "Year"]).agg(
        {
            "ctry1": "last",
            "ctry1_code": "last",
            "ctry2": "last",
            "ctry2_code": "last",
            "Year": "last",
            "FOB Exports": "mean",
            "CIF Imports": "mean",
            "CPI": "last",
            "pair": "last",
        },
    )

    data = data.drop_duplicates(["pair", "Year"])

    data["trade"] = (data.loc[:, ["FOB Exports", "CIF Imports"]].mean(axis=1)) / data[
        "CPI"
    ]

    data["ltrade"] = np.log(data["trade"])

    data = data[data["trade"].notna()]

    data = data[["pair", "Year", "ctry1", "ctry2", "trade", "ltrade"]]

    data["ctry1_ISO3"] = cc.pandas_convert(series=data["ctry1"], to="ISO3")
    data["ctry2_ISO3"] = cc.pandas_convert(series=data["ctry2"], to="ISO3")

    iso3 = countries_list["ISO3"].to_list()

    data = data[data["ctry1_ISO3"].isin(iso3)]
    data = data[data["ctry2_ISO3"].isin(iso3)]

    data["ctry1"] = cc.pandas_convert(series=data["ctry1"], to="name_short")
    data["ctry2"] = cc.pandas_convert(series=data["ctry2"], to="name_short")

    data["countries"] = data[["ctry1", "ctry2"]].values.tolist()
    data["countries"] = data["countries"].sort_values().apply(lambda x: sorted(x))

    data["ctry1"] = data["countries"].str[0]
    data["ctry2"] = data["countries"].str[1]

    data.columns = data.columns.str.strip()

    data["pair_id"] = data[["ctry1_ISO3", "ctry2_ISO3"]].values.tolist()
    data["pair_id"] = data["pair_id"].apply(sorted).str.join("")

    data["pair_year_id"] = data["pair_id"] + data["Year"].map(str)

    data = data[
        [
            "pair_id",
            "pair_year_id",
            "Year",
            "ctry1",
            "ctry2",
            "ctry1_ISO3",
            "ctry2_ISO3",
            "trade",
            "ltrade",
        ]
    ]

    data = data.reset_index(drop=True)
    return data
