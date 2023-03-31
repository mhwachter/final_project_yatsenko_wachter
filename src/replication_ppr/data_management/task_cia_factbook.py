"""Tasks for doing scraping the CIA Factbook data."""

import pandas as pd
import pytask
from replication_ppr.config import BLD, SRC
from replication_ppr.data_management.cia_factbook import (
    cia_factbook_cleaning,
    correct_country_names,
    get_cia_factbook_countries,
    scrape_cia_factbook_data,
)


@pytask.mark.depends_on(
    {
        "countries_list": SRC / "data" / "countries_list.csv",
    },
)
@pytask.mark.produces(
    {
        "cia_factbook": BLD / "python" / "data" / "cia_factbook.csv",
    },
)
def task_cia_factbook(depends_on, produces):
    """This function scrapes data from the CIA World Factbook website for a list of countries,
cleans the data, and saves the output."""
    countries_cia = get_cia_factbook_countries()
    countries_list = pd.read_csv(depends_on["countries_list"])
    countries_cia = correct_country_names(
        data=countries_cia,
        countries_list=countries_list,
    )
    cia_factbook = scrape_cia_factbook_data(countries_cia=countries_cia)
    cia_factbook = cia_factbook_cleaning(data=cia_factbook)
    cia_factbook.to_csv(produces["cia_factbook"])
