"""Python script defines various Pytask tasks with self-sourced data."""
import pytask

from replication_ppr.config import BLD, SRC


@pytask.mark.depends_on(BLD / "python" / "data" / "data_final.csv")
@pytask.mark.r(script=SRC / "analysis" / "tab1_models.r")
@pytask.mark.produces(BLD / "R" / "models" / "tab1_models_created_data.rds")
def task_analysis_r1_own():
    pass


@pytask.mark.depends_on(BLD / "python" / "data" / "data_final.csv")
@pytask.mark.r(script=SRC / "analysis" / "tab2_models.r")
@pytask.mark.produces(BLD / "R" / "models" / "tab2_models_created_data.rds")
def task_analysis_r2_own():
    pass


@pytask.mark.depends_on(BLD / "python" / "data" / "data_final.csv")
@pytask.mark.r(script=SRC / "analysis" / "tab3_models.r")
@pytask.mark.produces(BLD / "R" / "models" / "tab3_models_created_data.rds")
def task_analysis_r3_own():
    pass


@pytask.mark.depends_on(BLD / "python" / "data" / "data_final.csv")
@pytask.mark.r(script=SRC / "analysis" / "tab4_models.r")
@pytask.mark.produces(BLD / "R" / "models" / "tab4_models_created_data.rds")
def task_analysis_r4_own():
    pass


@pytask.mark.depends_on(BLD / "python" / "data" / "data_final.csv")
@pytask.mark.r(script=SRC / "analysis" / "tab5_models_excl_JPN.r")
@pytask.mark.produces(BLD / "R" / "models" / "tab5_models_created_data.rds")
def task_analysis_r5_own():
    pass


# @pytask.mark.depends_on(BLD / "python" / "data" / "data_final.csv")
# @pytask.mark.r(script=SRC / "analysis" / "tab6_models.r")
# @pytask.mark.produces(BLD / "R" / "models" / "tab6_models_created_data.rds")
# def task_analysis_r6_own():
#     pass


@pytask.mark.depends_on(BLD / "python" / "data" / "data_final.csv")
@pytask.mark.r(script=SRC / "analysis" / "tab8_models.r")
@pytask.mark.produces(BLD / "R" / "models" / "tab8_models_created_data.rds")
def task_analysis_r8_own():
    pass
