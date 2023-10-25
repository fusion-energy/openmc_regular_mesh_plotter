import math
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Optional
import openmc
import numpy as np
import openmc
import openmc.checkvalue as cv
import matplotlib.pyplot as plt

from packaging import version

if version.parse(openmc.__version__) < version.parse("0.13.3"):
    msg = (
        "openmc_regular_mesh_plotter package requires OpenMC version 0.13.4 "
        f"or newer. You currently have OpenMC version {openmc.__version__}"
    )
    raise ValueError(msg)

_BASES = ["xy", "xz", "yz"]

_default_outline_kwargs = {"colors": "black", "linestyles": "solid", "linewidths": 1}


def plot_mesh_tally(
    tally: "openmc.Tally",
    basis: str = "xy",
    slice_index: Optional[int] = None,
    score: Optional[str] = None,
    axes: Optional[str] = None,
    axis_units: str = "cm",
    value: str = "mean",
    outline: bool = False,
    outline_by: str = "cell",
    geometry: Optional["openmc.Geometry"] = None,
    pixels: int = 40000,
    colorbar: bool = True,
    volume_normalization: bool = True,
    scaling_factor: Optional[float] = None,
    colorbar_kwargs: dict = {},
    outline_kwargs: dict = _default_outline_kwargs,
    **kwargs,
) -> "matplotlib.image.AxesImage":
    """Display a slice plot of the mesh tally score.
    Parameters
    ----------
    tally : openmc.Tally
        The openmc tally to plot. Tally must contain a MeshFilter that uses a RegularMesh.
    basis : {'xy', 'xz', 'yz'}
        The basis directions for the plot
    slice_index : int
        The mesh index to plot
    score : str
        Score to plot, e.g. 'flux'
    axes : matplotlib.Axes
        Axes to draw to
    axis_units : {'km', 'm', 'cm', 'mm'}
        Units used on the plot axis
    value : str
        A string for the type of value to return  - 'mean' (default),
        'std_dev', 'rel_err', 'sum', or 'sum_sq' are accepted
    outline : True
        If set then an outline will be added to the plot. The outline can be
        by cell or by material.
    outline_by : {'cell', 'material'}
        Indicate whether the plot should be colored by cell or by material
    geometry : openmc.Geometry
        The geometry to use for the outline.
    pixels : int
        This sets the total number of pixels in the plot and the number of
        pixels in each basis direction is calculated from this total and
        the image aspect ratio.
    colorbar : bool
        Whether or not to add a colorbar to the plot.
    volume_normalization : bool, optional
        Whether or not to normalize the data by the volume of the mesh elements.
    scaling_factor : float
        A optional multiplier to apply to the tally data prior to ploting.
    colorbar_kwargs : dict
        Keyword arguments passed to :func:`matplotlib.colorbar.Colorbar`.
    outline_kwargs : dict
        Keyword arguments passed to :func:`matplotlib.pyplot.contour`.
    **kwargs
        Keyword arguments passed to :func:`matplotlib.pyplot.imshow`
    Returns
    -------
    matplotlib.image.AxesImage
        Resulting image
    """

    cv.check_value("basis", basis, _BASES)
    cv.check_value("axis_units", axis_units, ["km", "m", "cm", "mm"])
    cv.check_type("volume_normalization", volume_normalization, bool)
    cv.check_type("outline", outline, bool)

    mesh = tally.find_filter(filter_type=openmc.MeshFilter).mesh
    if not isinstance(mesh, openmc.RegularMesh):
        raise NotImplemented(
            f"Only RegularMesh are currently supported not {type(mesh)}"
        )
    # if mesh.n_dimension != 3:
    #     msg = "Your mesh has {mesh.n_dimension} dimension and currently only RegularMesh with 3 dimensions are supported"
    #     raise NotImplementedError(msg)

    # if score is not specified and tally has a single score then we know which score to use
    if score is None:
        if len(tally.scores) == 1:
            score = tally.scores[0]
        else:
            msg = "score was not specified and there are multiple scores in the tally."
            raise ValueError(msg)

    tally_slice = tally.get_slice(scores=[score])

    # if mesh.n_dimension == 3:

    if 1 in mesh.dimension:
        index_of_2d = mesh.dimension.index(1)
        axis_of_2d = {0: "x", 1: "y", 2: "z"}[index_of_2d]

    # todo check if 1 appears twice or three times, raise value error if so

    tally_data = tally_slice.get_reshaped_data(expand_dims=True, value=value).squeeze()

    basis_to_index = {"xy": 2, "xz": 1, "yz": 0}[basis]
    if len(tally_data.shape) == 3:
        if slice_index is None:
            slice_index = int(tally_data.shape[basis_to_index] / 2)

        if basis == "xz":
            slice_data = tally_data[:, slice_index, :]
            data = np.flip(np.rot90(slice_data, -1))
            xlabel, ylabel = f"x [{axis_units}]", f"z [{axis_units}]"
        elif basis == "yz":
            slice_data = tally_data[slice_index, :, :]
            data = np.flip(np.rot90(slice_data, -1))
            xlabel, ylabel = f"y [{axis_units}]", f"z [{axis_units}]"
        else:  # basis == 'xy'
            slice_data = tally_data[:, :, slice_index]
            data = np.rot90(slice_data, -3)
            xlabel, ylabel = f"x [{axis_units}]", f"y [{axis_units}]"
    # elif mesh.n_dimension == 2:
    elif len(tally_data.shape) == 2:
        if basis_to_index == index_of_2d:
            slice_data = tally_data[:, :]
            if basis == "xz":
                data = np.flip(np.rot90(slice_data, -1))
                xlabel, ylabel = f"x [{axis_units}]", f"z [{axis_units}]"
            elif basis == "yz":
                data = np.flip(np.rot90(slice_data, -1))
                xlabel, ylabel = f"y [{axis_units}]", f"z [{axis_units}]"
            else:  # basis == 'xy'
                data = np.rot90(slice_data, -3)
                xlabel, ylabel = f"x [{axis_units}]", f"y [{axis_units}]"

        else:
            raise ValueError(
                "The selected tally has a mesh that has 1 dimension in the "
                f"{axis_of_2d} axis, minimum of 2 needed to plot with a basis "
                f"of {basis}."
            )

    else:
        raise ValueError("mesh n_dimension")

    if volume_normalization:
        # in a regular mesh all volumes are the same so we just divide by the first
        data = data / mesh.volumes[0][0][0]

    if scaling_factor:
        data = data * scaling_factor

    axis_scaling_factor = {"km": 0.00001, "m": 0.01, "cm": 1, "mm": 10}[axis_units]

    x_min, x_max, y_min, y_max = [
        i * axis_scaling_factor for i in mesh.bounding_box.extent[basis]
    ]

    if axes is None:
        fig, axes = plt.subplots()
        axes.set_xlabel(xlabel)
        axes.set_ylabel(ylabel)

    im = axes.imshow(data, extent=(x_min, x_max, y_min, y_max), **kwargs)

    if colorbar:
        fig.colorbar(im, **colorbar_kwargs)

    if outline and geometry is not None:
        import matplotlib.image as mpimg

        # code to make sure geometry outline is in the middle of the mesh voxel
        # two of the three dimensions are just in the center of the mesh
        # but the slice can move one axis off the center so this needs calculating
        x0, y0, z0 = mesh.lower_left
        x1, y1, z1 = mesh.upper_right
        nx, ny, nz = mesh.dimension
        center_of_mesh = mesh.bounding_box.center
        if basis == "xy":
            zarr = np.linspace(z0, z1, nz + 1)
            if len(tally_data.shape) == 3:
                center_of_mesh_slice = [
                    center_of_mesh[0],
                    center_of_mesh[1],
                    (zarr[slice_index] + zarr[slice_index + 1]) / 2,
                ]
            else:  # 2
                center_of_mesh_slice = mesh.bounding_box.center
        if basis == "xz":
            yarr = np.linspace(y0, y1, ny + 1)
            if len(tally_data.shape) == 3:
                center_of_mesh_slice = [
                    center_of_mesh[0],
                    (yarr[slice_index] + yarr[slice_index + 1]) / 2,
                    center_of_mesh[2],
                ]
            else:  # 2
                center_of_mesh_slice = mesh.bounding_box.center
        if basis == "yz":
            xarr = np.linspace(x0, x1, nx + 1)
            if len(tally_data.shape) == 3:
                center_of_mesh_slice = [
                    (xarr[slice_index] + xarr[slice_index + 1]) / 2,
                    center_of_mesh[1],
                    center_of_mesh[2],
                ]
            else:  # 2
                center_of_mesh_slice = mesh.bounding_box.center

        model = openmc.Model()
        model.geometry = geometry
        plot = openmc.Plot()
        plot.origin = center_of_mesh_slice
        bb_width = mesh.bounding_box.extent[basis]
        plot.width = (bb_width[0] - bb_width[1], bb_width[2] - bb_width[3])
        aspect_ratio = (bb_width[0] - bb_width[1]) / (bb_width[2] - bb_width[3])
        pixels_y = math.sqrt(pixels / aspect_ratio)
        pixels = (int(pixels / pixels_y), int(pixels_y))
        plot.pixels = pixels
        plot.basis = basis
        plot.color_by = outline_by
        model.plots.append(plot)

        with TemporaryDirectory() as tmpdir:
            # Run OpenMC in geometry plotting mode
            model.plot_geometry(False, cwd=tmpdir)

            # Read image from file
            img_path = Path(tmpdir) / f"plot_{plot.id}.png"
            if not img_path.is_file():
                img_path = img_path.with_suffix(".ppm")
            img = mpimg.imread(str(img_path))

        # Combine R, G, B values into a single int
        rgb = (img * 256).astype(int)
        image_value = (rgb[..., 0] << 16) + (rgb[..., 1] << 8) + (rgb[..., 2])

        if basis == "xz":
            image_value = np.rot90(image_value, 2)
        elif basis == "yz":
            image_value = np.rot90(image_value, 2)
        else:  # basis == 'xy'
            image_value = np.rot90(image_value, 2)

        # Plot image and return the axes
        axes.contour(
            image_value,
            origin="upper",
            levels=np.unique(image_value),
            extent=(x_min, x_max, y_min, y_max),
            **outline_kwargs,
        )

    return axes


# TODO currently we allow slice index, but this code will be useful if want to
# allow slicing by axis values / coordinates.
def get_index_where(self, value: float, basis: str = "xy"):
    """Gets the mesh cell index nearest to the specified axis value.
    Parameters
    ----------
    basis : {'xy', 'xz', 'yz'}
        The basis directions for the slice
    value : str
        A string for the type of value to return  - 'mean' (default),
        'std_dev', 'rel_err', 'sum', or 'sum_sq' are accepted
    Returns
    -------
    int
        the index of the mesh cell
    """

    index_of_basis = {"xy": 2, "xz": 1, "yz": 0}[basis]

    if value < self.lower_left[index_of_basis]:
        msg = f"value [{value}] is smaller than the mesh.lower_left [{self.lower_left}]"
        raise ValueError(msg)
    if value > self.upper_right[index_of_basis]:
        msg = (
            f"value [{value}] is bigger than the mesh.upper_right [{self.upper_right}]"
        )
        raise ValueError(msg)

    voxel_axis_vals = np.linspace(
        self.lower_left[index_of_basis],
        self.upper_right[index_of_basis],
        self.dimension[index_of_basis],
        endpoint=True,
    )
    slice_index = (np.abs(voxel_axis_vals - value)).argmin()

    return slice_index
