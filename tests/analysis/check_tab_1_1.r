rm(list = ls())

library(jsonlite)
library(data.table)
library(modelsummary)
library(fixest)

args <- commandArgs(trailingOnly = TRUE)
path_to_json <- args[length(args)]
config <- read_json(path_to_json)

depends_on <- config$depends_on
produces <- config$produces

df <- fread(file = depends_on)
ctrls <- c(
  "ldist", "lrgdp", "lrgdppc", "comlang", "border", "landl", "island",
  "lareap", "comcol", "curcol", "colony", "comctry", "custrict",
  "regional", "bothin", "onein", "gsp"
)

tab_1_1_model <- feols(fml = ltrade ~ .[ctrls] | year, data = df,vcov = cluster~pairid)
tab_1_1_df <- modelsummary(tab_1_1_model, fmt = 2, coef_map = c("bothin", "onein", "gsp", "ldist", "lrgdp", "lrgdppc", "regional", "custrict", "comlang", "border", "landlocked", "island", "lareap", "comcol", "curcol", "colony", "comctry"), gof_map = c("nobs", "r.squared", "rmse"), output = "data.frame", title = "Benchmark Results")
write.csv(tab_1_1_df,produces)
