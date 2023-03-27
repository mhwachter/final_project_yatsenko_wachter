import zipfile

import country_converter as coco
import pandas as pd

cc = coco.CountryConverter()

with zipfile.ZipFile("../data/rta.csv.zip", "r") as zip_ref:
    zip_ref.extractall("../data")

rta = pd.read_csv("../data/rta.csv")

countries_list = pd.read_csv("../data/countries_list.csv")
iso3 = countries_list["ISO3"].to_list()

rta = rta.rename(columns={"exporter": "ctry1", "importer": "ctry2", "year": "Year"})

rta["ctry1"] = cc.pandas_convert(series=rta["ctry1"], to="name_short")
rta["ctry2"] = cc.pandas_convert(series=rta["ctry2"], to="name_short")

rta["ctry1_ISO3"] = cc.pandas_convert(series=rta["ctry1"], to="ISO3")
rta["ctry2_ISO3"] = cc.pandas_convert(series=rta["ctry2"], to="ISO3")

rta = rta[rta["ctry1_ISO3"].isin(iso3)]
rta = rta[rta["ctry2_ISO3"].isin(iso3)]


rta["pair_id"] = rta[["ctry1_ISO3", "ctry2_ISO3"]].values.tolist()
rta["pair_id"] = rta["pair_id"].apply(sorted).str.join("")

rta["pair_year_id"] = rta["pair_id"] + rta["Year"].map(str)

rta = rta.drop(rta[rta.ctry1 == rta.ctry2].index)
rta = rta.drop_duplicates("pair_year_id")

rta["cer"] = 0
rta.loc[rta["cerg"] == 1, "cer"] = 1
rta.loc[rta["cers"] == 1, "cer"] = 1

rta = rta[
    [
        "pair_id",
        "pair_year_id",
        "Year",
        "ctry1",
        "ctry2",
        "ctry1_ISO3",
        "ctry2_ISO3",
        "rta",
        "eu",
        "cer",
        "patcra",
        "usaisr",
        "cacm",
        "caricomg",
        "mercosurg",
        "mercosurs",
        "sparteca",
        "eea",
        "nafta",
    ]
]

rta = rta.reset_index(drop=True)

rta.to_csv("../../../bld/python/data/rta_final.csv", index=False)
