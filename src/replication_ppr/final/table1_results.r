rm(list = ls())

library(jsonlite)
library(modelsummary)
library(kableExtra)

args <- commandArgs(trailingOnly = TRUE)
path_to_json <- args[length(args)]
config <- read_json(path_to_json)

depends_on <- config$depends_on
produces <- config$produces

create_table1 <- function(models) {
  tab1_models <- readRDS(models)
  tab1_tex <- modelsummary(tab1_models, fmt = 2, coef_map = c("bothin", "onein", "gsp", "ldist", "lrgdp", "lrgdppc", "regional", "custrict", "comlang", "border", "landlocked", "island", "lareap", "comcol", "curcol", "colony", "comctry"), gof_map = c("nobs", "r.squared", "rmse"), output = "latex", title = "Benchmark Results")
  save_kable(tab1_tex, file = produces)
}

create_table1(models = depends_on)
