import pytask

from replication_ppr.config import BLD, SRC


@pytask.mark.depends_on(BLD / "R" / "models" / "tab1_models_created_data.rds")
@pytask.mark.r(script=SRC / "final" / "table1_results.r")
@pytask.mark.produces(BLD / "R" / "tables" / "tab1_results_created_data.tex")
def task_final_r1_own():
    pass


@pytask.mark.depends_on(BLD / "R" / "models" / "tab2_models_created_data.rds")
@pytask.mark.r(script=SRC / "final" / "table2_results.r")
@pytask.mark.produces(BLD / "R" / "tables" / "tab2_results_created_data.tex")
def task_final_r2_own():
    pass


@pytask.mark.depends_on(BLD / "R" / "models" / "tab3_models_created_data.rds")
@pytask.mark.r(script=SRC / "final" / "table3_results.r")
@pytask.mark.produces(BLD / "R" / "tables" / "tab3_results_created_data.tex")
def task_final_r3_own():
    pass


@pytask.mark.depends_on(BLD / "R" / "models" / "tab4_models_created_data.rds")
@pytask.mark.r(script=SRC / "final" / "table4_results.r")
@pytask.mark.produces(BLD / "R" / "tables" / "tab4_results_created_data.tex")
def task_final_r4_own():
    pass


@pytask.mark.depends_on(BLD / "R" / "models" / "tab5_models_created_data.rds")
@pytask.mark.r(script=SRC / "final" / "table5_results.r")
@pytask.mark.produces(BLD / "R" / "tables" / "tab5_results_created_data.tex")
def task_final_r5_own():
    pass


# @pytask.mark.depends_on(BLD / "R" / "models" / "tab6_models_created_data.rds")
# @pytask.mark.r(script=SRC / "final" / "table6_results.r")
# @pytask.mark.produces(BLD / "R" / "tables" / "tab6_results_created_data.tex")
# def task_final_r6_own():
#     pass


@pytask.mark.depends_on(BLD / "R" / "models" / "tab8_models_created_data.rds")
@pytask.mark.r(script=SRC / "final" / "table8_results.r")
@pytask.mark.produces(BLD / "R" / "tables" / "tab8_results_created_data.tex")
def task_final_r8_own():
    pass
