import pandas as pd

# WTO countries code to delete to date and just leave the year.
join = pd.read_excel("src/replication_ppr/data/Countries_member_WTO.xls")
join = pd.DataFrame(join)
join = join.rename(columns={"Membership Date": "Membership_Date"})
join["Membership_Date"] = pd.to_datetime(join["Membership_Date"])
join["join"] = join["Membership_Date"].dt.strftime("%Y")
join["join"] = join["join"].fillna(10000)
join = join.drop(columns="Membership_Date")
