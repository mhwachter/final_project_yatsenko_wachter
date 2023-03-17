import numpy as np
import pandas as pd

dot = pd.read_csv("../data/DOT_03-08-2023 16-25-54-79_panel.csv")

dot.columns

dot = dot.rename(
    columns={
        "Goods, Value of Exports, Free on board (FOB), US Dollars (TXG_FOB_USD)": "FOB Exports",
        "Goods, Value of Imports, Cost, Insurance, Freight (CIF), US Dollars (TMG_CIF_USD)": "CIF Imports",
    },
)

dot["value"] = np.abs(dot["FOB Exports"] - dot["CIF Imports"])

cpi = pd.read_csv("../data/cpi_urban_consumers.csv")

cpi_annual = cpi.groupby(["Year"]).mean()
cpi_annual["Value/100"] = cpi_annual["Value"] / 100

dot["trade"] = np.abs(dot["Goods, Value of Trade Balance, US Dollars (TBG_USD)"])

dot["ltrade"] = np.log(
    np.abs(dot["Goods, Value of Trade Balance, US Dollars (TBG_USD)"]),
)

dot["ltrade"]
