"""Functions to merge final dataset."""
import numpy as np
import pandas as pd


def do_merge(dot, rta, dist, wb_reg_inc, cia_fact):
    """Merges final dataset.

    Args:
        dot (pd.DataFrame) : Direction of trade dataset.
        rta (pd.DataFrame) : Regional Trade agreements dataset.
        dist (pd.DataFrame) : Distance between countries dataset.
        wb_reg_inc (pd.DataFrame): World Bank income classification dataset.
        cia_fact (pd.DataFrame): CIA fact-book dataset.

    Returns:
        data (pd.DataFrame):Returns merged dataset.

    """
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

    data_final = pd.merge(
        data_final,
        dist,
        on="pair_id",
        how="left",
        suffixes=("", "_y"),
    )
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
    return data_final


def calc_additional_vars(data):
    """Creates additional dummy variables.

    Args:
      data (pd.DataFrame) :uses final dataset.

    Returns:
        data (pd.DataFrame):Returns merged dataset.

    """
    data["cty1_str"] = data["cty1"].apply(str)
    data["cty2_str"] = data["cty2"].apply(str)
    dummies = data[["cty1_str", "cty2_str"]].stack().str.get_dummies().sum(level=0)
    dummies = dummies.add_prefix("cd_")
    data = data.join(dummies)
    data["lareap"] = np.log(data["area_1"] * data["area_2"])
    data["comlang"] = 0
    data.loc[data["language_1"] == data["language_2"], "comlang"] = 1
    data["island"] = data["island_1"] + data["island_2"]
    data["landl"] = data["landlocked_1"] + data["landlocked_2"]
    data["border"] = 0
    data.loc[
        data["ctry1_ISO3"].isin(data["border_countries_2"]),
        "border",
    ] = 1
    return data


def add_original_variables(data, original_data):
    """Merges self-sourced dataset with cut version of dataset used in original paper.

    Args:
        data(pd.DataFrame):self-sourced dataset.
        original_data (pd.DataFrame): dataset used by a paper author.

    Returns:
        data (pd.DataFrame):Returns merged final dataset.

    """
    data = pd.merge(
        data,
        original_data[
            [
                "lrgdp",
                "lrgdppc",
                "comcol",
                "curcol",
                "colony",
                "comctry",
                "custrict",
                "regional",
                "bothin",
                "onein",
                "gsp",
                "pair_year_id_ISO3",
                "cty1",
                "cty2",
                "pairid",
                "found1",
                "found2",
                "minyrs",
                "maxyrs",
                "sasia1",
                "sasia2",
                "easia1",
                "easia2",
                "ssafr1",
                "ssafr2",
                "menaf1",
                "menaf2",
                "latca1",
                "latca2",
                "highi1",
                "highi2",
                "midin1",
                "midin2",
                "lowin1",
                "lowin2",
                "least1",
                "least2",
                "cty1_UNregion",
                "cty2_UNregion",
                "cty1_ISO3",
                "cty2_ISO3",
            ]
        ],
        left_on="pair_year_id",
        right_on="pair_year_id_ISO3",
        how="left",
    )
    data = data.dropna()
    return data


def rename_columns(data):
    """Renames a column.

    Args:
        data (pd.DataFrame):final dataset.

    Returns:
        data (pd.DataFrame):returns final dataset with renamed column.

    """
    data = data.rename(columns={"Year": "year"})
    return data
