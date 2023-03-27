rm(list = ls())

library(jsonlite)
library(data.table)
library(fixest)

args <- commandArgs(trailingOnly = TRUE)
path_to_json <- args[length(args)]
config <- read_json(path_to_json)

depends_on <- config$depends_on
produces <- config$produces

tab4_est_models <- function(data, controls) {
  m1 <- feols(fml = ltrade ~ .[ctrls] | year, data = df)
  m2 <- feols(fml = ltrade ~ .[ctrls] | year, data = df[sasia1 == 1 | sasia2 == 1])
  m3 <- feols(fml = ltrade ~ .[ctrls] | year, data = df[easia1 == 1 | easia2 == 1])
  m4 <- feols(fml = ltrade ~ .[ctrls] | year, data = df[ssafr1 == 1 | ssafr2 == 1])
  m5 <- feols(fml = ltrade ~ .[ctrls] | year, data = df[menaf1 == 1 | menaf2 == 1])
  m6 <- feols(fml = ltrade ~ .[ctrls] | year, data = df[latca1 == 1 | latca2 == 1])
  m7 <- feols(fml = ltrade ~ .[ctrls] | year, data = df[highi1 == 1 | highi2 == 1])
  m8 <- feols(fml = ltrade ~ .[ctrls] | year, data = df[midin1 == 1 | midin2 == 1])
  m9 <- feols(fml = ltrade ~ .[ctrls] | year, data = df[lowin1 == 1 | lowin2 == 1])
  m10 <- feols(fml = ltrade ~ .[ctrls] | year, data = df[least1 == 1 | least2 == 1])

  tab4_models <- list("Default" = m1, "South Asia" = m2, "East Asia" = m3, "Sub-Saharan Africa" = m4, "Middle East or North Africa" = m5, "Latin America or Caribbean" = m6, "High income" = m7, "Middle income" = m8, "Low income" = m9, "Least developed" = m10)

  saveRDS(tab4_models, file = produces)
}

df <- fread(file = depends_on)
ctrls <- c(
  "ldist", "lrgdp", "lrgdppc", "comlang", "border", "landl", "island",
  "lareap", "comcol", "curcol", "colony", "comctry", "custrict",
  "regional", "bothin", "onein", "gsp"
)

tab4_est_models(data = df, controls = ctrls)
