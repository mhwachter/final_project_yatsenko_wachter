import numpy as np
import pandas as pd


def do_merge(dot, rta, dist, wb_reg_inc, cia_fact):
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
            ]
        ],
        left_on="pair_year_id",
        right_on="pair_year_id_ISO3",
        how="left",
    )
    return data
