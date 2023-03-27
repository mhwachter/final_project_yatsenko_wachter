import pandas as pd

df = pd.read_csv("../data/original_data_paper.csv")

df["cty1_str"] = df["cty1"].apply(str)
df["cty2_str"] = df["cty2"].apply(str)

dummies = df[["cty1_str", "cty2_str"]].stack().str.get_dummies().sum(level=0)
dummies = dummies.add_prefix("cd_")
cty = list(dummies.columns.values)
df = df.join(dummies)

df = df.set_index(["pairid", "year"], drop=False)

df.to_csv("../../../bld/python/data/original_extended.csv")
