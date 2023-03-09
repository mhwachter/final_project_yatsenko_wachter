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
)
data_wb
