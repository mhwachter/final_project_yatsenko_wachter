import country_converter as coco
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

cc = coco.CountryConverter()

browser = webdriver.Firefox()
browser.get("https://www.cia.gov/the-world-factbook/countries/")
element = browser.find_element(By.CLASS_NAME, "pagination__arrow-right")
countries_cia_list = []
for _i in range(1, 23):
    soup = BeautifulSoup(browser.page_source, features="html5lib")
    for el in soup.find_all("a", {"class": "inline-link"}):
        countries_cia_list.append({"country": el.get_text()})
    element.click()

# countries_cia = [
#     "united-states-pacific-island-wildlife-refuges"
#     if x == "Baker Island"
#     or x == "Howland Island"
#     or x == "Jarvis Island"
#     or x == "Johnston Atoll"
#     or x == "Kingman Reef"
#     or x == "Midway Islands"
#     or x == "Palmyra Atoll"
#     else x
#     for x in countries_cia
# ]

countries_cia = pd.DataFrame(countries_cia_list)

# countries_cia = list(dict.fromkeys(countries_cia))


countries_cia["country"] = countries_cia["country"].str.lower()
countries_cia["country"] = countries_cia["country"].replace(
    {" ": "-", ",": "", "\(": "", "\)": "", "`": "", "’": ""}, regex=True
)

# countries_cia_standard = coco.convert(
#     names=countries_cia,
#     to="name_short",
#     not_found=None,
# )

countries_cia["ISO3"] = cc.pandas_convert(series=countries_cia["country"], to="ISO3")

countries_list = pd.read_csv(
    "../data/countries_list.csv",
)

# countries_list = countries_list["country"].to_list()

# countries_list_standard = coco.convert(
#     names=countries_list,
#     to="name_short",
#     not_found=None,
# )

# cia = pd.DataFrame(
#     {"countries_cia": countries_cia, "countries_cia_standard": countries_cia_standard},
# )
# list = pd.DataFrame(
#     {
#         "countries_list": countries_list,
#         "countries_list_standard": countries_list_standard,
#     },
# )

countries_cia = countries_cia.drop_duplicates(subset="ISO3", keep="first")

matching_id = countries_cia["ISO3"].isin(countries_list["ISO3"])

countries_cia = countries_cia.loc[matching_id]

# new = pd.merge(
#     list,
#     cia,
#     how="left",
#     left_on="countries_list_standard",
#     right_on="countries_cia_standard",
# )
# new = new.dropna()
# new

# new = new.drop(55)
# countries_cia = new.countries_cia.to_list()

coordinates = []
d = []
for country in countries_cia["country"]:
    url = "https://www.cia.gov/the-world-factbook/countries/" + str(country)
    print(url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    geography = soup.find("div", attrs={"id": "geography"})
    government = soup.find("div", attrs={"id": "government"})
    people_society = soup.find("div", attrs={"id": "people-and-society"})
    d.append(
        {
            "country": soup.find("h1", attrs={"class": "hero-title"}).get_text(),
            "coordinates": soup.find(
                "a", attrs={"href": "/the-world-factbook/field/geographic-coordinates"}
            ).next_element.next_element.text
            if country != "france"
            else soup.find(
                "a", attrs={"href": "/the-world-factbook/field/geographic-coordinates"}
            )
            .next_element.next_element.text.split(";")[0]
            .split(": ")[1],
            "landlocked": soup.find(
                "a", attrs={"href": "/the-world-factbook/field/coastline"}
            ).next_element.next_element.text,
            "language": soup.find(
                "a", attrs={"href": "/the-world-factbook/field/languages"}
            ).next_element.next_element.text.split(" ")[0],
            "area": soup.find(
                "a", attrs={"href": "/the-world-factbook/field/area"}
            ).next_element.next_element.text.split(" ")[1],
            "island": soup.find(
                "a", attrs={"href": "/the-world-factbook/field/land-boundaries"}
            ).next_element.next_element.text.split(" ")[1],
            "border_countries": soup.find(
                "a", attrs={"href": "/the-world-factbook/field/land-boundaries"}
            ).next_element.next_element.text.split(": ", 2)[2]
            if soup.find(
                "a", attrs={"href": "/the-world-factbook/field/land-boundaries"}
            ).next_element.next_element.text.split("border", 1)[0]
            != "total: 0 km"
            else np.nan,
        }
    )

data = pd.DataFrame(d)

# data = data.drop(53)

data["island"] = data["island"].str.replace(",", "")
data["area"] = data["area"].str.replace(",", "")

data["area"] = pd.to_numeric(data["area"])
data["island"] = pd.to_numeric(data["island"])

data.loc[~data["landlocked"].str.contains("landlocked", na=False), "landlocked"] = "No"
data.loc[data["landlocked"].str.contains("landlocked", na=False), "landlocked"] = "Yes"

data.loc[data["island"] != 0, "island"] = "No"
data.loc[data["island"] == 0, "island"] = "Yes"

data = data.replace(",", "", regex=True)

data["ISO3"] = cc.pandas_convert(series=data["country"], to="ISO3")

data["border_countries"] = data["border_countries"].str.replace("\d+", "")
data["border_countries"] = data["border_countries"].str.replace("km", "")
data["border_countries"] = data["border_countries"].str.replace(";", ",")
data["border_countries"] = data["border_countries"].str.strip()
data["border_countries"] = data["border_countries"].str.replace(", ", ",")
data["border_countries"] = data["border_countries"].str.replace(" ,", ",")

# data["border_countries"] = data["border_countries"].str.split(",")

data["border_countries"] = cc.pandas_convert(
    series=data["border_countries"], to="ISO3", not_found=None
)

data.to_csv("../data/cia_factbook.csv")
