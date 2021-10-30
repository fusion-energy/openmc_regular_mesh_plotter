import trimesh
import matplotlib.pyplot as plt
from matplotlib import transforms
from typing import List, Optional, Tuple
import numpy as np
from pathlib import Path
import dagmc_geometry_slice_plotter as dgsp
from matplotlib import transforms

import openmc_post_processor as opp
import openmc


def plot_regular_mesh_values(
    values: np.ndarray,
    filename: Optional[str] = None,
    scale=None,  # LogNorm(),
    vmin=None,
    label="",
    base_plt=None,
    extent=None,
    x_label="X [cm]",
    y_label="Y [cm]",
    rotate_plot: float = 0,
):

    if base_plt:
        plt = base_plt
    else:
        import matplotlib.pyplot as plt

        plt.plot()

    if rotate_plot != 0:
        x_center = sum(extent[:2]) / 2
        y_center = sum(extent[2:]) / 2
        base = plt.gca().transData
        rot = transforms.Affine2D().rotate_deg_around(x_center, y_center, rotate_plot)

        image_map = plt.imshow(
            values, norm=scale, vmin=vmin, extent=extent, transform=rot + base
        )
    else:
        image_map = plt.imshow(values, norm=scale, vmin=vmin, extent=extent)

    plt.xlabel(x_label)
    plt.ylabel(y_label)

    # image_map = fig.imshow(values, norm=scale, vmin=vmin)
    plt.colorbar(image_map, label=label)
    if filename:
        plt.savefig(filename, dpi=300)
    return plt


def plot_regular_mesh_values_with_geometry(
    values: np.ndarray,
    dagmc_file_or_trimesh_object,
    filename: Optional[str] = None,
    scale=None,  # LogNorm(),
    vmin=None,
    label="",
    extent=None,
    x_label="X [cm]",
    y_label="Y [cm]",
    plane_origin: List[float] = None,
    plane_normal: List[float] = [0, 0, 1],
    rotate_mesh: float = 0,
    rotate_geometry: float = 0,
):

    slice = dgsp.plot_slice_of_dagmc_geometry(
        dagmc_file_or_trimesh_object=dagmc_file_or_trimesh_object,
        plane_origin=plane_origin,
        plane_normal=plane_normal,
        rotate_plot=rotate_geometry,
    )

    both = plot_regular_mesh_values(
        values=values,
        filename=filename,
        scale=scale,  # LogNorm(),
        vmin=vmin,
        label=label,
        base_plt=slice,
        extent=extent,
        x_label=x_label,
        y_label=y_label,
        rotate_plot=rotate_mesh,
    )

    return both

def get_values_from_tally(tally):
    data_frame = tally.get_pandas_dataframe()
    if "std. dev." in data_frame.columns.to_list():
        values = (
            np.array(data_frame["mean"]),
            np.array(data_frame["std. dev."])
        )
    else:
        values = (
            np.array(data_frame["mean"])
        )
    return values

def get_std_dev_or_value_from_tally(tally, values, std_dev_or_tally_value):

    if std_dev_or_tally_value == 'std_dev':
        value = reshape_values_to_mesh_shape(tally, values[1])
    elif std_dev_or_tally_value == 'tally_value':
        if isinstance(values, np.ndarray):
            value = reshape_values_to_mesh_shape(tally, values)
        elif isinstance(values, tuple):
            value = reshape_values_to_mesh_shape(tally, values[0])
        else:
            msg = f'Values to plot should be a numpy ndarry or a tuple or numpy ndarrys not a {type(values)}'
            raise ValueError(msg)
    else:
        msg = f'Value of std_dev_or_tally_value should be either "std_dev" or "value", not {type(values)}'
        raise ValueError(msg)
    
    return value

def plot_regular_mesh_tally_with_geometry(
    tally,
    dagmc_file_or_trimesh_object,
    std_dev_or_tally_value='tally_value',
    filename: Optional[str] = None,
    scale=None,  # LogNorm(),
    vmin=None,
    label="",
    x_label="X [cm]",
    y_label="Y [cm]",
    plane_origin: List[float] = None,
    plane_normal: List[float] = [0, 0, 1],
    rotate_mesh: float = 0,
    rotate_geometry: float = 0,
    required_units=None,
    source_strength: float = None
):

    if required_units is not None:
        values = opp.process_tally(
            tally=tally,
            required_units=required_units,
            source_strength=source_strength
        )
    else:
        values = get_values_from_tally(tally)
    
    value = get_std_dev_or_value_from_tally(tally, values, std_dev_or_tally_value)

    extent = get_tally_extent(tally)

    base_plt = dgsp.plot_slice_of_dagmc_geometry(
        dagmc_file_or_trimesh_object=dagmc_file_or_trimesh_object,
        plane_origin=plane_origin,
        plane_normal=plane_normal,
        rotate_plot=rotate_geometry,
    )

    plot = plot_regular_mesh_values(
        values=value,
        filename=filename,
        scale=scale,
        vmin=vmin,
        label=label,
        base_plt=base_plt,
        extent=extent,
        x_label=x_label,
        y_label=y_label,
        rotate_plot=rotate_mesh,
    )

    return plot



def plot_regular_mesh_tally(
    tally,
    filename: Optional[str] = None,
    scale=None,  # LogNorm(),
    vmin=None,
    label="",
    base_plt=None,
    x_label="X [cm]",
    y_label="Y [cm]",
    rotate_plot: float = 0,
    required_units: str = None,
    source_strength: float = None,
):

    if required_units is not None:
        values = opp.process_tally(
            tally=tally,
            required_units=required_units,
            source_strength=source_strength
        )
    else:
        values = get_values_from_tally(tally)

    values = reshape_values_to_mesh_shape(tally, values)

    extent = get_tally_extent(tally)

    plot = plot_regular_mesh_values(
        values=values[0],
        filename=filename,
        scale=scale,
        vmin=vmin,
        label=label,
        base_plt=base_plt,
        extent=extent,
        x_label=x_label,
        y_label=y_label,
        rotate_plot=rotate_plot,
    )

    return plot


def plot_regular_mesh_dose_tally(
    tally,
    filename: Optional[str] = None,
    scale=None,  # LogNorm(),
    vmin=None,
    label="",
    base_plt=None,
    x_label="X [cm]",
    y_label="Y [cm]",
    rotate_plot: float = 0,
    required_units='picosievert cm **2 / simulated_particle',
    source_strength: float = None,
):

    if required_units is not None:
        values = opp.process_dose_tally(
            tally=tally,
            required_units=required_units,
            source_strength=source_strength
        )
    else:
        values = get_values_from_tally(tally)

    values = reshape_values_to_mesh_shape(tally, values)

    extent = get_tally_extent(tally)

    if len
    plot = plot_regular_mesh_values(
        values=values[0],
        filename=filename,
        scale=scale,
        vmin=vmin,
        label=label,
        base_plt=base_plt,
        extent=extent,
        x_label=x_label,
        y_label=y_label,
        rotate_plot=rotate_plot,
    )

    return plot


def plot_regular_mesh_dose_tally_with_geometry(
    tally,
    dagmc_file_or_trimesh_object,
    filename: Optional[str] = None,
    scale=None,  # LogNorm(),
    vmin=None,
    label="",
    x_label="X [cm]",
    y_label="Y [cm]",
    plane_origin: List[float] = None,
    plane_normal: List[float] = [0, 0, 1],
    rotate_mesh: float = 0,
    rotate_geometry: float = 0,
    required_units='picosievert cm **2 / simulated_particle',
    source_strength: float = None,
):

    slice = dgsp.plot_slice_of_dagmc_geometry(
        dagmc_file_or_trimesh_object=dagmc_file_or_trimesh_object,
        plane_origin=plane_origin,
        plane_normal=plane_normal,
        rotate_plot=rotate_geometry,
    )

    both = plot_regular_mesh_dose_tally(
        tally=tally,
        filename=filename,
        scale=scale,  # LogNorm(),
        vmin=vmin,
        label=label,
        base_plt=slice,
        x_label=x_label,
        y_label=y_label,
        rotate_plot=rotate_mesh,
        required_units=required_units,
        source_strength=source_strength
    )

    return both


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
            # print(mesh_filter)
            # print(mesh_filter.mesh.lower_left)
            # print(mesh_filter.mesh.upper_right)
            # print(mesh_filter.mesh.width)
            # print(mesh_filter.mesh.__dict__)
            # print(mesh_filter.mesh.dimension)

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
