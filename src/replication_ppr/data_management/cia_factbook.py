import country_converter as coco
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

cc = coco.CountryConverter()


def get_cia_factbook_countries():
    browser = webdriver.Firefox()
    browser.get("https://www.cia.gov/the-world-factbook/countries/")
    element = browser.find_element(By.CLASS_NAME, "pagination__arrow-right")
    data = []
    for _i in range(1, 23):
        soup = BeautifulSoup(browser.page_source, features="html5lib")
        for el in soup.find_all("a", {"class": "inline-link"}):
            data.append({"country": el.get_text()})
        element.click()

    data = pd.DataFrame(data)
    return data


def correct_country_names(data, countries_list):
    data["country"] = data["country"].str.lower()
    data["country"] = data["country"].replace(
        {" ": "-", ",": "", "\(": "", "\)": "", "`": "", "’": ""}, regex=True
    )

    data["ISO3"] = cc.pandas_convert(series=data["country"], to="ISO3")

    data = data.drop_duplicates(subset="ISO3", keep="first")

    matching_id = data["ISO3"].isin(countries_list["ISO3"])

    data = data.loc[matching_id]
    return data


def scrape_cia_factbook_data(countries_cia):
    d = []
    for country in countries_cia["country"]:
        url = "https://www.cia.gov/the-world-factbook/countries/" + str(country)
        print(url)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        d.append(
            {
                "country": soup.find("h1", attrs={"class": "hero-title"}).get_text(),
                "coordinates": soup.find(
                    "a",
                    attrs={"href": "/the-world-factbook/field/geographic-coordinates"},
                ).next_element.next_element.text
                if country != "france"
                else soup.find(
                    "a",
                    attrs={"href": "/the-world-factbook/field/geographic-coordinates"},
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
    return data


def cia_factbook_cleaning(data):
    data["island"] = data["island"].str.replace(",", "")
    data["area"] = data["area"].str.replace(",", "")

    data["area"] = pd.to_numeric(data["area"])
    data["island"] = pd.to_numeric(data["island"])

    data.loc[
        ~data["landlocked"].str.contains("landlocked", na=False), "landlocked"
    ] = "No"
    data.loc[
        data["landlocked"].str.contains("landlocked", na=False), "landlocked"
    ] = "Yes"

    data.loc[data["island"] != 0, "island"] = "No"
    data.loc[data["island"] == 0, "island"] = "Yes"

    data = data.replace(",", "", regex=True)

    data["ISO3"] = cc.pandas_convert(series=data["country"], to="ISO3")

    data["border_countries"] = data["border_countries"].replace(
        {"\d+": "", "km": "", ";": ",", ", ": ",", " ,": ","}, regex=True
    )

    data["border_countries"] = data["border_countries"].str.strip()

    data["border_countries"] = cc.pandas_convert(
        series=data["border_countries"], to="ISO3", not_found=None
    )

    data.loc[data["island"] == "Yes", "island"] = 1
    data.loc[data["island"] == "No", "island"] = 0

    data.loc[data["landlocked"] == "Yes", "landlocked"] = 1
    data.loc[data["landlocked"] == "No", "landlocked"] = 0

    data = data.reset_index(drop=True)
    return data
