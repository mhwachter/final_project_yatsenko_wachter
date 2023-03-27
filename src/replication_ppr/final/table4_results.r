rm(list = ls())

library(jsonlite)
library(modelsummary)
library(kableExtra)

args <- commandArgs(trailingOnly = TRUE)
path_to_json <- args[length(args)]
config <- read_json(path_to_json)

depends_on <- config$depends_on
produces <- config$produces

create_table4 <- function(models) {
  tab4_models <- readRDS(models)
  tab4_tex <- modelsummary(tab4_models,
    fmt = 2, gof_map = "none",
    coef_map = c("bothin", "onein", "gsp"), group = model ~ term,
    output = "latex", title = "Allowing the Effects to Vary by Region and Income Class"
  )
  save_kable(tab4_tex, file = produces)
}

create_table4(models = depends_on)
