[![N|Python](https://www.python.org/static/community_logos/python-powered-w-100x40.png)](https://www.python.org)

[![CI with install](https://github.com/fusion-energy/regular_mesh_plotter/actions/workflows/ci_with_install.yml/badge.svg?branch=develop)](https://github.com/fusion-energy/regular_mesh_plotter/actions/workflows/ci_with_install.yml)

[![PyPI](https://img.shields.io/pypi/v/regular-mesh-plotter?color=brightgreen&label=pypi&logo=grebrightgreenen&logoColor=green)](https://pypi.org/project/regular-mesh-plotter/)

[![codecov](https://codecov.io/gh/fusion-energy/regular_mesh_plotter/branch/main/graph/badge.svg)](https://codecov.io/gh/fusion-energy/regular_mesh_plotter)

## A minimal Python package that extracts 2D mesh tally results for plotting convenience.

This package is deployed on [xsplot.com](https://www.xsplot.com) as part of the ```openmc_plot``` suite of plotting apps

# Local install

First you will need openmc installed, then you can install this package with pip

```bash
pip install regular_mesh_plotter
```
# Usage

The package can be used from within your own python script to make plots or via a GUI that is also bundled into the package install.

## Python API script usage

See the [examples folder](https://github.com/fusion-energy/regular_mesh_plotter/tree/master/examples) for example scripts

## Graphical User Interface (GUI) usage

After installing run ```openmc_mesh_plotter``` command from the terminal and the GUI should launch in a new browser window.
# Related packages

[openmc_plot](https://github.com/fusion-energy/openmc_plot)A single package that includes all the various plotters.

If you want to plot the DAGMC geometry without a mesh tally then take a look at
the [dagmc_geometry_slice_plotter](https://github.com/fusion-energy/dagmc_geometry_slice_plotter) package

If you want to plot the Native CSG geometry without a mesh tally then take a look at
the [dagmc_geometry_slice_plotter](https://github.com/fusion-energy/openmc_geometry_plot) package
