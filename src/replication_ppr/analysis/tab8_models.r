rm(list = ls())

library(jsonlite)
library(data.table)
library(fixest)

args <- commandArgs(trailingOnly = TRUE)
path_to_json <- args[length(args)]
config <- read_json(path_to_json)

depends_on <- config$depends_on
produces <- config$produces

tab8_est_models <- function(data, controls) {
  m1 <- feols(fml = ltrade ~ .[ctrls] | year, data = df, vcov = cluster ~ pairid)
  m2 <- feols(fml = ltrade ~ bothin + onein + gsp + ldist + lrgdp + lrgdppc | year, data = df, vcov = cluster ~ pairid)
  m3 <- feols(fml = ltrade ~ bothin + onein + gsp | year, data = df, vcov = cluster ~ pairid)
  m4 <- feols(fml = ltrade ~ .[ctrls_m4] + found1 + found2 + minyrs + maxyrs | year, data = df, vcov = cluster ~ pairid)

  tab8_models <- list(m1, m2, m3, m4)
  saveRDS(tab8_models, file = produces)
}

df <- fread(file = depends_on)
ctrls <- c(
  "ldist", "lrgdp", "lrgdppc", "comlang", "border", "landl", "island",
  "lareap", "comcol", "curcol", "colony", "comctry", "custrict",
  "regional", "bothin", "onein", "gsp"
)
ctrls_m4 <- c(
  "ldist", "lrgdp", "lrgdppc", "comlang", "border", "landl", "island",
  "lareap", "comcol", "curcol", "colony", "comctry", "custrict",
  "regional", "gsp"
)

tab8_est_models(data = df, controls = ctrls)
