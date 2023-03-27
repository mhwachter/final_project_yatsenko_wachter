import pytask

from replication_ppr.config import BLD, SRC


@pytask.mark.depends_on(BLD / "python" / "data" / "original_extended.csv")
@pytask.mark.r(script=SRC / "analysis" / "tab1_models.r")
@pytask.mark.produces(BLD / "R" / "models" / "tab1_models.rds")
def task_analysis_r1():
    pass


@pytask.mark.depends_on(BLD / "python" / "data" / "original_extended.csv")
@pytask.mark.r(script=SRC / "analysis" / "tab2_models.r")
@pytask.mark.produces(BLD / "R" / "models" / "tab2_models.rds")
def task_analysis_r2():
    pass


@pytask.mark.depends_on(BLD / "python" / "data" / "original_extended.csv")
@pytask.mark.r(script=SRC / "analysis" / "tab3_models.r")
@pytask.mark.produces(BLD / "R" / "models" / "tab3_models.rds")
def task_analysis_r3():
    pass


@pytask.mark.depends_on(BLD / "python" / "data" / "original_extended.csv")
@pytask.mark.r(script=SRC / "analysis" / "tab4_models.r")
@pytask.mark.produces(BLD / "R" / "models" / "tab4_models.rds")
def task_analysis_r4():
    pass


@pytask.mark.depends_on(BLD / "python" / "data" / "original_extended.csv")
@pytask.mark.r(script=SRC / "analysis" / "tab5_models.r")
@pytask.mark.produces(BLD / "R" / "models" / "tab5_models.rds")
def task_analysis_r5():
    pass


@pytask.mark.depends_on(BLD / "python" / "data" / "original_extended.csv")
@pytask.mark.r(script=SRC / "analysis" / "tab8_models.r")
@pytask.mark.produces(BLD / "R" / "models" / "tab8_models.rds")
def task_analysis_r8():
    pass
