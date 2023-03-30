"""Function creates,cleans and modifies RTA dataset."""
import zipfile

import country_converter as coco

cc = coco.CountryConverter()


def unzip_rta_data(zip, unzip):
    with zipfile.ZipFile(zip, "r") as zip_ref:
        zip_ref.extractall(unzip)


def create_rta_final(data, countries_list):
    iso3 = countries_list["ISO3"].to_list()
    data = data.rename(
        columns={"exporter": "ctry1", "importer": "ctry2", "year": "Year"},
    )

    data["ctry1"] = cc.pandas_convert(series=data["ctry1"], to="name_short")
    data["ctry2"] = cc.pandas_convert(series=data["ctry2"], to="name_short")

    data["ctry1_ISO3"] = cc.pandas_convert(series=data["ctry1"], to="ISO3")
    data["ctry2_ISO3"] = cc.pandas_convert(series=data["ctry2"], to="ISO3")

    data = data[data["ctry1_ISO3"].isin(iso3)]
    data = data[data["ctry2_ISO3"].isin(iso3)]

    data["pair_id"] = data[["ctry1_ISO3", "ctry2_ISO3"]].values.tolist()
    data["pair_id"] = data["pair_id"].apply(sorted).str.join("")

    data["pair_year_id"] = data["pair_id"] + data["Year"].map(str)

    data = data.drop(data[data.ctry1 == data.ctry2].index)
    data = data.drop_duplicates("pair_year_id")

    data["cer"] = 0
    data.loc[data["cerg"] == 1, "cer"] = 1
    data.loc[data["cers"] == 1, "cer"] = 1

    data = data[
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

    data = data.reset_index(drop=True)
    return data
