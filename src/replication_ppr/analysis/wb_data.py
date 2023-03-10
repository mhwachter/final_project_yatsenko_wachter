import wbgapi as wb

data_wb = wb.data.DataFrame(
    series=[
        "SP.POP.TOTL",
        "NY.GDP.MKTP.KD",
        "NY.GDP.MKTP.KN",
        "NY.GDP.MKTP.CN",
        "NY.GDP.MKTP.CD",
    ],
    economy="all",
    time="all",
    columns="series",
    labels=True,
)
data_wb

data_wb.to_csv(
    "/Users/marcel/sciebo/Uni/MSc/3rd/EPP/epp-2022/final_project/final_project_yatsenko_wachter/src/replication_ppr/data/data_wb.csv",
)
