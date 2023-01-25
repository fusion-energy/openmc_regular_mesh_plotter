import numpy as np
import typing
import openmc

class RegularMesh(openmc.RegularMesh):

    def slice_of_data(
        self,
        dataset: np.ndarray,
        slice_index: int = 0,
        view_direction: str = 'z',
        volume_normalization: bool = True
    ):
        """Obtains the dataset values on an axis aligned 2D slice through the
        mesh. Useful for producing plots of slice data

        Parameters
        ----------
        datasets : numpy.ndarray
            1-D array of data values. Will be reshaped to fill the mesh and
            should therefore have the same number of entries to fill the mesh
        slice_index : int
            The index of the mesh slice to extract.
        view_direction : str
            The axis to view the slice from. Supports negative and positive axis
            values. Acceptable values are 'x', 'y', 'z', '-x', '-y', '-z'.
        volume_normalization : bool, optional
            Whether or not to normalize the data by the volume of the mesh
            elements.

        Returns
        -------
        np.array()
            the 2D array of dataset values
        """

        if volume_normalization:
            dataset = dataset.flatten() / self.volumes.flatten()

        reshaped_ds = dataset.reshape(self.dimension, order="F")


        if view_direction == "x":
            # vertical axis is z, horizontal axis is -y
            transposed_ds = reshaped_ds.transpose(0, 1, 2)[slice_index]
            rotated_ds = np.rot90(transposed_ds, 1)
            aligned_ds = np.fliplr(rotated_ds)
        elif view_direction == "-x":
            # vertical axis is z, horizontal axis is y
            transposed_ds = reshaped_ds.transpose(0, 1, 2)[slice_index]
            aligned_ds = np.rot90(transposed_ds, 1)
        elif view_direction == "y":
            # vertical axis is z, horizontal axis is x
            transposed_ds = reshaped_ds.transpose(1, 2, 0)[slice_index]
            aligned_ds = np.flipud(transposed_ds)
        elif view_direction == "-y":
            # vertical axis is z, horizontal axis is -x
            transposed_ds = reshaped_ds.transpose(1, 2, 0)[slice_index]
            aligned_ds = np.flipud(transposed_ds)
            aligned_ds = np.fliplr(aligned_ds)
        elif view_direction == "z":
            # vertical axis is y, horizontal axis is -x
            transposed_ds = reshaped_ds.transpose(2, 0, 1)[slice_index]
            aligned_ds = np.rot90(transposed_ds, 1)
            aligned_ds = np.fliplr(aligned_ds)
        elif view_direction == "-z":
            # vertical axis is y, horizontal axis is x
            transposed_ds = reshaped_ds.transpose(2, 0, 1)[slice_index]
            aligned_ds = np.rot90(transposed_ds, 1)
        else:
            msg = 'view_direction is not one of the acceptable options {supported_view_dirs}'
            raise ValueError(msg)

        return aligned_ds


    def plot_slice(
        self,
        dataset: np.ndarray,
        slice_index: typing.Optional[int] = None,
        view_direction: str = 'z',
        axes: typing.Optional['matplotlib.Axes'] = None,
        volume_normalization: bool = True,
        **kwargs
    ):
        """Create a slice plot of the dataset on the RegularMesh.

        Parameters
        ----------
        datasets : numpy.ndarray
            1-D array of data values. Will be reshaped to fill the mesh and
            should therefore have the same number of entries to fill the mesh
        slice_index : int
            The index of the mesh slice to extract. If not set then the index
            that slices through the middle of the mesh will be used
        view_direction : str
            The axis to view the slice from. Supports negative and positive axis
            values. Acceptable values are 'x', 'y', 'z', '-x', '-y', '-z'.
        axes : matplotlib.Axes, optional
            Axes to draw to
        volume_normalization : bool, optional
            Whether or not to normalize the data by the volume of the mesh
            elements.
        **kwargs
            Keyword arguments passed to :func:`matplotlib.pyplot.imshow`

        Returns
        -------
        matplotlib.image.AxesImage
            Resulting image
        """

        import matplotlib.pyplot as plt

        # gets the axis labels and bounding box index
        if 'x' in view_direction:
            x_label = 'Y [cm]'
            y_label = 'Z [cm]'
            bb_index = 0

        if 'y' in view_direction:
            x_label = 'X [cm]'
            y_label = 'Z [cm]'
            bb_index = 1

        if 'z' in view_direction:
            x_label = 'X [cm]'
            y_label = 'Y [cm]'
            bb_index = 2

        # selecting mid index on the mesh for the slice
        if slice_index is None:
            slice_index = int(self.dimension[bb_index]/2)

        # slice_of_data also checks the view_direction is acceptable
        image_slice = self.slice_of_data(
            dataset=dataset,
            slice_index=slice_index,
            view_direction=view_direction,
            volume_normalization=volume_normalization,
        )

        # gets the extent of the plot
        x_min = self.lower_left[bb_index]
        x_max = self.upper_right[bb_index]
        y_min = self.lower_left[bb_index]
        y_max = self.upper_right[bb_index]

        if axes is None:
            fig, axes = plt.subplots()
            axes.set_xlabel(x_label)
            axes.set_ylabel(y_label)
            axes.set_title(f'View direction {view_direction}')

        return axes.imshow(
            X=image_slice,
            extent=(x_min, x_max, y_min, y_max),
            aspect='auto',
            **kwargs
        )


# def get_cell_ids_for_regularmesh_slice(mesh, geometry):
    # loop through the centroids of the mesh
    # find the material at each point 
    # build up a pixel map of material ids


openmc.RegularMesh = RegularMesh

