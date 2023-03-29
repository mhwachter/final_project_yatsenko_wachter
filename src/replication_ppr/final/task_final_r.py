import pytask

from replication_ppr.config import BLD, SRC


@pytask.mark.depends_on(BLD / "R" / "models" / "tab1_models.rds")
@pytask.mark.r(script=SRC / "final" / "table1_results.r")
@pytask.mark.produces(BLD / "R" / "tables" / "tab1_results.tex")
def task_final_r1():
    pass


@pytask.mark.depends_on(BLD / "R" / "models" / "tab2_models.rds")
@pytask.mark.r(script=SRC / "final" / "table2_results.r")
@pytask.mark.produces(BLD / "R" / "tables" / "tab2_results.tex")
def task_final_r2():
    pass


@pytask.mark.depends_on(BLD / "R" / "models" / "tab3_models.rds")
@pytask.mark.r(script=SRC / "final" / "table3_results.r")
@pytask.mark.produces(BLD / "R" / "tables" / "tab3_results.tex")
def task_final_r3():
    pass


@pytask.mark.depends_on(BLD / "R" / "models" / "tab4_models.rds")
@pytask.mark.r(script=SRC / "final" / "table4_results.r")
@pytask.mark.produces(BLD / "R" / "tables" / "tab4_results.tex")
def task_final_r4():
    pass


@pytask.mark.depends_on(BLD / "R" / "models" / "tab5_models.rds")
@pytask.mark.r(script=SRC / "final" / "table5_results.r")
@pytask.mark.produces(BLD / "R" / "tables" / "tab5_results.tex")
def task_final_r5():
    pass


@pytask.mark.depends_on(BLD / "R" / "models" / "tab6_models.rds")
@pytask.mark.r(script=SRC / "final" / "table6_results.r")
@pytask.mark.produces(BLD / "R" / "tables" / "tab6_results.tex")
def task_final_r6():
    pass


@pytask.mark.depends_on(BLD / "R" / "models" / "tab8_models.rds")
@pytask.mark.r(script=SRC / "final" / "table8_results.r")
@pytask.mark.produces(BLD / "R" / "tables" / "tab8_results.tex")
def task_final_r8():
    pass
