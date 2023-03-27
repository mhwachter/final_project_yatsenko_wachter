rm(list = ls())

library(jsonlite)
library(data.table)
library(fixest)

args <- commandArgs(trailingOnly = TRUE)
path_to_json <- args[length(args)]
config <- read_json(path_to_json)

depends_on <- config$depends_on
produces <- config$produces

tab1_est_models <- function(data, controls) {
  m1 <- feols(fml = ltrade ~ .[controls] | year, data = data, vcov = cluster ~ pairid)
  m2 <- feols(fml = ltrade ~ .[controls] | year, data = data[cty1 >= 200 & cty2 >= 200], vcov = cluster ~ pairid)
  m3 <- feols(fml = ltrade ~ .[controls] | year, data = data[year > 1970], vcov = cluster ~ pairid)
  m4 <- feols(fml = ltrade ~ .[controls] + ..("^cd_") | year, data = data, vcov = cluster ~ pairid)

  tab1_models <- list("Default" = m1, "No industrial countries" = m2, "Post 1970" = m3, "With country effects" = m4)
  saveRDS(tab1_models, file = produces)
}

df <- fread(file = depends_on)
ctrls <- c(
  "ldist", "lrgdp", "lrgdppc", "comlang", "border", "landl", "island",
  "lareap", "comcol", "curcol", "colony", "comctry", "custrict",
  "regional", "bothin", "onein", "gsp"
)

tab1_est_models(data = df, controls = ctrls)
