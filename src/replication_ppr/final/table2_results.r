rm(list = ls())

library(jsonlite)
library(modelsummary)
library(kableExtra)

args <- commandArgs(trailingOnly = TRUE)
path_to_json <- args[length(args)]
config <- read_json(path_to_json)

depends_on <- config$depends_on
produces <- config$produces

create_table2 <- function(models) {
  tab2_models <- readRDS(models)
  tab2_tex <- modelsummary(tab2_models,
    fmt = 2, vcov = ~pairid, gof_map = "none",
    coef_map = c("bothin", "onein", "gsp"), group = model ~ term,
    output = "latex", title = "Cross-Sectional Analysis"
  )
  save_kable(tab2_tex, file = produces)
}

create_table2(models = depends_on)
