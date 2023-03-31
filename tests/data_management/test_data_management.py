import urllib.request

import numpy as np
import pandas as pd
import pytest
from pandas.util.testing import assert_frame_equal
from replication_ppr.config import BLD, SRC

from src.replication_ppr.data_management.dot import create_dot_final
from src.replication_ppr.data_management.wb_classification import get_wb_classification


@pytest.fixture()
def data():
    dot = pd.read_csv(SRC / "data" / "DOT.csv")
    rta = pd.read_csv(SRC / "data" / "rta.csv")
    cpi = pd.read_csv(SRC / "data" / "cpi_urban_consumers.csv")
    original_data = pd.read_csv(BLD / "python" / "data" / "original_extended.csv")
    data_final = pd.read_csv(BLD / "python" / "data" / "data_final.csv")
    countries_list = pd.read_csv(SRC / "data" / "countries_list.csv")
    data = {
        "dot": dot,
        "rta": rta,
        "original_data": original_data,
        "cpi": cpi,
        "countries_list": countries_list,
        "data_final": data_final,
    }
    return data


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


def test_unique_country_year_pairs1(data):
    assert data["original_data"][
        "pair_year_id_ISO3"
    ].is_unique, "There are multiple observation for a country pair in a given year, which should not be the case."


def test_unique_country_year_pairs2(data):
    assert data["data_final"][
        "pair_year_id_ISO3"
    ].is_unique, "There are multiple observation for a country pair in a given year, which should not be the case."


def test_dot(data):
    dot = data["dot"]
    cpi = data["cpi"]
    countries_list = data["countries_list"]
    dot = create_dot_final(data=dot, cpi=cpi, countries_list=countries_list)
    assert dot[
        "pair_year_id"
    ].is_unique, "There are multiple observation for a country pair in a given year, which should not be the case."


@pytest.fixture()
def cia_url():
    url = "https://www.cia.gov/the-world-factbook/"
    return url


def test_site_reachable(cia_url):
    urllib.request.urlopen(cia_url).getcode() == 200, "Site is not reachable"


def test_wb_classification():
    wb_data = pd.DataFrame(
        {
            "Country": [
                "Canada",
                "Rwanda",
                "Zimbabwe",
            ],
            "Income group": ["High income", "Low income", "Lower middle income"],
            "Region": ["North America", "Sub-Saharan Africa", "Sub-Saharan Africa"],
        },
    )
    least_developed = pd.DataFrame({"country": ["Bangladesh", "Rwanda", "Haiti"]})
    expected = pd.DataFrame(
        {
            "Country": ["Canada", "Rwanda", "Zimbabwe"],
            "ISO3": ["CAN", "RWA", "ZWE"],
            "Income group": ["High income", "Low income", "Lower middle income"],
            "Region": ["North America", "Sub-Saharan Africa", "Sub-Saharan Africa"],
            "least": [0, 1, 0],
            "North America": [1, 0, 0],
            "Sub-Saharan Africa": [0, 1, 1],
            "High income": [1, 0, 0],
            "Low income": [0, 1, 0],
            "Lower middle income": [0, 0, 1],
        },
    )
    wb_classification = get_wb_classification(wb_data, least_developed)
    assert_frame_equal(
        wb_classification,
        expected,
        check_dtype=False,
    ), "Data frames are not equal as they should be."
