"""Tasks for getting the distance data."""

import pandas as pd
import pytask
from replication_ppr.config import BLD
from replication_ppr.data_management.distance_calculation import (
    calculate_distance,
    create_distance_data,
    distance_data_cleaning,
    get_coordinates,
)


@pytask.mark.depends_on(
    {
        "cia_factbook": BLD / "python" / "data" / "cia_factbook.csv",
    },
)
@pytask.mark.produces(
    {
        "coordinates": BLD / "python" / "data" / "coordinates.csv",
    },
)
def task_coordinates(depends_on, produces):
    cia_factbook = pd.read_csv(depends_on["cia_factbook"])
    coordinates = get_coordinates(data=cia_factbook)
    coordinates.to_csv(produces["coordinates"])


@pytask.mark.depends_on(
    {
        "coordinates": BLD / "python" / "data" / "coordinates.csv",
    },
)
@pytask.mark.produces(
    {
        "distance_data": BLD / "python" / "data" / "distance_final.csv",
    },
)
def task_distance_calculation(depends_on, produces):
    coordinates = pd.read_csv(depends_on["coordinates"])
    distances = calculate_distance(data=coordinates)
    distances = create_distance_data(data=distances)
    distances = distance_data_cleaning(data=distances)
    distances.to_csv(produces["distance_data"])
