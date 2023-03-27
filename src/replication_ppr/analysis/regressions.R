rm(list = ls())

library(plm)
library(nlme)
library(gmnl)
library(fixest)
library(data.table)
library(lme4)
library(modelsummary)
library(quantreg)
library(AER)
library(pdynmc)
library(kableExtra)

df <- fread(file = "/Users/marcel/Desktop/df.csv")

ctrls <- c(
  "ldist", "lrgdp", "lrgdppc", "comlang", "border", "landl", "island",
  "lareap", "comcol", "curcol", "colony", "comctry", "custrict",
  "regional", "bothin", "onein", "gsp"
)
ctrls_tab8 <- c(
  "ldist", "lrgdp", "lrgdppc", "comlang", "border", "landl", "island",
  "lareap", "comcol", "curcol", "colony", "comctry", "custrict",
  "regional", "gsp"
)
ctrls_tab3 <- c(
  "ldist", "lrgdp", "lrgdppc", "comlang", "border", "landl", "island",
  "lareap", "comcol", "curcol", "colony", "comctry", "custrict",
  "regional", "gsp"
)

frml <- as.formula(ltrade ~ ldist + lrgdp + lrgdppc + comlang + border + landl + island + lareap + comcol + curcol + colony + comctry + custrict + regional + bothin + onein + gsp)



# Table 1 -----------------------------------------------------------------

tab1 <- list(
  "Default" = feols(fml = ltrade ~ .[ctrls] | year, data = df),
  "No industrial countries" = feols(fml = ltrade ~ .[ctrls] | year, data = df[cty1 >= 200 & cty2 >= 200]),
  "Post 1970" = tab1_3 <- feols(fml = ltrade ~ .[ctrls] | year, data = df[year > 1970]),
  "With country effects" = feols(fml = ltrade ~ .[ctrls] + ..("^cd_") | year, data = df)
)
tab1 <- modelsummary(tab1,
  fmt = 2, vcov = ~pairid,
  coef_map = c(
    "bothin", "onein", "gsp", "ldist", "lrgdp", "lrgdppc", "regional",
    "custrict", "comlang", "border", "landlocked",
    "island", "lareap", "comcol", "curcol", "colony", "comctry"
  ),
  gof_map = c("nobs", "r.squared", "rmse"), output = "latex",
  title = "Benchmark Results"
)

# Table2 ------------------------------------------------------------------

tab2 <- feols(
  fml = ltrade ~ .[ctrls] | year, data = df,
  split = ~ year %keep% c(
    "1950", "1955", "1960", "1965", "1970", "1975", "1980",
    "1985", "1990", "1995"
  )
)
tab2 <- modelsummary(tab2,
  fmt = 2, vcov = ~pairid, gof_map = "none",
  coef_map = c("bothin", "onein", "gsp"), group = model ~ term,
  output = "latex", title = "Cross-Sectional Analysis"
)

# Table 3 -----------------------------------------------------------------

df$periods <- cut(df$year,
  breaks = c(1948, 1949, 1951, 1956, 1961, 1967, 1979, 1994, 2000),
  labels = c(
    "Before Annecy round (1949)",
    "Annecy to Torquay round (1951)",
    "Torquay to Geneva round (1956)",
    "Geneva to Dillon round (1961)",
    "Dillon to Kennedy round (1967)",
    "Kennedy to Tokyo round (1979)",
    "Tokyo to Uruguay round (1994)",
    "After Uruguay round"
  ), include.lowest = TRUE, right = FALSE
)
tab3 <- list(
  "OLS year effects" = feols(fml = ltrade ~ .[ctrls_tab3] + bothin:periods + onein:periods | year, data = df),
  "Fixed country-pair effects" = feols(fml = ltrade ~ .[ctrls_tab3] + bothin:periods + onein:periods | pairid, data = df)
)

tab3 <- modelsummary(tab3,
  fmt = 2, vcov = ~pairid, gof_map = "none",
  coef_omit = "^(?!.*bothin|.*onein)", coef_rename = TRUE,
  output = "latex",
  title = "Allowing the Effects to Vary Over GATT Rounds"
)

# Table 4 -----------------------------------------------------------------
tab4 <- list(
  "Default" = feols(fml = ltrade ~ .[ctrls] | year, data = df),
  "South Asia" = feols(
    fml = ltrade ~ .[ctrls] | year,
    data = df[sasia1 == 1 | sasia2 == 1]
  ),
  "East Asia" = feols(
    fml = ltrade ~ .[ctrls] | year,
    data = df[easia1 == 1 | easia2 == 1]
  ),
  "Sub-Saharan Africa" = feols(
    fml = ltrade ~ .[ctrls] | year,
    data = df[ssafr1 == 1 | ssafr2 == 1]
  ),
  "Middle East or North Africa" = feols(
    fml = ltrade ~ .[ctrls] | year,
    data = df[menaf1 == 1 | menaf2 == 1]
  ),
  "Latin America or Caribbean" = feols(
    fml = ltrade ~ .[ctrls] | year,
    data = df[latca1 == 1 | latca2 == 1]
  ),
  "High income" = feols(
    fml = ltrade ~ .[ctrls] | year,
    data = df[highi1 == 1 | highi2 == 1]
  ),
  "Middle income" = feols(
    fml = ltrade ~ .[ctrls] | year,
    data = df[midin1 == 1 | midin2 == 1]
  ),
  "Low income" = feols(
    fml = ltrade ~ .[ctrls] | year,
    data = df[lowin1 == 1 | lowin2 == 1]
  ),
  "Least developed" = feols(
    fml = ltrade ~ .[ctrls] | year,
    data = df[least1 == 1 | least2 == 1]
  )
)
tab4 <- modelsummary(tab4,
  fmt = 2, vcov = ~pairid, gof_map = "none",
  coef_map = c("bothin", "onein", "gsp"), group = model ~ term,
  output = "latex", title = "Allowing the Effects to Vary by Region and Income Class"
)
# Table 5 -----------------------------------------------------------------
opec <- c(429, 433, 443, 456, 299, 453, 536, 672, 466, 612, 694, 248, 646)
df <- df[order(lrgdp), quartile_lrgdp := floor(1 + 4 * (.I - 1) / .N)]
df <- df[order(lrgdppc), quartile_lrgdppc := floor(1 + 4 * (.I - 1) / .N)]
mod <- feols(fml = ltrade ~ .[ctrls] | year, data = df)
df$residuals <- mod$residuals
sd3 <- 3 * sd(resid(mod))
df$outliers <- 0
df[abs(residuals) > sd3, outliers := 1]
tab5 <- list(
  "Data before 1980" = feols(fml = ltrade ~ .[ctrls] | year, data = df[year < 1980]),
  "Data after 1979" = feols(fml = ltrade ~ .[ctrls] | year, data = df[year > 1979]),
  "Only industrial countries" = feols(
    fml = ltrade ~ .[ctrls] | year,
    data = df[cty1 < 200 & cty2 < 200]
  ),
  "No African countries" = feols(
    fml = ltrade ~ .[ctrls] | year,
    data = df[ssafr1 == 0 & ssafr2 == 0 & menaf1 == 0 & menaf2 == 0]
  ),
  "No Latin or Caribbean countries" = feols(
    fml = ltrade ~ .[ctrls] | year,
    data = df[latca1 == 0 & latca2 == 0]
  ),
  "No OPEC countries" = feols(
    fml = ltrade ~ .[ctrls] | year,
    data = df[!(cty1 %in% opec) & !(cty2 %in% opec)]
  ),
  "No RTA observations" = feols(
    fml = ltrade ~ .[ctrls] | year,
    data = df[regional == 0]
  ),
  "Without poorest quartile of real GDP p/c" = feols(
    fml = ltrade ~ .[ctrls] | year,
    data = df[quartile_lrgdppc != 1]
  ),
  "Without smallest quartile of real GDP" = feols(
    fml = ltrade ~ .[ctrls] | year,
    data = df[quartile_lrgdp != 1]
  ),
  "Without 3sd outliers" = feols(
    fml = ltrade ~ .[ctrls] | year,
    data = df[outliers != 1]
  ),
  "Only Canadian observations" = feols(
    fml = ltrade ~ .[ctrls] | year,
    data = df[cty1 == 156 | cty2 == 156]
  ),
  "Only American observations" = feols(
    fml = ltrade ~ .[ctrls] | year,
    data = df[cty1 == 111 | cty2 == 111]
  ),
  "Only British observations" = feols(
    fml = ltrade ~ .[ctrls] | year,
    data = df[cty1 == 112 | cty2 == 112]
  ),
  "Only French observations" = feols(
    fml = ltrade ~ .[ctrls] | year,
    data = df[cty1 == 132 | cty2 == 132]
  ),
  "Only Italian observations" = feols(
    fml = ltrade ~ .[ctrls] | year,
    data = df[cty1 == 136 | cty2 == 136]
  ),
  "Only German observations" = feols(
    fml = ltrade ~ .[ctrls] | year,
    data = df[cty1 == 134 | cty2 == 134]
  ),
  "Only Japanese observations" = feols(
    fml = ltrade ~ .[ctrls] | year,
    data = df[cty1 == 158 | cty2 == 158]
  )
)
tab5 <- modelsummary(tab5,
  fmt = 2, vcov = ~pairid, gof_map = "none",
  coef_map = c("bothin", "onein", "gsp"), group = model ~ term,
  output = "latex", title = "Sample Sensitvity Analysis"
)

# Table 6 -----------------------------------------------------------------
# df_tobit <- df[ltrade <= quantile(ltrade, .05), ltrade := 0]
# tab6 <- list(
#   #"With quadratic gravity terms" = feols(fml = ltrade ~ .[ctrls] | year, data = df),
#   "Without year effects" = feols(fml = ltrade ~ .[ctrls], data = df),
#   #"Disaggregated regional trade agreements"
#   #"Controlling for aggregate thirdcountry trade"
#   #"5-year averages"
#   "Random-effects (GLS) estimator"= plm(formula = frml, data = df,
#                                         effect = "individual", model = "random",
#                                         index = "pairid"),
#   "Fixed-effects (within) estimator" = feols(fml = ltrade ~ .[ctrls] | pairid,
#                                              data = df),
#   "Random-effects (GLS) estimator with years" = plm(formula = frml, data = df,
#                                                     effect = "twoways",
#                                                     model = "random",
#                                                     index = c("pairid","year")),
#   "Fixed-effects (within) estimator with years" = feols(fml = ltrade ~ .[ctrls] | pairid + year,
#                                                         data = df),
#   #"Treatment MLE: Both members vs. neither"
#   #"Treatment MLE: One member vs. neither"
#   "Median regression" = rq(formula = frml, tau = 0.5, data = df),
#   "Weighted least squares" = feols(fml = ltrade ~ .[ctrls] | year, data = df,
#                                    weights = ~lrgdp),
#   "Tobit" = tobit(formula = frml, data = df_tobit),
#   "With lagged dependent variable" = feols(fml = ltrade ~ .[ctrls] + l(ltrade, 1) + i(year),
#                                            data = df, panel.id = ~pairid + year),
#   #"Arellano-Bond dynamic panel" = pdynmc(dat = df, varname.i = "pairid", varname.t = "year",use.mc.diff = TRUE, use.mc.lev = FALSE, use.mc.nonlin = FALSE, include.y = TRUE, varname.y = "ltrade", lagTerms.y = 1, include.x = TRUE, varname.reg.end = ctrls)
# )
# tab6 <- list(
#   "Without year effects" = feols(fml = ltrade ~ .[ctrls], data = df),
#   "Random-effects (GLS) estimator"= plm(formula = frml, data = df,
#                                         effect = "individual", model = "random",
#                                         index = "pairid"),
#   "Fixed-effects (within) estimator" = feols(fml = ltrade ~ .[ctrls] | pairid,
#                                              data = df),
#   "Random-effects (GLS) estimator with years" = plm(formula = frml, data = df,
#                                                     effect = "twoways",
#                                                     model = "random",
#                                                     index = c("pairid","year")),
#   "Fixed-effects (within) estimator with years" = feols(fml = ltrade ~ .[ctrls] | pairid + year,
#                                                         data = df),
#   "Median regression" = rq(formula = frml, tau = 0.5, data = df),
#   "Weighted least squares" = feols(fml = ltrade ~ .[ctrls] | year, data = df,
#                                    weights = ~lrgdp),
#   "Tobit" = tobit(formula = frml, data = df_tobit),
#   "With lagged dependent variable" = feols(fml = ltrade ~ .[ctrls] + l(ltrade, 1) + i(year),
#                                            data = df, panel.id = ~pairid + year)
# )
# modelsummary(tab6, fmt = 2, vcov = NULL, gof_map = NA, coef_map = c("bothin","onein","gsp"), group = model ~ term)
#
# feols1 <- feols(fml = ltrade ~ .[ctrls], data = df)
# plm1 <- plm(formula = frml, data = df,effect = "individual", model = "random",index = "pairid")
# feols2 <- feols(fml = ltrade ~ .[ctrls] | pairid,data = df)
# plm2 <- plm(formula = frml, data = df,effect = "twoways",model = "random",index = c("pairid","year"))
# rq <- rq(formula = frml, tau = 0.5, data = df)
# feols3 <- feols(fml = ltrade ~ .[ctrls] + i(year), data = df, weights = ~lrgdp)
# tobit <- tobit(formula = frml, data = df_tobit)
# feols4 <- feols(fml = ltrade ~ .[ctrls] + l(ltrade, 1) + i(year),data = df, panel.id = ~pairid + year)
# modelsummary(list(feols1,plm1,feols2,plm2,feols3,tobit,feols4), fmt = 2, vcov = NULL, gof_map = NA, coef_map = c("bothin","onein","gsp"), group = model ~ term)
# modelsummary(rq, fmt = 2, vcov = NULL, gof_map = NA, coef_map = c("bothin","onein","gsp"), group = model ~ term)

# Table 7 -----------------------------------------------------------------
# df$join5 <- 0
# df$join10 <- 0
# df$join15 <- 0
# df$join20 <- 0
# df[years1 >= 5 | years2 >= 5, join_5 := 1]
# df[years1 >= 10 | years2 >= 10, join_10 := 1]
# df[years1 >= 15 | years2 >= 15, join_15 := 1]
# df[years1 >= 20 | years2 >= 20, join_20 := 1]
#
#
# feols(fml = ltrade ~ .[ctrls] + join5 + join10 + join15 + join20 + i(year), data = df)


# Table 8 -----------------------------------------------------------------

tab8 <- list(
  feols(fml = ltrade ~ .[ctrls] | year, data = df),
  feols(fml = ltrade ~ bothin + onein + gsp + ldist + lrgdp + lrgdppc | year, data = df),
  feols(fml = ltrade ~ bothin + onein + gsp | year, data = df),
  feols(fml = ltrade ~ .[ctrls_tab8] + found1 + found2 + minyrs + maxyrs | year, data = df)
)
tab8 <- modelsummary(tab8,
  fmt = 2, vcov = ~pairid, gof_map = c("r.squared", "rmse"),
  coef_map = c(
    "bothin", "onein", "gsp", "found1", "found2", "minyrs",
    "maxyrs", "ldist", "lrgdp", "lrgdppc", "regional", "custrict",
    "comlang", "border", "landlocked", "island", "lareap", "comcol",
    "curcol", "colony", "comctry"
  ), output = "latex",
  title = "Perturbations of the Gravity Model"
)


tab3 <- tab3 %>% kable_styling(latex_options = "scale_down")
save_kable(tab1, file = "/Users/marcel/Desktop/tab1.tex")
save_kable(tab2, file = "/Users/marcel/Desktop/tab2.tex")
save_kable(tab3, file = "/Users/marcel/Desktop/tab3.tex")
save_kable(tab4, file = "/Users/marcel/Desktop/tab4.tex")
save_kable(tab5, file = "/Users/marcel/Desktop/tab5.tex")
save_kable(tab8, file = "/Users/marcel/Desktop/tab8.tex")
