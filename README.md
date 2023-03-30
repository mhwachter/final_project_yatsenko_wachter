# Replication Paper

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/mhwachter/replication_ppr/main.svg)](https://results.pre-commit.ci/latest/github/mhwachter/replication_ppr/main)
[![image](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Authors

Anzhelika Yatsenko & Marcel Harald Wachter

## Description

This project replicates the paper Rose, A. K. (2004). Do We Really Know That the WTO
Increases Trade? *American Economic Review*, *94*(1), 98–114.
https://www.doi.org/10.1257/000282804322970724.

Only the final dataset and no replication code was available on the website of the
journal. The data is sourced from the original sources whenever possible. The following
data is used:

- International Monetary Fund:
- Central Intelligence Agency:
- World Bank:
- Bureau of Labor Statistics:

## Requirements

To run this project the following system requirements need to be fulfilled:

- Conda (https://docs.conda.io/projects/conda/en/stable/user-guide/install/index.html)
- LaTeX (https://www.tug.org/texlive/)

## Usage

To get started, navigate to the folder you would like to save the project in. Then,
clone the repository

```console
$ git clone https://github.com/mhwachter/final_project_yatsenko_wachter
```

navigate to the root directory of the project and create and activate the environment
with

```console
$ conda env create -f environment.yml
$ conda activate replication_ppr
```

To build the project, type

```console
$ pytask
```

## Project Structure

The `src` directory contains all files needed for the replication and is organised as
follows:

- `data_management`
- `data`
- `analysis`
- `final`

## Credits

This project was created with [cookiecutter](https://github.com/audreyr/cookiecutter)
and the
[econ-project-templates](https://github.com/OpenSourceEconomics/econ-project-templates).
