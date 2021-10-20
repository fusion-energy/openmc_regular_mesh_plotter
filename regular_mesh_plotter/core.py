import trimesh
import matplotlib.pyplot as plt
from matplotlib import transforms
from typing import List, Optional
import numpy as np
from pathlib import Path

def plot_geometry_mesh(
    mesh_file_or_trimesh_object,
    plane_origin: List[float] = None,
    plane_normal: List[float] = [0, 0, 1],
    rotate_plot: float = 0,
    filename: Optional[str] = None,
) -> plt:
    """Slices through a 3D geometry in STL file format and extracts a slice of
    the geometry at the provided plane and origin

    Args:
        plane_origin: the origin of the plain, if None then the mesh.centroid
            will be used.
        plane_normal: the plane to slice the geometry on. Defaults to slicing
         along the Z plane which is input as [0, 0, 1].
        rotate_plot: the angle in degrees to rotate the plot by. Useful when
            used in conjunction with changing plane_normal to orientate the
            plot correctly.

    Return:
        A matplotlib.pyplot object
    """

    if isinstance(mesh_file_or_trimesh_object, str):
        if not Path(mesh_file_or_trimesh_object).is_file():
            raise FileNotFoundError(f'file {mesh_file_or_trimesh_object} not found.')
        mesh = trimesh.load_mesh(mesh_file_or_trimesh_object, process=False)
    else:
        mesh = mesh_file_or_trimesh_object

    if plane_origin is None:
        plane_origin = mesh.centroid
    slice = mesh.section(
        plane_origin=plane_origin,
        plane_normal=plane_normal,
    )

    slice_2D, to_3D = slice.to_planar()

    # keep plot axis scaled the same
    plt.axes().set_aspect("equal", "datalim")

    if rotate_plot != 0:
        base = plt.gca().transData
        rot = transforms.Affine2D().rotate_deg(rotate_plot)

    for entity in slice_2D.entities:

        discrete = entity.discrete(slice_2D.vertices)

        if rotate_plot != 0:
            plt.plot(*discrete.T, color="black", linewidth=1, transform=rot + base)
        else:
            plt.plot(*discrete.T, color="black", linewidth=1)

    if filename:
        plt.savefig(filename, dpi=300)
    return plt


def plot_regular_mesh_values(
    values: np.ndarray,
    filename: Optional[str] = None,
    scale=None,  # LogNorm(),
    vmin=None,
    label="",
    base_plt=None,
    extent=None,
    x_label='X [cm]',
    y_label='Y [cm]',
):

    if base_plt:
        plt = base_plt
    else:
        import matplotlib.pyplot as plt
        plt.plot()
    image_map = plt.imshow(
        values,
        norm=scale,
        vmin=vmin,
        extent=extent
    )

    plt.xlabel(x_label)
    plt.ylabel(y_label)

    # image_map = fig.imshow(values, norm=scale, vmin=vmin)
    plt.colorbar(image_map, label=label)
    if filename:
        plt.savefig(filename, dpi=300)
    # fig.clear()
    # plt.close()
    return plt

def plot_regular_mesh_values_with_geometry(
    values: np.ndarray,
    mesh_file_or_trimesh_object,
    filename: Optional[str] = None,
    scale=None,  # LogNorm(),
    vmin=None,
    label="",
    extent=None,
    x_label='X [cm]',
    y_label='Y [cm]',
    plane_origin: List[float] = None,
    plane_normal: List[float] = [0, 0, 1],
    rotate_plot: float = 0,
):
    slice = plot_geometry_mesh(
        mesh_file_or_trimesh_object=mesh_file_or_trimesh_object,
        plane_origin = plane_origin,
        plane_normal = plane_normal,
        rotate_plot = rotate_plot
    )

    both = plot_regular_mesh_values(
        values = values,
        filename = filename,
        scale=scale,  # LogNorm(),
        vmin=vmin,
        label=label,
        base_plt=slice,
        extent=extent,
        x_label=x_label,
        y_label=y_label,
    )

    return both

def plot_regular_mesh_tally(
    tally: np.ndarray,
    filename: Optional[str] = None,
    scale=None,  # LogNorm(),
    vmin=None,
    label="",
    base_plt=None,
    x_label='X [cm]',
    y_label='Y [cm]',
):

    if base_plt:
        plt = base_plt
    else:
        import matplotlib.pyplot as plt
        plt.plot()

    import openmc_post_processor as opp
    values = statepoint.process_tally(
        tally=my_tally_1,
    )

    extent = get_tally_extent(tally)

    image_map = plt.imshow(
        values,
        norm=scale,
        vmin=vmin,
        extent=extent
    )

    plt.xlabel(x_label)
    plt.ylabel(y_label)

    # image_map = fig.imshow(values, norm=scale, vmin=vmin)
    plt.colorbar(image_map, label=label)
    if filename:
        plt.savefig(filename, dpi=300)
    # fig.clear()
    # plt.close()
    return plt

def get_tally_extent(
    tally,
):
    import openmc
    for filter in tally.filters:
        if isinstance(filter, openmc.MeshFilter):
            mesh_filter = filter
            # print(mesh_filter)
            # print(mesh_filter.mesh.lower_left)
            # print(mesh_filter.mesh.upper_right)
            # print(mesh_filter.mesh.width)
            # print(mesh_filter.mesh.__dict__)
            # print(mesh_filter.mesh.dimension)

    extent_x = (min(mesh_filter.mesh.lower_left[0],mesh_filter.mesh.upper_right[0]), max(mesh_filter.mesh.lower_left[0],mesh_filter.mesh.upper_right[0]))
    extent_y = (min(mesh_filter.mesh.lower_left[1],mesh_filter.mesh.upper_right[1]), max(mesh_filter.mesh.lower_left[1],mesh_filter.mesh.upper_right[1]))
    extent_z = (min(mesh_filter.mesh.lower_left[2],mesh_filter.mesh.upper_right[2]), max(mesh_filter.mesh.lower_left[2],mesh_filter.mesh.upper_right[2]))
    
    if 1 in mesh_filter.mesh.dimension.tolist():
        print('2d mesh tally')
        index_of_1d = mesh_filter.mesh.dimension.tolist().index(1)
        print('index', index_of_1d)
        if index_of_1d == 0:
            return extent_y + extent_z
        if index_of_1d == 1:
            return extent_x + extent_z
        if index_of_1d == 2:
            return extent_x + extent_y
    return None
