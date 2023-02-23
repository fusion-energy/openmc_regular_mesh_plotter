import numpy as np
import typing
import openmc


def get_tallies_with_regular_mesh_filters(statepoint: openmc.StatePoint):
    """scans the statepoint object to find all tallies and with regular mesh
    filters, returns a list of tally indexes"""

    matching_tally_ids = []
    for tally_id, tally in statepoint.tallies.items():
        print("tally id", tally_id)
        try:
            mf = tally.find_filter(filter_type=openmc.MeshFilter)
            if isinstance(mf.mesh, openmc.RegularMesh):
                matching_tally_ids.append(tally.id)
                print("found regmeshfilter")
        except ValueError:
            mf = None

    return sorted(matching_tally_ids)


def get_regularmesh_tallies_and_scores(statepoint: openmc.StatePoint):
    """scans the statepoint object to find all tallies and scores,
    returns list of dictionaries. Each dictionary contains tally id,
    score and tally name"""

    tallies_of_interest = get_tallies_with_regular_mesh_filters(statepoint)

    tally_score_info = []
    for tally_id in tallies_of_interest:
        tally = statepoint.tallies[tally_id]
        for score in tally.scores:
            entry = {"id": tally.id, "score": score, "name": tally.name}
            tally_score_info.append(entry)

    return tally_score_info


def get_mpl_plot_extent(self, view_direction: str = "x"):
    """Returns the (x_min, x_max, y_min, y_max) of the bounding box. The
    view_direction is taken into account and can be set using
    openmc.Geometry.view_direction property is taken into account and can be
    set to 'x', 'y' or 'z'."""

    bb = (self.lower_left, self.upper_right)

    x_min = self.get_side_extent("left", view_direction, bb)
    x_max = self.get_side_extent("right", view_direction, bb)
    y_min = self.get_side_extent("bottom", view_direction, bb)
    y_max = self.get_side_extent("top", view_direction, bb)

    return (x_min, x_max, y_min, y_max)


def get_side_extent(self, side: str, view_direction: str = "x", bb=None):
    if bb is None:
        bb = (self.lower_left, self.upper_right)

    avail_extents = {}
    avail_extents[("left", "x")] = bb[0][1]
    avail_extents[("right", "x")] = bb[1][1]
    avail_extents[("top", "x")] = bb[1][2]
    avail_extents[("bottom", "x")] = bb[0][2]
    avail_extents[("left", "y")] = bb[0][0]
    avail_extents[("right", "y")] = bb[1][0]
    avail_extents[("top", "y")] = bb[1][2]
    avail_extents[("bottom", "y")] = bb[0][2]
    avail_extents[("left", "z")] = bb[0][0]
    avail_extents[("right", "z")] = bb[1][0]
    avail_extents[("top", "z")] = bb[1][1]
    avail_extents[("bottom", "z")] = bb[0][1]
    return avail_extents[(side, view_direction)]


def reshape_data(self, dataset, view_direction):
    reshaped_ds = dataset.reshape(self.dimension, order="F")

    if view_direction == "x":
        # vertical axis is z, horizontal axis is -y
        transposed_ds = reshaped_ds.transpose(0, 1, 2)

    elif view_direction == "-x":
        # vertical axis is z, horizontal axis is y
        transposed_ds = reshaped_ds.transpose(0, 1, 2)

    elif view_direction == "y":
        # vertical axis is z, horizontal axis is x
        transposed_ds = reshaped_ds.transpose(1, 2, 0)

    elif view_direction == "-y":
        # vertical axis is z, horizontal axis is -x
        transposed_ds = reshaped_ds.transpose(1, 2, 0)

    elif view_direction == "z":
        # vertical axis is y, horizontal axis is -x
        transposed_ds = reshaped_ds.transpose(2, 0, 1)

    elif view_direction == "-z":
        # vertical axis is y, horizontal axis is x
        transposed_ds = reshaped_ds.transpose(2, 0, 1)

    else:
        msg = "view_direction of {view_direction} is not one of the acceptable options ({supported_view_dirs})"
        raise ValueError(msg)

    return transposed_ds


def slice_of_data(
    self,
    dataset: np.ndarray,
    view_direction: str = "z",
    slice_index: typing.Optional[int] = None,
    volume_normalization: bool = True,
):
    """Obtains the dataset values on an axis aligned 2D slice through the
    mesh. Useful for producing plots of slice data

    Parameters
    ----------
    datasets : numpy.ndarray
        1-D array of data values. Will be reshaped to fill the mesh and
        should therefore have the same number of entries to fill the mesh
    view_direction : str
        The axis to view the slice from. Supports negative and positive axis
        values. Acceptable values are 'x', 'y', 'z', '-x', '-y', '-z'.
    slice_index : int
        The index of the mesh slice to extract.
    volume_normalization : bool, optional
        Whether or not to normalize the data by the volume of the mesh
        elements.

    Returns
    -------
    np.array()
        the 2D array of dataset values
    """

    bb_index_to_view_direction = {"x": 0, "y": 1, "z": 2}

    if slice_index is None:
        slice_index = int(
            self.dimension[bb_index_to_view_direction[view_direction]] / 2
        )

    if volume_normalization:
        dataset = dataset.flatten() / self.volumes.flatten()

    transposed_ds = self.reshape_data(dataset, view_direction)[slice_index]

    if view_direction == "x":
        # vertical axis is z, horizontal axis is -y
        rotated_ds = np.rot90(transposed_ds, 1)
        aligned_ds = np.fliplr(rotated_ds)
    elif view_direction == "-x":
        # vertical axis is z, horizontal axis is y
        aligned_ds = np.rot90(transposed_ds, 1)
    elif view_direction == "y":
        # vertical axis is z, horizontal axis is x
        aligned_ds = np.flipud(transposed_ds)
    elif view_direction == "-y":
        # vertical axis is z, horizontal axis is -x
        aligned_ds = np.flipud(transposed_ds)
        aligned_ds = np.fliplr(aligned_ds)
    elif view_direction == "z":
        # vertical axis is y, horizontal axis is -x
        aligned_ds = np.rot90(transposed_ds, 1)
        aligned_ds = np.fliplr(aligned_ds)
    elif view_direction == "-z":
        # vertical axis is y, horizontal axis is x
        aligned_ds = np.rot90(transposed_ds, 1)
    else:
        msg = "view_direction of {view_direction} is not one of the acceptable options ({supported_view_dirs})"
        raise ValueError(msg)

    return aligned_ds


def get_axis_labels(self, view_direction):
    """Returns two axis label values for the x and y value. Takes
    view_direction into account."""

    if view_direction == "x":
        xlabel = "Y [cm]"
        ylabel = "Z [cm]"
    if view_direction == "y":
        xlabel = "X [cm]"
        ylabel = "Z [cm]"
    if view_direction == "z":
        xlabel = "X [cm]"
        ylabel = "Y [cm]"
    return xlabel, ylabel


openmc.RegularMesh.reshape_data = reshape_data
openmc.mesh.RegularMesh.reshape_data = reshape_data

openmc.RegularMesh.get_axis_labels = get_axis_labels
openmc.mesh.RegularMesh.get_axis_labels = get_axis_labels

openmc.RegularMesh.slice_of_data = slice_of_data
openmc.mesh.RegularMesh.slice_of_data = slice_of_data

openmc.RegularMesh.get_mpl_plot_extent = get_mpl_plot_extent
openmc.mesh.RegularMesh.get_mpl_plot_extent = get_mpl_plot_extent

openmc.RegularMesh.get_side_extent = get_side_extent
openmc.mesh.RegularMesh.get_side_extent = get_side_extent
