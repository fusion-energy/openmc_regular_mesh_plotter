from pathlib import Path
from typing import List, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
import openmc
import pandas as pd


def reshape_values_to_mesh_shape(tally, values):
    tally_filter = tally.find_filter(filter_type=openmc.MeshFilter)
    shape = tally_filter.mesh.dimension.tolist()
    # 2d mesh has a shape in the form [1, 400, 400]
    if 1 in shape:
        shape.remove(1)
    return values.reshape(shape)


def get_tally_extent(
    tally,
):

    for filter in tally.filters:
        if isinstance(filter, openmc.MeshFilter):
            mesh_filter = filter

    extent_x = (
        min(mesh_filter.mesh.lower_left[0], mesh_filter.mesh.upper_right[0]),
        max(mesh_filter.mesh.lower_left[0], mesh_filter.mesh.upper_right[0]),
    )
    extent_y = (
        min(mesh_filter.mesh.lower_left[1], mesh_filter.mesh.upper_right[1]),
        max(mesh_filter.mesh.lower_left[1], mesh_filter.mesh.upper_right[1]),
    )
    extent_z = (
        min(mesh_filter.mesh.lower_left[2], mesh_filter.mesh.upper_right[2]),
        max(mesh_filter.mesh.lower_left[2], mesh_filter.mesh.upper_right[2]),
    )

    if 1 in mesh_filter.mesh.dimension.tolist():
        print("2d mesh tally")
        index_of_1d = mesh_filter.mesh.dimension.tolist().index(1)
        print("index", index_of_1d)
        if index_of_1d == 0:
            return extent_y + extent_z
        if index_of_1d == 1:
            return extent_x + extent_z
        if index_of_1d == 2:
            return extent_x + extent_y
    return None


def get_values_from_tally(tally):
    """Return a numpy array of the openmc tally values (mean entry in
    dataframe) and if present the standard deviation (std. dev. in the
    dateframe) is also returned"""

    data_frame = tally.get_pandas_dataframe()
    if "std. dev." in get_data_frame_columns(data_frame):
        values = (np.array(data_frame["mean"]), np.array(data_frame["std. dev."]))
    else:
        values = np.array(data_frame["mean"])
    return values


def get_data_frame_columns(data_frame):
    if isinstance(data_frame.columns, pd.MultiIndex):
        data_frame_columns = data_frame.columns.get_level_values(0).to_list()
    else:
        data_frame_columns = data_frame.columns.to_list()
    return data_frame_columns


def get_std_dev_or_value_from_tally(tally, values, std_dev_or_tally_value):

    if std_dev_or_tally_value == "std_dev":
        value_index = 1
    elif std_dev_or_tally_value == "tally_value":
        value_index = 0
    else:
        msg = f'Value of std_dev_or_tally_value should be either "std_dev" or "value", not {type(values)}'
        raise ValueError(msg)

    if isinstance(values, tuple):
        value = reshape_values_to_mesh_shape(tally, values[value_index])
    elif isinstance(values, np.ndarray):
        value = reshape_values_to_mesh_shape(tally, values)
    else:  # isinstance(values, np.ndarray):
        # a pint unit object
        value = reshape_values_to_mesh_shape(tally, values.magnitude)
        # else:
        #     msg = f'Values to plot should be a numpy ndarry or a tuple or numpy ndarrys not a {type(values)}'
        #     raise ValueError(msg)

    return value
