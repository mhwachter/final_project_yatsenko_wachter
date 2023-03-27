rm(list = ls())

library(jsonlite)
library(modelsummary)
library(kableExtra)

args <- commandArgs(trailingOnly = TRUE)
path_to_json <- args[length(args)]
config <- read_json(path_to_json)

depends_on <- config$depends_on
produces <- config$produces

create_table8 <- function(models) {
  tab8_models <- readRDS(models)
  tab8_tex <- modelsummary(tab8_models,
    fmt = 2, gof_map = c("r.squared", "rmse"),
    coef_map = c(
      "bothin", "onein", "gsp", "found1", "found2", "minyrs",
      "maxyrs", "ldist", "lrgdp", "lrgdppc", "regional", "custrict",
      "comlang", "border", "landlocked", "island", "lareap", "comcol",
      "curcol", "colony", "comctry"
    ), output = "latex",
    title = "Perturbations of the Gravity Model"
  )
  save_kable(tab8_tex, file = produces)
}

create_table8(models = depends_on)
