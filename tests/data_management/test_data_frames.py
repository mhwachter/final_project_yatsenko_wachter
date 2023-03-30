import urllib.request

import numpy as np
import pandas as pd
import pytest
from replication_ppr.config import BLD, SRC

from src.replication_ppr.data_management.dot import create_dot_final


@pytest.fixture()
def data():
    dot = pd.read_csv(SRC / "data" / "DOT.csv")
    rta = pd.read_csv(SRC / "data" / "rta.csv")
    cpi = pd.read_csv(SRC / "data" / "cpi_urban_consumers.csv")
    original_data = pd.read_csv(BLD / "python" / "data" / "original_extended.csv")
    countries_list = pd.read_csv(SRC / "data" / "countries_list.csv")
    data = {
        "dot": dot,
        "rta": rta,
        "original_data": original_data,
        "cpi": cpi,
        "countries_list": countries_list,
    }
    return data


# @pytest.fixture()
# def original_data():


def test_no_na(data):
    assert data["original_data"].notna().all().all(), "There are NAs in the data frame."


def test_numerical(data):
    assert all(
        np.issubdtype(dtype, np.number)
        for dtype in data["original_data"][
            [
                "ldist",
                "lrgdp",
                "lrgdppc",
                "comlang",
                "border",
                "landl",
                "island",
                "lareap",
                "comcol",
                "curcol",
                "colony",
                "comctry",
                "custrict",
                "regional",
                "bothin",
                "onein",
                "gsp",
            ]
        ].dtypes
    ), "Certain columns that should be numeric are not."


def test_unique_country_year_pairs(data):
    assert data["original_data"][
        "pair_year_id_ISO3"
    ].is_unique, "There are multiple observation for a country pair in a given year, which should not be the case."


def test_dot(data):
    dot = data["dot"]
    cpi = data["cpi"]
    countries_list = data["countries_list"]
    dot = create_dot_final(data=dot, cpi=cpi, countries_list=countries_list)
    assert all(
        dot["pair_year_id"].value_counts() <= 2,
    ), "For a given country pair there are more than two observations."


@pytest.fixture()
def cia_url():
    url = "https://www.cia.gov/the-world-factbook/"
    return url


def test_site_reachable(cia_url):
    urllib.request.urlopen(cia_url).getcode() == 200, "Site is not reachable"
