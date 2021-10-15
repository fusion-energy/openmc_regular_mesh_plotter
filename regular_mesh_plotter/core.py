import trimesh
import matplotlib.pyplot as plt
from matplotlib import transforms
from typing import List, Optional
import numpy as np


def plot_stl_slice(
    stl_or_mesh,
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

    if isinstance(stl_or_mesh, str):
        mesh = trimesh.load_mesh(stl_or_mesh, process=False)
    else:
        mesh = stl_or_mesh

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


def plot_mesh(
    values: np.ndarray,
    filename: Optional[str] = None,
    scale=None,  # LogNorm(),
    vmin=None,
    label="",
    base_plt=None
):

    if base_plt:
        pass
    else:
        fig = plt.subplot()
    image_map = fig.imshow(values, norm=scale, vmin=vmin)
    plt.colorbar(image_map, label=label)
    if filename:
        plt.savefig(filename, dpi=300)
    # fig.clear()
    # plt.close()
    return fig
