import country_converter as coco
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

browser = webdriver.Firefox()  # open a browser
browser.get("https://www.cia.gov/the-world-factbook/countries/")
element = browser.find_element(By.CLASS_NAME, "pagination__arrow-right")
countries_cia = []
for _i in range(1, 23):
    soup = BeautifulSoup(browser.page_source, features="html5lib")
    for el in soup.find_all("a", {"class": "inline-link"}):
        countries_cia.append(el.get_text())
    element.click()

countries_cia = [
    "united-states-pacific-island-wildlife-refuges"
    if x == "Baker Island"
    or x == "Howland Island"
    or x == "Jarvis Island"
    or x == "Johnston Atoll"
    or x == "Kingman Reef"
    or x == "Midway Islands"
    or x == "Palmyra Atoll"
    else x
    for x in countries_cia
]
countries_cia = [x.lower() for x in countries_cia]
countries_cia = [s.replace(" ", "-") for s in countries_cia]
countries_cia = [s.replace(",", "") for s in countries_cia]
countries_cia = [s.replace("(", "") for s in countries_cia]
countries_cia = [s.replace(")", "") for s in countries_cia]
countries_cia = [s.replace("`", "") for s in countries_cia]
countries_cia = list(dict.fromkeys(countries_cia))

countries_cia_standard = coco.convert(
    names=countries_cia,
    to="name_short",
    not_found=None,
)

countries_list = pd.read_csv(
    "/Users/marcel/sciebo/Uni/MSc/3rd/EPP/epp-2022/final_project/final_project_yatsenko_wachter/src/replication_ppr/data/countries_list.csv",
)

countries_list = countries_list["country"].to_list()

countries_list_standard = coco.convert(
    names=countries_list,
    to="name_short",
    not_found=None,
)

cia = pd.DataFrame(
    {"countries_cia": countries_cia, "countries_cia_standard": countries_cia_standard},
)
list = pd.DataFrame(
    {
        "countries_list": countries_list,
        "countries_list_standard": countries_list_standard,
    },
)
cia = cia.drop_duplicates(subset="countries_cia_standard", keep="last")

new = pd.merge(
    list,
    cia,
    how="left",
    left_on="countries_list_standard",
    right_on="countries_cia_standard",
)
new = new.dropna()
new

countries_cia = new.countries_cia.to_list()

coordinates = []
d = []
for country in countries_cia:
    url = "https://www.cia.gov/the-world-factbook/countries/" + str(country)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    geography = soup.find("div", attrs={"id": "geography"})
    government = soup.find("div", attrs={"id": "government"})
    people_society = soup.find("div", attrs={"id": "people-and-society"})
    d.append(
        {
            "country": soup.find("h1", attrs={"class": "hero-title"}).get_text(),
            "coordinates": geography.find_all("p")[1].get_text(),
            "landlocked": geography.find_all("p")[6].get_text(),
            "language": people_society.find_all("p")[3].get_text().split(" ")[0],
            "area": geography.find_all("p")[3].get_text().split(" ")[1],
            "island": geography.find_all("p")[5].text.split(" ")[1],
        },
    )

data = pd.DataFrame(d)
data.loc[~data["landlocked"].str.contains("landlocked", na=False), "landlocked"] = 0
data.loc[data["landlocked"].str.contains("landlocked", na=False), "landlocked"] = 1
data["island"] = data["island"].str.replace(",", "")
data.dtypes
