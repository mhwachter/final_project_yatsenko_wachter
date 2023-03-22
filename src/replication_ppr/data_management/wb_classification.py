import country_converter as coco
import pandas as pd

cc = coco.CountryConverter()


wb_reg_data = pd.read_csv(
    "../data/data-XHzgJ.csv",
)

least_developed = pd.read_csv("../data/least_developed.csv")

wb_reg_data["Country"] = cc.pandas_convert(
    series=wb_reg_data["Country"],
    to="name_short",
)

wb_reg_data["ISO3"] = cc.pandas_convert(series=wb_reg_data["Country"], to="ISO3")

least_developed["country"] = cc.pandas_convert(
    series=least_developed["country"],
    to="name_short",
)

least_developed["ISO3"] = cc.pandas_convert(
    series=least_developed["country"],
    to="ISO3",
)


wb_reg_data = wb_reg_data[["Country", "ISO3", "Income group", "Region"]]

region_dummies = pd.get_dummies(wb_reg_data["Region"])

income_dummies = pd.get_dummies(wb_reg_data["Income group"])

wb_reg_data["least"] = 0
wb_reg_data.loc[wb_reg_data["Country"].isin(least_developed["country"]), "least"] = 1

wb_reg_data = pd.concat([wb_reg_data, region_dummies, income_dummies], axis=1)

wb_reg_data.reset_index()

wb_reg_data.to_csv("../../../bld/python/data/wb_reg_inc.csv", index=False)

#     merged,
#     wb_reg_data,

#     Data_region_dis_1,
#     wb_reg_data,
