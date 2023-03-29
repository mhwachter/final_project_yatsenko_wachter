rm(list = ls())

library(jsonlite)
library(data.table)
library(fixest)
library(plm)
library(AER)
library(quantreg)

args <- commandArgs(trailingOnly = TRUE)
path_to_json <- args[length(args)]
config <- read_json(path_to_json)

depends_on <- config$depends_on
produces <- config$produces

tab6_est_models <- function(data, controls) {
  m1 <- feols(fml = ltrade ~ ldist + I(ldist^2) + lrgdp + I(lrgdp^2) + lrgdppc + I(lrgdppc^2) + comlang + border + landl + island + lareap + comcol + curcol + colony + comctry + custrict + regional + bothin + onein + gsp | year, data = df,vcov = cluster ~ pairid)
  m2 <- feols(fml = ltrade ~ .[ctrls], data = df,vcov = cluster ~ pairid)
  m3 <- feols(fml = ltrade ~ .[ctrls] + i(rta) | year, data = df,vcov = cluster ~ pairid)
  m4 <- plm(formula = frml, data = df,effect = "individual", model = "random",index = "pairid")
  m5 <- feols(fml = ltrade ~ .[ctrls] | pairid,data = df,vcov = cluster ~ pairid)
  m6 <- plm(formula = frml, data = df,effect = "twoways",model = "random",index = c("pairid","year"))
  m7 <- feols(fml = ltrade ~ .[ctrls] | pairid + year,data = df,vcov = cluster ~ pairid)
  m8 <- rq(formula = frml, tau = 0.5, data = df)
  m9 <- feols(fml = ltrade ~ .[ctrls] | year, data = df,weights = ~lrgdp,vcov = cluster ~ pairid)
  m10 <- tobit(formula = frml, data = df_tobit)
  m11 <- feols(fml = ltrade ~ .[ctrls] + l(ltrade, 1) + i(year),data = df, panel.id = ~pairid + year,vcov = cluster ~ pairid)

  tab6_models <- list("With quadratic gravity terms" = m1, "Without year effects" = m2,"Disaggregated regional trade agreements"=m3,"Random-effects (GLS) estimator" = m4, "Fixed-effects (within) estimator" = m5,"Random-effects (GLS) estimator with years" = m6, "Fixed-effects (within) estimator with years"=m7,"Median regression"=m8,"Weighted least squares"=m9,"Tobit"=m10,"With lagged dependent variable"=m11)
  saveRDS(tab6_models, file = produces)
}

df <- fread(file = depends_on)
df_tobit <- df[ltrade <= quantile(ltrade, .05), ltrade := 0]
ctrls <- c(
  "ldist", "lrgdp", "lrgdppc", "comlang", "border", "landl", "island",
  "lareap", "comcol", "curcol", "colony", "comctry", "custrict",
  "regional", "bothin", "onein", "gsp"
)
frml = as.formula(ltrade ~ ldist + lrgdp + lrgdppc + comlang + border + landl + island + lareap + comcol + curcol + colony + comctry + custrict + regional + bothin + onein + gsp)

tab6_est_models(data = df, controls = ctrls)

# create_table6 <- function(models) {
#   tab6_tex <- modelsummary(models, fmt = 2,vcov = NULL, gof_map = NA, coef_map = c("bothin","onein","gsp"), group = model ~ term, output = "latex")
#   save_kable(tab6_tex, file = produces)
# }

# create_table6(models = tab6_models)
