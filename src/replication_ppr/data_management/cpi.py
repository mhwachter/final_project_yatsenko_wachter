"""Python script to import CPI dataset."""
import pandas as pd

cpi = pd.read_csv("../data/cpi_urban_consumers.csv")

cpi_annual = cpi.groupby(["Year"]).mean()
