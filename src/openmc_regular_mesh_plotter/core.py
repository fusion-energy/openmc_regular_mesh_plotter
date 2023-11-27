import math
from pathlib import Path
from tempfile import TemporaryDirectory
import typing
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


def _squeeze_end_of_array(array, dims_required=3):
    while len(array.shape) > dims_required:
        array = np.squeeze(array, axis=len(array.shape) - 1)
    return array


def plot_mesh_tally(
    tally: typing.Union["openmc.Tally", typing.Sequence["openmc.Tally"]],
    basis: str = "xy",
    slice_index: typing.Optional[int] = None,
    score: typing.Optional[str] = None,
    axes: typing.Optional[str] = None,
    axis_units: str = "cm",
    value: str = "mean",
    outline: bool = False,
    outline_by: str = "cell",
    geometry: typing.Optional["openmc.Geometry"] = None,
    pixels: int = 40000,
    colorbar: bool = True,
    volume_normalization: bool = True,
    scaling_factor: typing.Optional[float] = None,
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
        Keyword arguments passed to :func:`matplotlib.pyplot.contour`. Defaults
        to "colors": "black", "linestyles": "solid", "linewidths": 1
    **kwargs
        Keyword arguments passed to :func:`matplotlib.pyplot.imshow`. Defaults
        to {"interpolation", "none"}.
    Returns
    -------
    matplotlib.image.AxesImage
        Resulting image
    """

    cv.check_value("basis", basis, _BASES)
    cv.check_value("axis_units", axis_units, ["km", "m", "cm", "mm"])
    cv.check_type("volume_normalization", volume_normalization, bool)
    cv.check_type("outline", outline, bool)

    if isinstance(tally, typing.Sequence):
        mesh_ids = []
        for one_tally in tally:
            mesh = one_tally.find_filter(filter_type=openmc.MeshFilter).mesh
            # TODO check the tallies use the same mesh
            mesh_ids.append(mesh.id)
        if not all(i == mesh_ids[0] for i in mesh_ids):
            raise ValueError(
                f"mesh ids {mesh_ids} are different, please use same mesh when combining tallies"
            )
    else:
        mesh = tally.find_filter(filter_type=openmc.MeshFilter).mesh

    if isinstance(mesh, openmc.CylindricalMesh):
        raise NotImplemented(
            f"Only RegularMesh are supported, not {type(mesh)}, try the openmc_cylindrical_mesh_plotter package available at https://github.com/fusion-energy/openmc_cylindrical_mesh_plotter/"
        )
    if not isinstance(mesh, openmc.RegularMesh):
        raise NotImplemented(f"Only RegularMesh are supported, not {type(mesh)}")

    axis_scaling_factor = {"km": 0.00001, "m": 0.01, "cm": 1, "mm": 10}[axis_units]

    x_min, x_max, y_min, y_max = [
        i * axis_scaling_factor for i in mesh.bounding_box.extent[basis]
    ]

    if basis == "xz":
        xlabel, ylabel = f"x [{axis_units}]", f"z [{axis_units}]"
    elif basis == "yz":
        xlabel, ylabel = f"y [{axis_units}]", f"z [{axis_units}]"
    else:  # basis == 'xy'
        xlabel, ylabel = f"x [{axis_units}]", f"y [{axis_units}]"

    if axes is None:
        fig, axes = plt.subplots()
        axes.set_xlabel(xlabel)
        axes.set_ylabel(ylabel)

    basis_to_index = {"xy": 2, "xz": 1, "yz": 0}[basis]
    if slice_index is None:
        # finds the mid index
        slice_index = int(mesh.dimension[basis_to_index] / 2)

    # zero values with logscale produce noise / fuzzy on the time but setting interpolation to none solves this
    default_imshow_kwargs = {"interpolation": "none"}
    default_imshow_kwargs.update(kwargs)

    if isinstance(tally, typing.Sequence):
        for counter, one_tally in enumerate(tally):
            new_data = _get_tally_data(
                scaling_factor,
                mesh,
                basis,
                one_tally,
                value,
                volume_normalization,
                score,
                slice_index,
            )
            if counter == 0:
                data = np.zeros(shape=new_data.shape)
            data = data + new_data
    else:  # single tally
        data = _get_tally_data(
            scaling_factor,
            mesh,
            basis,
            tally,
            value,
            volume_normalization,
            score,
            slice_index,
        )

    im = axes.imshow(data, extent=(x_min, x_max, y_min, y_max), **default_imshow_kwargs)

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
            center_of_mesh_slice = [
                center_of_mesh[0],
                center_of_mesh[1],
                (zarr[slice_index] + zarr[slice_index + 1]) / 2,
            ]
        if basis == "xz":
            yarr = np.linspace(y0, y1, ny + 1)
            center_of_mesh_slice = [
                center_of_mesh[0],
                (yarr[slice_index] + yarr[slice_index + 1]) / 2,
                center_of_mesh[2],
            ]
        if basis == "yz":
            xarr = np.linspace(x0, x1, nx + 1)
            center_of_mesh_slice = [
                (xarr[slice_index] + xarr[slice_index + 1]) / 2,
                center_of_mesh[1],
                center_of_mesh[2],
            ]

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


def _get_tally_data(
    scaling_factor, mesh, basis, tally, value, volume_normalization, score, slice_index
):
    # if score is not specified and tally has a single score then we know which score to use
    if score is None:
        if len(tally.scores) == 1:
            score = tally.scores[0]
        else:
            msg = "score was not specified and there are multiple scores in the tally."
            raise ValueError(msg)

    tally_slice = tally.get_slice(scores=[score])

    if 1 in mesh.dimension:
        index_of_2d = mesh.dimension.index(1)
        axis_of_2d = {0: "x", 1: "y", 2: "z"}[index_of_2d]
        if (
            axis_of_2d in basis
        ):  # checks if the axis is being plotted, e.g is 'x' in 'xy'
            raise ValueError(
                "The selected tally has a mesh that has 1 dimension in the "
                f"{axis_of_2d} axis, minimum of 2 needed to plot with a basis "
                f"of {basis}."
            )

    # TODO check if 1 appears twice or three times, raise value error if so

    tally_data = tally_slice.get_reshaped_data(
        expand_dims=True, value=value
    )  # .squeeze()

    tally_data = _squeeze_end_of_array(tally_data, dims_required=3)

    # if len(tally_data.shape) == 3:
    if mesh.n_dimension == 3:
        if basis == "xz":
            slice_data = tally_data[:, slice_index, :]
            data = np.flip(np.rot90(slice_data, -1))
        elif basis == "yz":
            slice_data = tally_data[slice_index, :, :]
            data = np.flip(np.rot90(slice_data, -1))
        else:  # basis == 'xy'
            slice_data = tally_data[:, :, slice_index]
            data = np.rot90(slice_data, -3)

    else:
        raise ValueError(
            f"mesh n_dimension is not 3 but is {mesh.n_dimension} which is not supported"
        )

    if volume_normalization:
        # in a regular mesh all volumes are the same so we just divide by the first
        data = data / mesh.volumes[0][0][0]

    if scaling_factor:
        data = data * scaling_factor
    return data
