"""Function creates Worldbank region and income classification."""
import country_converter as coco
import pandas as pd

cc = coco.CountryConverter()


def get_wb_classification(wb_classification, least_developed):
    """Get World Bank classification data for countries and add dummy variables for
    region and income group.

    Args:
        wb_classification (pd.DataFrame): Dataframe containing World Bank classification data.
        least_developed (pd.DataFrame): Dataframe containing list of least developed countries.

    Returns:
        pds.DataFrame: Dataframe with World Bank classification data and dummy variables for region and income group.

    """
    wb_classification["Country"] = cc.pandas_convert(
        series=wb_classification["Country"],
        to="name_short",
    )

    wb_classification["ISO3"] = cc.pandas_convert(
        series=wb_classification["Country"],
        to="ISO3",
    )

    least_developed["country"] = cc.pandas_convert(
        series=least_developed["country"],
        to="name_short",
    )

    least_developed["ISO3"] = cc.pandas_convert(
        series=least_developed["country"],
        to="ISO3",
    )

    wb_classification = wb_classification[["Country", "ISO3", "Income group", "Region"]]

    region_dummies = pd.get_dummies(wb_classification["Region"])

    income_dummies = pd.get_dummies(wb_classification["Income group"])

    wb_classification["least"] = 0
    wb_classification.loc[
        wb_classification["Country"].isin(least_developed["country"]),
        "least",
    ] = 1

    wb_classification = pd.concat(
        [wb_classification, region_dummies, income_dummies],
        axis=1,
    )

    wb_classification.reset_index()
    return wb_classification
