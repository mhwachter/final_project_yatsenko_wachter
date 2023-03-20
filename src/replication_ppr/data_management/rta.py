import zipfile

import country_converter as coco
import pandas as pd

cc = coco.CountryConverter()

with zipfile.ZipFile("../data/rta.zip", "r") as zip_ref:
    zip_ref.extractall("../data")

rta = pd.read_csv("../data/rta.csv")

countries_list = pd.read_csv("../data/countries_list.csv")
iso3 = countries_list["ISO3"].to_list()

rta["exporter"] = cc.pandas_convert(series=rta["exporter"], to="ISO3")
rta["importer"] = cc.pandas_convert(series=rta["importer"], to="ISO3")

rta = rta[rta["exporter"].isin(iso3)]
rta = rta[rta["importer"].isin(iso3)]

rta = rta.assign(pair_id=list(map(frozenset, zip(rta.exporter, rta.importer))))

rta = rta.assign(
    pair_year_id=list(map(frozenset, zip(rta.exporter, rta.importer, rta.year))),
)

rta = rta.drop(rta[rta.exporter == rta.importer].index)
rta = rta.drop_duplicates("pair_year_id")

rta = rta.reset_index(drop=True)

rta.to_csv("../../../bld/python/data/rta_final.csv")
