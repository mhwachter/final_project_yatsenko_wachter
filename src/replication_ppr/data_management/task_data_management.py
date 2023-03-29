"""Tasks for doing the data management."""

import pandas as pd
import pytask

from replication_ppr.config import BLD, SRC
from replication_ppr.data_management.dot import create_dot_final
from replication_ppr.data_management.final_dataset import (
    add_original_variables,
    calc_additional_vars,
    do_merge,
    rename_columns,
)
from replication_ppr.data_management.original_data import extend_original_data
from replication_ppr.data_management.rta import create_rta_final, unzip_rta_data
from replication_ppr.data_management.wb_classification import get_wb_classification


@pytask.mark.depends_on(
    {
        "countries_list": SRC / "data" / "countries_list.csv",
        "rta_zip": SRC / "data" / "rta.csv.zip",
        "rta_unzip": SRC / "data",
    },
)
@pytask.mark.produces(
    {
        "rta_final": BLD / "python" / "data" / "rta_final.csv",
    },
)
def task_create_rta_final(depends_on, produces):
    """Create final RTA Dataset."""
    unzip_rta_data(zip=depends_on["rta_zip"], unzip=depends_on["rta_unzip"])
    rta = pd.read_csv(SRC / "data" / "rta.csv")
    countries_list = pd.read_csv(depends_on["countries_list"])
    rta = create_rta_final(data=rta, countries_list=countries_list)
    rta.to_csv(produces["rta_final"], index=False)


@pytask.mark.depends_on(
    {
        "countries_list": SRC / "data" / "countries_list.csv",
        "dot": SRC / "data" / "DOT.csv",
        "cpi": SRC / "data" / "cpi_urban_consumers.csv",
    },
)
@pytask.mark.produces(
    {
        "dot_final": BLD / "python" / "data" / "dot_final.csv",
    },
)
def task_create_dot_final(depends_on, produces):
    dot = pd.read_csv(depends_on["dot"])
    cpi = pd.read_csv(depends_on["cpi"])
    countries_list = pd.read_csv(depends_on["countries_list"])
    dot = create_dot_final(data=dot, cpi=cpi, countries_list=countries_list)
    dot.to_csv(produces["dot_final"], index=False)


@pytask.mark.depends_on(
    {
        "original_data": SRC / "data" / "original_data_paper.csv",
    },
)
@pytask.mark.produces(
    {
        "original_extended": BLD / "python" / "data" / "original_extended.csv",
    },
)
def task_original_data(depends_on, produces):
    original_data = pd.read_csv(depends_on["original_data"])
    original_extended = extend_original_data(data=original_data)
    original_extended.to_csv(produces["original_extended"], index=False)


@pytask.mark.depends_on(
    {
        "wb_classification": SRC / "data" / "wb_classification.csv",
        "least_developed": SRC / "data" / "least_developed.csv",
    },
)
@pytask.mark.produces(
    {
        "wb_region_income": BLD / "python" / "data" / "wb_region_income.csv",
    },
)
def task_wb_classification(depends_on, produces):
    wb_classification = pd.read_csv(depends_on["wb_classification"])
    least_developed = pd.read_csv(depends_on["least_developed"])
    wb_region_income = get_wb_classification(
        wb_classification=wb_classification,
        least_developed=least_developed,
    )
    wb_region_income.to_csv(produces["wb_region_income"])


@pytask.mark.depends_on(
    {
        "cia_factbook": BLD / "python" / "data" / "cia_factbook.csv",
        "distance_final": BLD / "python" / "data" / "distance_final.csv",
        "dot_final": BLD / "python" / "data" / "dot_final.csv",
        "rta_final": BLD / "python" / "data" / "rta_final.csv",
        "wb_region_income": BLD / "python" / "data" / "wb_region_income.csv",
        "original_extended": BLD / "python" / "data" / "original_extended.csv",
    },
)
@pytask.mark.produces(BLD / "python" / "data" / "data_final.csv")
def task_final_dataset(depends_on, produces):
    cia_fact = pd.read_csv(depends_on["cia_factbook"])
    dot = pd.read_csv(depends_on["dot_final"])
    rta = pd.read_csv(depends_on["rta_final"])
    wb_reg_inc = pd.read_csv(depends_on["wb_region_income"])
    dist = pd.read_csv(depends_on["distance_final"])
    original_extended = pd.read_csv(depends_on["original_extended"])
    final_dataset = do_merge(
        dot=dot,
        rta=rta,
        dist=dist,
        wb_reg_inc=wb_reg_inc,
        cia_fact=cia_fact,
    )
    final_dataset = add_original_variables(
        data=final_dataset,
        original_data=original_extended,
    )
    final_dataset = rename_columns(data=final_dataset)
    final_dataset = calc_additional_vars(data=final_dataset)
    final_dataset.to_csv(produces)
