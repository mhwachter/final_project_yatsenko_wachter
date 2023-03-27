import pandas as pd
import statsmodels.api as sm
from linearmodels import PanelOLS, RandomEffects

df = pd.read_csv("../data/original_data_paper.csv")
df["cty1_str"] = df["cty1"].apply(str)
df["cty2_str"] = df["cty2"].apply(str)
dummies = df[["cty1_str", "cty2_str"]].stack().str.get_dummies().sum(level=0)
dummies = dummies.add_prefix("cd_")
cty = list(dummies.columns.values)
df = df.join(dummies)
df = df.set_index(["pairid", "year"], drop=False)

exog = [
    "ldist",
    "lrgdp",
    "lrgdppc",
    "comlang",
    "border",
    "landl",
    "island",
    "lareap",
    "comcol",
    "curcol",
    "colony",
    "comctry",
    "custrict",
    "regional",
    "bothin",
    "onein",
    "gsp",
]

exog_cty = exog + cty

df.to_csv("/Users/marcel/Desktop/df.csv")

# Table 1 (1)
tab1_1 = PanelOLS.from_formula(
    "ltrade ~ ldist + lrgdp + lrgdppc + comlang + border + landl + island + lareap + comcol + curcol + colony + comctry + custrict + regional + bothin + onein + gsp + TimeEffects",
    data=df,
)
tab1_1.fit(cov_type="clustered", cluster_entity=True)
# Table 1 (2)
tab1_2 = PanelOLS.from_formula(
    "ltrade ~ ldist + lrgdp + lrgdppc + comlang + border + landl + island + lareap + comcol + curcol + colony + comctry + custrict + regional + bothin + onein + gsp + TimeEffects)",
    data=df[(df["cty1"] >= 200) & (df["cty2"] >= 200)],
)
tab1_2.fit(cov_type="cluster", cov_kwds={"groups": df["pairid"]}).summary()
# Table 1 (3)
tab1_3 = PanelOLS.from_formula(
    "ltrade ~ ldist + lrgdp + lrgdppc + comlang + border + landl + island + lareap + comcol + curcol + colony + comctry + custrict + regional + bothin + onein + gsp + TimeEffects",
    df[(df["year"] > 1970)],
    check_rank=False,
    drop_absorbed=True,
)
tab1_3.fit(cov_type="clustered", cluster_entity=True)
# Table 1 (4)
tab1_4 = PanelOLS(
    dependent=df["ltrade"],
    exog=df[exog_cty],
    time_effects=True,
    check_rank=False,
    drop_absorbed=True,
)
tab1_4.fit(cov_type="clustered", cluster_entity=True)

# Table 2
for i in range(1950, 1996, 5):
    tab = sm.OLS.from_formula(
        "ltrade ~ ldist + lrgdp + lrgdppc + comlang + border + landl + island + lareap + comcol + curcol + colony + comctry + custrict + regional + bothin + onein + gsp",
        data=df[df["year"] == i],
    )

# Table 3 (1) + (2)
df["periods"] = pd.cut(
    df["year"],
    [1948, 1949, 1951, 1956, 1961, 1967, 1979, 1994, 2000],
    labels=[
        "Before Annecy round (1949)",
        "Annecy to Torquay round (1951)",
        "Torquay to Geneva round (1956)",
        "Geneva to Dillon round (1961)",
        "Dillon to Kennedy round (1967)",
        "Kennedy to Tokyo round (1979)",
        "Tokyo to Uruguay round (1994)",
        "After Uruguay round",
    ],
    right=False,
    include_lowest=True,
)

tab3_12 = PanelOLS.from_formula(
    "ltrade ~ ldist + lrgdp + lrgdppc + comlang + border + landl + island + lareap + comcol + curcol + colony + comctry + custrict + regional + bothin:periods + onein:periods + gsp + TimeEffects",
    df,
)
tab3_12.fit(cov_type="clustered", cluster_entity=True)

# Table 3 (3) + (4)
tab3_34 = PanelOLS.from_formula(
    "ltrade ~ ldist + lrgdp + lrgdppc + comlang + border + landl + island + lareap + comcol + curcol + colony + comctry + custrict + regional + bothin:periods + onein:periods + gsp + EntityEffects",
    df,
    drop_absorbed=True,
)
tab3_34.fit(cov_type="clustered", cluster_entity=True)

# Table 4 (1) + (2) + (3)
tab4_1 = PanelOLS.from_formula(
    "ltrade ~ ldist + lrgdp + lrgdppc + comlang + border + landl + island + lareap + comcol + curcol + colony + comctry + custrict + regional + bothin + onein + gsp + TimeEffects",
    df,
    check_rank=False,
    drop_absorbed=True,
)
tab4_1.fit(cov_type="clustered", cluster_entity=True).params[["bothin", "onein", "gsp"]]

tab4_2 = PanelOLS.from_formula(
    "ltrade ~ ldist + lrgdp + lrgdppc + comlang + border + landl + island + lareap + comcol + curcol + colony + comctry + custrict + regional + bothin + onein + gsp + TimeEffects",
    df[(df["sasia1"] == 1) | df["sasia2"] == 1],
    check_rank=False,
    drop_absorbed=True,
)
tab4_2.fit(cov_type="clustered", cluster_entity=True).params[["bothin", "onein", "gsp"]]

tab4_3 = PanelOLS.from_formula(
    "ltrade ~ ldist + lrgdp + lrgdppc + comlang + border + landl + island + lareap + comcol + curcol + colony + comctry + custrict + regional + bothin + onein + gsp + TimeEffects",
    df[(df["easia1"] == 1) | df["easia2"] == 1],
    check_rank=False,
    drop_absorbed=True,
)
tab4_3.fit(cov_type="clustered", cluster_entity=True).params[["bothin", "onein", "gsp"]]

tab4_4 = PanelOLS.from_formula(
    "ltrade ~ ldist + lrgdp + lrgdppc + comlang + border + landl + island + lareap + comcol + curcol + colony + comctry + custrict + regional + bothin + onein + gsp + TimeEffects",
    df[(df["ssafr1"] == 1) | df["ssafr2"] == 1],
    check_rank=False,
    drop_absorbed=True,
)
tab4_4.fit(cov_type="clustered", cluster_entity=True).params[["bothin", "onein", "gsp"]]

tab4_5 = PanelOLS.from_formula(
    "ltrade ~ ldist + lrgdp + lrgdppc + comlang + border + landl + island + lareap + comcol + curcol + colony + comctry + custrict + regional + bothin + onein + gsp + TimeEffects",
    df[(df["menaf1"] == 1) | df["menaf2"] == 1],
    check_rank=False,
    drop_absorbed=True,
)
tab4_5.fit(cov_type="clustered", cluster_entity=True).params[["bothin", "onein", "gsp"]]

tab4_6 = PanelOLS.from_formula(
    "ltrade ~ ldist + lrgdp + lrgdppc + comlang + border + landl + island + lareap + comcol + curcol + colony + comctry + custrict + regional + bothin + onein + gsp + TimeEffects",
    df[(df["latca1"] == 1) | df["latca2"] == 1],
    check_rank=False,
    drop_absorbed=True,
)
tab4_6.fit(cov_type="clustered", cluster_entity=True).params[["bothin", "onein", "gsp"]]

tab4_7 = PanelOLS.from_formula(
    "ltrade ~ ldist + lrgdp + lrgdppc + comlang + border + landl + island + lareap + comcol + curcol + colony + comctry + custrict + regional + bothin + onein + gsp + TimeEffects",
    df[(df["highi1"] == 1) | df["highi2"] == 1],
    check_rank=False,
    drop_absorbed=True,
)
tab4_7.fit(cov_type="clustered", cluster_entity=True).params[["bothin", "onein", "gsp"]]

tab4_8 = PanelOLS.from_formula(
    "ltrade ~ ldist + lrgdp + lrgdppc + comlang + border + landl + island + lareap + comcol + curcol + colony + comctry + custrict + regional + bothin + onein + gsp + TimeEffects",
    df[(df["midin1"] == 1) | df["midin2"] == 1],
    check_rank=False,
    drop_absorbed=True,
)
tab4_8.fit(cov_type="clustered", cluster_entity=True).params[["bothin", "onein", "gsp"]]

tab4_9 = PanelOLS.from_formula(
    "ltrade ~ ldist + lrgdp + lrgdppc + comlang + border + landl + island + lareap + comcol + curcol + colony + comctry + custrict + regional + bothin + onein + gsp + TimeEffects",
    df[(df["lowin1"] == 1) | df["lowin2"] == 1],
    check_rank=False,
    drop_absorbed=True,
)
tab4_9.fit(cov_type="clustered", cluster_entity=True).params[["bothin", "onein", "gsp"]]

tab4_10 = PanelOLS.from_formula(
    "ltrade ~ ldist + lrgdp + lrgdppc + comlang + border + landl + island + lareap + comcol + curcol + colony + comctry + custrict + regional + bothin + onein + gsp + TimeEffects",
    df[(df["least1"] == 1) | df["least2"] == 1],
    check_rank=False,
    drop_absorbed=True,
)
tab4_10.fit(cov_type="clustered", cluster_entity=True).params[
    ["bothin", "onein", "gsp"]
]

# Table 5
tab5_1 = PanelOLS.from_formula(
    "ltrade ~ ldist + lrgdp + lrgdppc + comlang + border + landl + island + lareap + comcol + curcol + colony + comctry + custrict + regional + bothin + onein + gsp + TimeEffects",
    df[df["year"] < 1980],
    check_rank=False,
    drop_absorbed=True,
)
tab5_1.fit(cov_type="clustered", cluster_entity=True).params[["bothin", "onein", "gsp"]]

tab5_2 = PanelOLS.from_formula(
    "ltrade ~ ldist + lrgdp + lrgdppc + comlang + border + landl + island + lareap + comcol + curcol + colony + comctry + custrict + regional + bothin + onein + gsp + TimeEffects",
    df[df["year"] > 1979],
    check_rank=False,
    drop_absorbed=True,
)
tab5_2.fit(cov_type="clustered", cluster_entity=True).params[["bothin", "onein", "gsp"]]

tab5_3 = PanelOLS.from_formula(
    "ltrade ~ ldist + lrgdp + lrgdppc + comlang + border + landl + island + lareap + comcol + curcol + colony + comctry + custrict + regional + bothin + onein + gsp + TimeEffects",
    df[(df["cty1"] < 200) & (df["cty2"] < 200)],
    check_rank=False,
    drop_absorbed=True,
)
tab5_3.fit(cov_type="clustered", cluster_entity=True).params[["bothin", "onein", "gsp"]]

tab5_4 = PanelOLS.from_formula(
    "ltrade ~ ldist + lrgdp + lrgdppc + comlang + border + landl + island + lareap + comcol + curcol + colony + comctry + custrict + regional + bothin + onein + gsp + TimeEffects",
    df[(df["latca1"] == 0) & (df["latca2"] == 0)],
    check_rank=False,
    drop_absorbed=True,
)
tab5_4.fit(cov_type="clustered", cluster_entity=True).params[["bothin", "onein", "gsp"]]

tab5_5 = PanelOLS.from_formula(
    "ltrade ~ ldist + lrgdp + lrgdppc + comlang + border + landl + island + lareap + comcol + curcol + colony + comctry + custrict + regional + bothin + onein + gsp + TimeEffects",
    df[(df["ssafr1"] == 0) & (df["ssafr2"] == 0)],
    check_rank=False,
    drop_absorbed=True,
)
tab5_5.fit(cov_type="clustered", cluster_entity=True).params[["bothin", "onein", "gsp"]]

df["lrgdppc_quartile"] = pd.qcut(df["lrgdppc"], 4, labels=False)
tab5_6 = PanelOLS.from_formula(
    "ltrade ~ ldist + lrgdp + lrgdppc + comlang + border + landl + island + lareap + comcol + curcol + colony + comctry + custrict + regional + bothin + onein + gsp + TimeEffects",
    df[df["lrgdppc_quartile"] != 1],
    check_rank=False,
    drop_absorbed=True,
)
tab5_6.fit(cov_type="clustered", cluster_entity=True).params[["bothin", "onein", "gsp"]]

tab5_7 = PanelOLS.from_formula(
    "ltrade ~ ldist + lrgdp + lrgdppc + comlang + border + landl + island + lareap + comcol + curcol + colony + comctry + custrict + regional + bothin + onein + gsp + TimeEffects",
    df[(df["cty1"] == 156) | (df["cty2"] == 156)],
    check_rank=False,
    drop_absorbed=True,
)
tab5_7.fit(cov_type="clustered", cluster_entity=True).params[["bothin", "gsp"]]

tab5_8 = PanelOLS.from_formula(
    "ltrade ~ ldist + lrgdp + lrgdppc + comlang + border + landl + island + lareap + comcol + curcol + colony + comctry + custrict + regional + bothin + onein + gsp + TimeEffects",
    df[(df["cty1"] == 111) | (df["cty2"] == 111)],
    check_rank=False,
    drop_absorbed=True,
)
tab5_8.fit(cov_type="clustered", cluster_entity=True).params[["bothin", "gsp"]]

tab5_9 = PanelOLS.from_formula(
    "ltrade ~ ldist + lrgdp + lrgdppc + comlang + border + landl + island + lareap + comcol + curcol + colony + comctry + custrict + regional + bothin + onein + gsp + TimeEffects",
    df[(df["cty1"] == 112) | (df["cty2"] == 112)],
    check_rank=False,
    drop_absorbed=True,
)
tab5_9.fit(cov_type="clustered", cluster_entity=True).params[["bothin", "gsp"]]

tab5_10 = PanelOLS.from_formula(
    "ltrade ~ ldist + lrgdp + lrgdppc + comlang + border + landl + island + lareap + comcol + curcol + colony + comctry + custrict + regional + bothin + onein + gsp + TimeEffects",
    df[(df["cty1"] == 132) | (df["cty2"] == 132)],
    check_rank=False,
    drop_absorbed=True,
)
tab5_10.fit(cov_type="clustered", cluster_entity=True).params[["bothin", "gsp"]]

tab5_11 = PanelOLS.from_formula(
    "ltrade ~ ldist + lrgdp + lrgdppc + comlang + border + landl + island + lareap + comcol + curcol + colony + comctry + custrict + regional + bothin + onein + gsp + TimeEffects",
    df[(df["cty1"] == 136) | (df["cty2"] == 136)],
    check_rank=False,
    drop_absorbed=True,
)
tab5_11.fit(cov_type="clustered", cluster_entity=True).params[["bothin", "gsp"]]

tab5_12 = PanelOLS.from_formula(
    "ltrade ~ ldist + lrgdp + lrgdppc + comlang + border + landl + island + lareap + comcol + curcol + colony + comctry + custrict + regional + bothin + onein + gsp + TimeEffects",
    df[(df["cty1"] == 134) | (df["cty2"] == 134)],
    check_rank=False,
    drop_absorbed=True,
)
tab5_12.fit(cov_type="clustered", cluster_entity=True).params[
    ["bothin", "onein", "gsp"]
]

tab5_13 = PanelOLS.from_formula(
    "ltrade ~ ldist + lrgdp + lrgdppc + comlang + border + landl + island + lareap + comcol + curcol + colony + comctry + custrict + regional + bothin + onein + gsp + TimeEffects",
    df[(df["cty1"] == 158) | (df["cty2"] == 158)],
    check_rank=False,
    drop_absorbed=True,
)
tab5_13.fit(cov_type="clustered", cluster_entity=True).params[
    ["bothin", "onein", "gsp"]
]

# Table 6
tab6_1 = PanelOLS.from_formula(
    "ltrade ~ ldist + lrgdp + lrgdppc + comlang + border + landl + island + lareap + comcol + curcol + colony + comctry + custrict + regional + bothin + onein + gsp + TimeEffects",
    df,
    check_rank=False,
    drop_absorbed=True,
)
tab6_1.fit(cov_type="clustered", cluster_entity=True)

tab6_2 = sm.OLS.from_formula(
    "ltrade ~ ldist + lrgdp + lrgdppc + comlang + border + landl + island + lareap + comcol + curcol + colony + comctry + custrict + regional + bothin + onein + gsp",
    data=df,
)
tab6_2.fit(cov_type="cluster", cov_kwds={"groups": df["pairid"]}).summary()

tab6_3 = PanelOLS.from_formula(
    "ltrade ~ ldist + lrgdp + lrgdppc + comlang + border + landl + island + lareap + comcol + curcol + colony + comctry + custrict + regional + bothin + onein + gsp + C(rta) + TimeEffects",
    df,
    check_rank=False,
    drop_absorbed=True,
)
tab6_3.fit(cov_type="clustered", cluster_entity=True)

df["group"] = 1
vcf = {"year": "0 + C(year)", "pairid": "0 + C(pairid)"}
tab6_4 = sm.MixedLM.from_formula(
    "ltrade ~ ldist + lrgdp + lrgdppc + comlang + border + landl + island + lareap + comcol + curcol + colony + comctry + custrict + regional + bothin + onein + gsp",
    groups="group",
    vc_formula=vcf,
    re_formula="~year",
    data=df,
)
tab6_4.fit()

tab6_5 = PanelOLS.from_formula(
    "ltrade ~ ldist + lrgdp + lrgdppc + comlang + border + landl + island + lareap + comcol + curcol + colony + comctry + custrict + regional + bothin + onein + gsp + EntityEffects",
    df,
    check_rank=False,
    drop_absorbed=True,
)
tab6_5.fit(cov_type="clustered", cluster_entity=True)

tab6_6 = PanelOLS.from_formula(
    "ltrade ~ ldist + lrgdp + lrgdppc + comlang + border + landl + island + lareap + comcol + curcol + colony + comctry + custrict + regional + bothin + onein + gsp + TimeEffects + EntityEffects",
    df,
    check_rank=False,
    drop_absorbed=True,
)
tab6_6.fit(cov_type="clustered", cluster_entity=True)


df = df.set_index("pairid", drop=False)
tab6_7 = RandomEffects.from_formula(
    "ltrade ~ ldist + lrgdp + lrgdppc + comlang + border + landl + island + lareap + comcol + curcol + colony + comctry + custrict + regional + bothin + onein + gsp",
    data=df,
)
tab6_7.fit()
