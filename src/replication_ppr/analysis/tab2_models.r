rm(list = ls())

library(jsonlite)
library(data.table)
library(fixest)

args <- commandArgs(trailingOnly = TRUE)
path_to_json <- args[length(args)]
config <- read_json(path_to_json)

depends_on <- config$depends_on
produces <- config$produces

tab2_est_models <- function(data, controls) {
  m1 <- feols(fml = ltrade ~ .[controls] | year, data = data, split = ~ year %keep% c("1950", "1955", "1960", "1965", "1970", "1975", "1980", "1985", "1990", "1995"))

  saveRDS(m1, file = produces)
}

df <- fread(file = depends_on)
ctrls <- c(
  "ldist", "lrgdp", "lrgdppc", "comlang", "border", "landl", "island",
  "lareap", "comcol", "curcol", "colony", "comctry", "custrict",
  "regional", "bothin", "onein", "gsp"
)

tab2_est_models(data = df, controls = ctrls)
