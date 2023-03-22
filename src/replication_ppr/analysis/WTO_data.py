import pandas as pd

dist = pd.read_csv("../../../bld/python/data/distance_final.csv")
# Work with WTO data.
WTO = pd.read_excel(
    "/Users/anzhelikayatsenko/Desktop/MASTERS/epp-2022/final_project/final_project_yatsenko_wachter/src/replication_ppr/data/WTO_members.xlsx",
    sheet_name="mem-obs-list",
)
WTO = pd.DataFrame(WTO)
WTO["Year"] = pd.to_datetime(WTO["Membership Date"]).dt.year
WTO["Year"] = WTO["Year"].fillna("5000")
WTO = WTO.drop("Membership Date", axis=1)
# GATT Data
GATT = pd.read_excel(
    "/Users/anzhelikayatsenko/Desktop/MASTERS/epp-2022/final_project/final_project_yatsenko_wachter/src/replication_ppr/data/GATT.xlsx",
    sheet_name="mem-obs-list",
)
GATT = pd.DataFrame(GATT)
GATT["Year"] = pd.to_datetime(GATT["Membership Date"]).dt.year
GATT = GATT.drop("Membership Date", axis=1)
# Merging
GATT_WTO = pd.merge(GATT, WTO, how="outer", on="Members")
new_names = {"Year_x": "GATT", "Year_y": "WTO"}
GATT_WTO = GATT_WTO.rename(columns=new_names)
GATT_WTO["GATT"] = GATT_WTO["GATT"].fillna(GATT_WTO["WTO"])
GATT_WTO = pd.DataFrame(GATT_WTO)
GATT_WTO["join"] = GATT_WTO[["GATT", "WTO"]].min(axis=1)
GATT_WTO = GATT_WTO.drop(["GATT", "WTO"], axis=1)

pairs = dist.loc[:, ["pair_id", "ctry1", "ctry2"]]
merged_df = pd.merge(GATT_WTO, pairs, how="inner", left_on="Members", right_on="ctry1")
merged_df = pd.merge(
    merged_df,
    GATT_WTO,
    how="inner",
    left_on="ctry2",
    right_on="Members",
)
