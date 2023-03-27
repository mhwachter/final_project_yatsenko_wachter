rm(list = ls())

library(jsonlite)
library(data.table)
library(fixest)

args <- commandArgs(trailingOnly = TRUE)
path_to_json <- args[length(args)]
config <- read_json(path_to_json)

depends_on <- config$depends_on
produces <- config$produces

tab3_est_models <- function(data, controls) {
  m1 <- feols(fml = ltrade ~ .[ctrls] + bothin:periods + onein:periods | year, data = df, vcov = cluster ~ pairid)
  m2 <- feols(fml = ltrade ~ .[ctrls] + bothin:periods + onein:periods | pairid, data = df, vcov = cluster ~ pairid)

  tab3_models <- list("OLS year effects" = m1, "Fixed country-pair effects" = m2)
  saveRDS(tab3_models, file = produces)
}

create_gatt_regimes <- function(data) {
  data$periods <- cut(df$year, breaks = c(1948, 1949, 1951, 1956, 1961, 1967, 1979, 1994, 2000), labels = c(
    "Before Annecy round (1949)",
    "Annecy to Torquay round (1951)",
    "Torquay to Geneva round (1956)",
    "Geneva to Dillon round (1961)",
    "Dillon to Kennedy round (1967)",
    "Kennedy to Tokyo round (1979)",
    "Tokyo to Uruguay round (1994)",
    "After Uruguay round"
  ), include.lowest = TRUE, right = FALSE)
  return(data)
}

df <- fread(file = depends_on)
ctrls <- c(
  "ldist", "lrgdp", "lrgdppc", "comlang", "border", "landl", "island",
  "lareap", "comcol", "curcol", "colony", "comctry", "custrict",
  "regional", "gsp"
)
df <- create_gatt_regimes(data = df)

tab3_est_models(data = df, controls = ctrls)
