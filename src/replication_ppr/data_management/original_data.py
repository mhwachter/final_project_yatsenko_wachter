import country_converter as coco

cc = coco.CountryConverter()


def extend_original_data(data):
    data["cty1_str"] = data["cty1"].apply(str)
    data["cty2_str"] = data["cty2"].apply(str)

    dummies = data[["cty1_str", "cty2_str"]].stack().str.get_dummies().sum(level=0)
    dummies = dummies.add_prefix("cd_")
    data = data.join(dummies)

    data.loc[data["cty1name"] == "KYRQYZ REPUBLIC", "cty1name"] = "KYRGYZSTAN"
    data.loc[data["cty2name"] == "KYRQYZ REPUBLIC", "cty2name"] = "KYRGYZSTAN"
    data.loc[data["cty1name"] == "MOLDVA", "cty1name"] = "MOLDOVA"
    data.loc[data["cty2name"] == "MOLDVA", "cty2name"] = "MOLDOVA"
    data.loc[
        data["cty1name"] == "YUGOSLAVIA, SOCIALIST FED. REP. OF",
        "cty1name",
    ] = "YUGOSLAVIA"
    data.loc[
        data["cty2name"] == "YUGOSLAVIA, SOCIALIST FED. REP. OF",
        "cty2name",
    ] = "YUGOSLAVIA"

    data["cty1_ISO3"] = cc.pandas_convert(series=data["cty1name"], to="ISO3")
    data["cty2_ISO3"] = cc.pandas_convert(series=data["cty2name"], to="ISO3")
    data["cty1_cont"] = cc.pandas_convert(series=data["cty1name"], to="continent")
    data["cty2_cont"] = cc.pandas_convert(series=data["cty2name"], to="continent")
    data["cty1_UNregion"] = cc.pandas_convert(series=data["cty1name"], to="UNregion")
    data["cty2_UNregion"] = cc.pandas_convert(series=data["cty2name"], to="UNregion")

    data["pair_id_ISO3"] = data[["cty1_ISO3", "cty2_ISO3"]].values.tolist()
    data["pair_id_ISO3"] = data["pair_id_ISO3"].apply(sorted).str.join("")

    data["pair_year_id_ISO3"] = data["pair_id_ISO3"] + data["year"].map(str)

    data = data.set_index(["pairid", "year"], drop=False)
    return data
