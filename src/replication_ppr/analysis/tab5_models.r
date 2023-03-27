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
  m1 <- feols(fml = ltrade ~ .[ctrls] | year, data = df[year < 1980])
  m2 <- feols(fml = ltrade ~ .[ctrls] | year, data = df[year > 1979])
  m3 <- feols(fml = ltrade ~ .[ctrls] | year, data = df[cty1 < 200 & cty2 < 200])
  m4 <- feols(fml = ltrade ~ .[ctrls] | year, data = df[ssafr1 == 0 & ssafr2 == 0 & menaf1 == 0 & menaf2 == 0])
  m5 <- feols(fml = ltrade ~ .[ctrls] | year, data = df[latca1 == 0 & latca2 == 0])
  m6 <- feols(fml = ltrade ~ .[ctrls] | year, data = df[!(cty1 %in% opec) & !(cty2 %in% opec)])
  m7 <- feols(fml = ltrade ~ .[ctrls] | year, data = df[regional == 0])
  m8 <- feols(fml = ltrade ~ .[ctrls] | year, data = df[quartile_lrgdppc != 1])
  m9 <- feols(fml = ltrade ~ .[ctrls] | year, data = df[quartile_lrgdp != 1])
  m10 <- feols(fml = ltrade ~ .[ctrls] | year, data = df[outliers != 1])
  m11 <- feols(fml = ltrade ~ .[ctrls] | year, data = df[cty1 == 156 | cty2 == 156])
  m12 <- feols(fml = ltrade ~ .[ctrls] | year, data = df[cty1 == 111 | cty2 == 111])
  m13 <- feols(fml = ltrade ~ .[ctrls] | year, data = df[cty1 == 112 | cty2 == 112])
  m14 <- feols(fml = ltrade ~ .[ctrls] | year, data = df[cty1 == 132 | cty2 == 132])
  m15 <- feols(fml = ltrade ~ .[ctrls] | year, data = df[cty1 == 136 | cty2 == 136])
  m16 <- feols(fml = ltrade ~ .[ctrls] | year, data = df[cty1 == 134 | cty2 == 134])
  m17 <- feols(fml = ltrade ~ .[ctrls] | year, data = df[cty1 == 158 | cty2 == 158])


  tab1_models <- list("Data before 1980" = m1, "Data after 1979" = m2, "Only industrial countries" = m3, "No African countries" = m4, "No Latin or Caribbean countries" = m5, "No OPEC countries" = m6, "No RTA observations" = m7, "Without poorest quartile of real GDP p/c" = m8, "Without smallest quartile of real GDP" = m9, "Without 3sd outliers" = m10, "Only Canadian observations" = m11, "Only American observations" = m12, "Only British observations" = m13, "Only French observations" = m14, "Only Italian observations" = m15, "Only German observations" = m16, "Only Japanese observations" = m17)
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
opec <- c(429, 433, 443, 456, 299, 453, 536, 672, 466, 612, 694, 248, 646)

df <- prepare_data(data = df)
tab5_est_models(data = df, controls = ctrls)
