rm(list = ls())

library(jsonlite)
library(modelsummary)
library(kableExtra)

args <- commandArgs(trailingOnly = TRUE)
path_to_json <- args[length(args)]
config <- read_json(path_to_json)

depends_on <- config$depends_on
produces <- config$produces

create_table3 <- function(models) {
  tab3_models <- readRDS(models)
  tab3_tex <- modelsummary(tab3_models,
    fmt = 2, gof_map = "none",
    coef_omit = "^(?!.*bothin|.*onein)", coef_rename = TRUE,
    output = "latex",
    title = "Allowing the Effects to Vary Over GATT Rounds"
  )
  tab3_tex <- tab3_tex %>% kable_styling(latex_options = "scale_down")
  save_kable(tab3_tex, file = produces)
}

create_table3(models = depends_on)
