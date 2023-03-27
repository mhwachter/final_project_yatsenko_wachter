import country_converter as coco
import pandas as pd

df = pd.read_csv("../data/original_data_paper.csv")
cc = coco.CountryConverter()

df["cty1_str"] = df["cty1"].apply(str)
df["cty2_str"] = df["cty2"].apply(str)

dummies = df[["cty1_str", "cty2_str"]].stack().str.get_dummies().sum(level=0)
dummies = dummies.add_prefix("cd_")
cty = list(dummies.columns.values)
df = df.join(dummies)

df.loc[df["cty1name"] == "KYRQYZ REPUBLIC", "cty1name"] = "KYRGYZSTAN"
df.loc[df["cty2name"] == "KYRQYZ REPUBLIC", "cty2name"] = "KYRGYZSTAN"
df.loc[df["cty1name"] == "MOLDVA", "cty1name"] = "MOLDOVA"
df.loc[df["cty2name"] == "MOLDVA", "cty2name"] = "MOLDOVA"
df.loc[
    df["cty1name"] == "YUGOSLAVIA, SOCIALIST FED. REP. OF",
    "cty1name",
] = "YUGOSLAVIA"
df.loc[
    df["cty2name"] == "YUGOSLAVIA, SOCIALIST FED. REP. OF",
    "cty2name",
] = "YUGOSLAVIA"

df["cty1_ISO3"] = cc.pandas_convert(series=df["cty1name"], to="ISO3")
df["cty2_ISO3"] = cc.pandas_convert(series=df["cty2name"], to="ISO3")
df["cty1_cont"] = cc.pandas_convert(series=df["cty1name"], to="continent")
df["cty2_cont"] = cc.pandas_convert(series=df["cty2name"], to="continent")
df["cty1_UNregion"] = cc.pandas_convert(series=df["cty1name"], to="UNregion")
df["cty2_UNregion"] = cc.pandas_convert(series=df["cty2name"], to="UNregion")

df = df.set_index(["pairid", "year"], drop=False)

df.to_csv("../../../bld/python/data/original_extended.csv")
