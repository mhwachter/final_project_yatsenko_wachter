"""Python script that tests if the fixed effect estimation provided by fixest delivers
similar results."""
import math

import pandas as pd
import pytask
from replication_ppr.config import BLD, TEST_DIR


@pytask.mark.depends_on(BLD / "python" / "data" / "original_extended.csv")
@pytask.mark.r(script=TEST_DIR / "analysis" / "check_tab_1_1.r")
@pytask.mark.produces(BLD / "R" / "tables" / "tab_1_1_model.csv")
def task_run_tab_1_1():
    pass


@pytask.mark.depends_on(BLD / "R" / "tables" / "tab_1_1_model.csv")
def task_check_tab_1_1(depends_on):
    tab_1_1 = pd.read_csv(depends_on)
    tab_1_1["(1)"] = tab_1_1["(1)"].str.replace("(", "")
    tab_1_1["(1)"] = tab_1_1["(1)"].str.replace(")", "")
    tab_1_1["(1)"] = pd.to_numeric(tab_1_1["(1)"])
    tab_1_1 = tab_1_1["(1)"].tolist()
    expected = [
        -0.04,
        0.05,
        -0.06,
        0.05,
        0.86,
        0.03,
        -1.12,
        0.02,
        0.92,
        0.01,
        0.32,
        0.01,
        1.2,
        0.11,
        1.12,
        0.12,
        0.31,
        0.04,
        0.53,
        0.11,
        0.04,
        0.04,
        -0.1,
        0.01,
        0.58,
        0.07,
        1.08,
        0.23,
        1.16,
        0.12,
        -0.02,
        1.08,
        234597.0,
        0.648,
        1.98,
    ]
    assert all(
        [math.isclose(i, j) for i, j in zip(tab_1_1, expected)],
    ), "Results differ from the original paper for at least one estimate."
