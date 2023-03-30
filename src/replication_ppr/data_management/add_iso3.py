"Python script to create one standard for various country names across dataset."
import country_converter as coco
import pandas as pd

data = pd.read_csv("src/replication_ppr/data/countries_list.csv")
countries_list = data["country"].tolist()
standard_names = coco.convert(names=countries_list, to="ISO3")
data["ISO3"] = standard_names
data.to_csv("src/replication_ppr/data/countries_list.csv")
