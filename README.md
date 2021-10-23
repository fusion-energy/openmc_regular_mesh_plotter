[![N|Python](https://www.python.org/static/community_logos/python-powered-w-100x40.png)](https://www.python.org)

[![CI with install](https://github.com/fusion-energy/regular_mesh_plotter/actions/workflows/ci_with_install.yml/badge.svg?branch=develop)](https://github.com/fusion-energy/regular_mesh_plotter/actions/workflows/ci_with_install.yml)

[![PyPI](https://img.shields.io/pypi/v/regular-mesh-plotter?color=brightgreen&label=pypi&logo=grebrightgreenen&logoColor=green)](https://pypi.org/project/regular-mesh-plotter/)

[![codecov](https://codecov.io/gh/fusion-energy/regular_mesh_plotter/branch/main/graph/badge.svg)](https://codecov.io/gh/fusion-energy/regular_mesh_plotter)

## A minimal Python package that plots 2D mesh tally results with the underlying DAGMC geometry

# Installation

```bash
pip install regular_mesh_plotter
```

Mesh results in the form of Numpy arrays or OpenMC.tally objects can be plotted
with a single API call.

A Matplotlib.pyplot object is returned by all functions so one can make changes
to the legend, axis, colour map etc. However some key options are accessable
in the function call directly.

There are additional options that allow

- rotation of the mesh tally results
- rotation of the DAGMC geometry slice
- saving the plot as an image file
- specifying contour lines TODO
- changing axis and colour bar labels
- changing colour scale applied
- truncation of values
- The plane_normal of the DAGMC geometry

The resulting plots can be used to show dose maps, activation, reaction rate
and other mesh tally results.


Example 1 shows a Numpy array plotted
```python
TODO
```

Example 2 shows a Numpy array plotted with an underlying DAGMC geometry
```python
TODO
```

Example 3 shows a OpenMC tally plotted with an underlying DAGMC geometry
```python
TODO
```

Example 4 shows how to rotate the underlying DAGMC geometry and mesh tally.
This is sometimes necessary as the slice and mesh can get out of alignment
when changing the   
```python
TODO
```

# Related packages

If you want to plot the DAGMC geometry without a mesh tally then take a look at
the [dagmc_geometry_slice_plotter](https://github.com/fusion-energy/dagmc_geometry_slice_plotter) package
