import pytask

from replication_ppr.config import BLD, SRC


@pytask.mark.depends_on(BLD / "python" / "data" / "original_extended.csv")
@pytask.mark.r(script=SRC / "analysis" / "tab1_models.r")
@pytask.mark.produces(BLD / "R" / "models" / "tab1_models.rds")
def task_run_r_script1():
    pass


@pytask.mark.depends_on(BLD / "python" / "data" / "original_extended.csv")
@pytask.mark.r(script=SRC / "analysis" / "tab2_models.r")
@pytask.mark.produces(BLD / "R" / "models" / "tab2_models.rds")
def task_run_r_script2():
    pass


@pytask.mark.depends_on(BLD / "python" / "data" / "original_extended.csv")
@pytask.mark.r(script=SRC / "analysis" / "tab3_models.r")
@pytask.mark.produces(BLD / "R" / "models" / "tab3_models.rds")
def task_run_r_script3():
    pass


@pytask.mark.depends_on(BLD / "python" / "data" / "original_extended.csv")
@pytask.mark.r(script=SRC / "analysis" / "tab4_models.r")
@pytask.mark.produces(BLD / "R" / "models" / "tab4_models.rds")
def task_run_r_script4():
    pass


@pytask.mark.depends_on(BLD / "python" / "data" / "original_extended.csv")
@pytask.mark.r(script=SRC / "analysis" / "tab5_models.r")
@pytask.mark.produces(BLD / "R" / "models" / "tab5_models.rds")
def task_run_r_script5():
    pass


@pytask.mark.depends_on(BLD / "python" / "data" / "original_extended.csv")
@pytask.mark.r(script=SRC / "analysis" / "tab8_models.r")
@pytask.mark.produces(BLD / "R" / "models" / "tab8_models.rds")
def task_run_r_script8():
    pass
