rm(list = ls())

library(jsonlite)
library(data.table)
library(fixest)

args <- commandArgs(trailingOnly = TRUE)
path_to_json <- args[length(args)]
config <- read_json(path_to_json)

depends_on <- config$depends_on
produces <- config$produces

tab5_est_models <- function(data, controls) {
  m1 <- feols(fml = ltrade ~ .[ctrls] | year, data = df[year < 1980], vcov = cluster ~ pairid)
  m2 <- feols(fml = ltrade ~ .[ctrls] | year, data = df[year > 1979], vcov = cluster ~ pairid)
  m3 <- feols(fml = ltrade ~ .[ctrls] | year, data = df[cty1 < 200 & cty2 < 200], vcov = cluster ~ pairid)
  m4 <- feols(fml = ltrade ~ .[ctrls] | year, data = df[cty1_UNregion != "Eastern Africa" & cty1_UNregion != "Southern Africa" & cty1_UNregion != "Western Africa" & cty1_UNregion != "Northern Africa" & cty1_UNregion != "Middle Africa" & cty2_UNregion != "Eastern Africa" & cty2_UNregion != "Southern Africa" & cty2_UNregion != "Western Africa" & cty2_UNregion != "Northern Africa" & cty2_UNregion != "Middle Africa"], vcov = cluster ~ pairid)
  m5 <- feols(fml = ltrade ~ .[ctrls] | year, data = df[cty1_UNregion != "Caribbean" & cty1_UNregion != "Central America" & cty1_UNregion != "South America" & cty2_UNregion != "Caribbean" & cty2_UNregion != "Central America" & cty2_UNregion != "South America"], vcov = cluster ~ pairid)
  m6 <- feols(fml = ltrade ~ .[ctrls] | year, data = df[!(cty1_ISO3 %in% opec) & !(cty2_ISO3 %in% opec)], vcov = cluster ~ pairid)
  m7 <- feols(fml = ltrade ~ .[ctrls] | year, data = df[regional == 0], vcov = cluster ~ pairid)
  m8 <- feols(fml = ltrade ~ .[ctrls] | year, data = df[quartile_lrgdppc != 1], vcov = cluster ~ pairid)
  m9 <- feols(fml = ltrade ~ .[ctrls] | year, data = df[quartile_lrgdp != 1], vcov = cluster ~ pairid)
  m10 <- feols(fml = ltrade ~ .[ctrls] | year, data = df[outliers != 1], vcov = cluster ~ pairid)
  m11 <- feols(fml = ltrade ~ .[ctrls] | year, data = df[cty1_ISO3 == "CAN" | cty2_ISO3 == "CAN"], vcov = cluster ~ pairid)
  m12 <- feols(fml = ltrade ~ .[ctrls] | year, data = df[cty1_ISO3 == "USA" | cty2_ISO3 == "USA"], vcov = cluster ~ pairid)
  m13 <- feols(fml = ltrade ~ .[ctrls] | year, data = df[cty1_ISO3 == "GBR" | cty2_ISO3 == "GBR"], vcov = cluster ~ pairid)
  m14 <- feols(fml = ltrade ~ .[ctrls] | year, data = df[cty1_ISO3 == "FRA" | cty2_ISO3 == "FRA"], vcov = cluster ~ pairid)
  m15 <- feols(fml = ltrade ~ .[ctrls] | year, data = df[cty1_ISO3 == "ITA" | cty2_ISO3 == "ITA"], vcov = cluster ~ pairid)
  m16 <- feols(fml = ltrade ~ .[ctrls] | year, data = df[cty1_ISO3 == "DEU" | cty2_ISO3 == "DEU"], vcov = cluster ~ pairid)
  #m17 <- feols(fml = ltrade ~ .[ctrls] | year, data = df[cty1_ISO3 == "JPN" | cty2_ISO3 == "JPN"], vcov = cluster ~ pairid)


  tab5_models <- list("Data before 1980" = m1, "Data after 1979" = m2, "Only industrial countries" = m3, "No African countries" = m4, "No Latin or Caribbean countries" = m5, "No OPEC countries" = m6, "No RTA observations" = m7, "Without poorest quartile of real GDP p/c" = m8, "Without smallest quartile of real GDP" = m9, "Without 3sd outliers" = m10, "Only Canadian observations" = m11, "Only American observations" = m12, "Only British observations" = m13, "Only French observations" = m14, "Only Italian observations" = m15, "Only German observations" = m16)
  saveRDS(tab5_models, file = produces)
}

prepare_data <- function(data) {
  data <- data[order(lrgdp), quartile_lrgdp := floor(1 + 4 * (.I - 1) / .N)]
  data <- data[order(lrgdppc), quartile_lrgdppc := floor(1 + 4 * (.I - 1) / .N)]
  mod <- feols(fml = ltrade ~ .[ctrls] | year, data = data)
  data$residuals <- mod$residuals
  sd3 <- 3 * sd(resid(mod))
  data$outliers <- 0
  data[abs(residuals) > sd3, outliers := 1]
}

df <- fread(file = depends_on)
ctrls <- c(
  "ldist", "lrgdp", "lrgdppc", "comlang", "border", "landl", "island",
  "lareap", "comcol", "curcol", "colony", "comctry", "custrict",
  "regional", "bothin", "onein", "gsp"
)
opec <- c("IRN", "IRQ", "KWT", "SAU", "VEN", "LBY", "ARE", "DZA", "NGA")

df <- prepare_data(data = df)
tab5_est_models(data = df, controls = ctrls)
