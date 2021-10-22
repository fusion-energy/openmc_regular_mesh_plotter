import trimesh
import matplotlib.pyplot as plt
from matplotlib import transforms
from typing import List, Optional
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


def plot_regular_mesh_tally_with_geometry(
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
):

    slice = dgsp.plot_slice_of_dagmc_geometry(
        dagmc_file_or_trimesh_object=dagmc_file_or_trimesh_object,
        plane_origin=plane_origin,
        plane_normal=plane_normal,
        rotate_plot=rotate_geometry,
    )

    both = plot_regular_mesh_tally(
        tally=tally,
        filename=filename,
        scale=scale,  # LogNorm(),
        vmin=vmin,
        label=label,
        base_plt=slice,
        x_label=x_label,
        y_label=y_label,
        rotate_plot=rotate_mesh,
    )

    return both


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
):

    values = opp.process_dose_tally(
        tally=tally,
    )

    extent = get_tally_extent(tally)

    plot = plot_regular_mesh_values(
        values=values,
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
