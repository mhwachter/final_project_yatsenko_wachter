rm(list = ls())

library(jsonlite)
library(modelsummary)
library(kableExtra)
library(plm)
library(AER)
library(quantreg)

args <- commandArgs(trailingOnly = TRUE)
path_to_json <- args[length(args)]
config <- read_json(path_to_json)

depends_on <- config$depends_on
produces <- config$produces

create_table6 <- function(models) {
  tab6_models <- readRDS(models)
  tab6_tex <- modelsummary(tab6_models,
    fmt = 2, gof_map = "none",
    coef_map = c("bothin", "onein", "gsp"), group = model ~ term,
    output = "latex", title = "Sample Sensitvity Analysis"
  )
  save_kable(tab6_tex, file = produces)
}

create_table6(models = depends_on)
