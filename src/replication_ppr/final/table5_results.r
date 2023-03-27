rm(list = ls())

library(jsonlite)
library(modelsummary)
library(kableExtra)

args <- commandArgs(trailingOnly = TRUE)
path_to_json <- args[length(args)]
config <- read_json(path_to_json)

depends_on <- config$depends_on
produces <- config$produces

create_table5 <- function(models) {
  tab5_models <- readRDS(models)
  tab5_tex <- modelsummary(tab5_models,
    fmt = 2, gof_map = "none",
    coef_map = c("bothin", "onein", "gsp"), group = model ~ term,
    output = "latex", title = "Sample Sensitvity Analysis"
  )
  save_kable(tab5_tex, file = produces)
}

create_table5(models = depends_on)
