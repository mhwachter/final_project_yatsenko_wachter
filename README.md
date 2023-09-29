# Replication of Rose (2004)

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/mhwachter/replication_ppr/main.svg)](https://results.pre-commit.ci/latest/github/mhwachter/replication_ppr/main)
[![image](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Authors

- Anzhelika Yatsenko
- Marcel Harald Wachter

## Description

This repository contains our final project for the course *Effective Programming Practices for Economists* held in the winter semester 2022/23 at the University of Bonn as part of our master's program in Economics. The project replicates the paper Rose, A. K. (2004). Do We Really Know That the WTO
Increases Trade? *American Economic Review*, *94*(1), 98–114.
https://www.doi.org/10.1257/000282804322970724.

No replication code and only the final dataset was available on the website of the
journal. First, we tried to replicate the results with the available final dataset.
Second, we tried to source as much data as possible from the original sources and tried
to replicate it that way. The following data is used:

- International Monetary Fund: Direction of Trade Statistics
- Central Intelligence Agency: World Factbook
- World Bank: World Development Indivators
- Bureau of Labor Statistics: Consumer Price Index

The projects creates a final document called `replication_ppr.pdf` with all regression
tables we were able to replicate. Because the analysis of the original paper was
conducted with Stata and ours was primarily done with R, the results can vary a bit
(especially since it involves unbalanced panel data). The paper contains two sections:
"1 Original Data" with the results we obtained from using the original dataset, and "2
Sourced Data" with the results obtained from our own data.

## Requirements

To run this project working versions of the following dependencies have to be present:

- Conda (https://docs.conda.io/projects/conda/en/stable/user-guide/install/index.html)
- LaTeX (https://www.tug.org/texlive/)
- Git (https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- Firefox (https://www.mozilla.org/en-US/firefox/new/)
- R (https://www.r-project.org)

In addition, the following R Packages are required:

- jsonlite
- data.table
- fixest
- plm
- AER
- quantreg
- modelsummary
- kableExtra

You can install them via the following command in R:

```R
if (!require("pacman")) install.packages("pacman")
pacman::p_load(jsonlite, data.table, fixest, plm, AER, quantreg, modelsummary, kableExtra)
```

## Usage

To get started, in a terminal navigate to the location you would like to save the
project in. Then, clone the repository

```console
git clone https://github.com/mhwachter/final_project_yatsenko_wachter
```

navigate to the root directory of the project and create and activate the environment
with

```console
conda env create -f environment.yml
```

```console
conda activate replication_ppr
```

To build the project, type

```console
pytask
```

### Notes

The project has been tested on macOS Ventura 13.3.

## Project Structure

The `src` directory contains all files needed for the replication and is organised as
follows:

- `data_management`: Contains all files for creating the dataset sourced on our own.
- `data`: Contains all datasets that have to be downloaded manually.
- `analysis`: Contains the R Scripts for running the regressions and estimating the
  models.
- `final`: Creates the LaTeX output for all regression tables.

## Credits

This project was created with [cookiecutter](https://github.com/audreyr/cookiecutter)
and the
[econ-project-templates](https://github.com/OpenSourceEconomics/econ-project-templates).
