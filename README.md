[![N|Python](https://www.python.org/static/community_logos/python-powered-w-100x40.png)](https://www.python.org)

[![CI with install](https://github.com/fusion-energy/openmc_regular_mesh_plotter/actions/workflows/ci_with_install.yml/badge.svg)](https://github.com/fusion-energy/openmc_regular_mesh_plotter/actions/workflows/ci_with_install.yml)

[![PyPI](https://img.shields.io/pypi/v/openmc-regular-mesh-plotter?color=brightgreen&label=pypi&logo=grebrightgreenen&logoColor=green)](https://pypi.org/project/openmc-regular-mesh-plotter/)


# A minimal Python package that plots slices of OpenMC regular mesh tallies with the model geometry.

Features

:straight_ruler: Axis units in in helpful units mm, cm, m, km

:eyes: Supports all 3 viewing basis (xy, xz, yz)

:hocho: Automaticly finds central slice or allows user specified slice index

:dart: Supports all values (mean, std_dev etc)

:black_square_button: Adds outlines for geometry cells or material at different pixel resolution

:arrow_right_hook: Customisable by passing keywords to underlying matplotlib functions colorbar, contour and imshow

|<img src="https://user-images.githubusercontent.com/8583900/265032335-27463ee9-8960-4f5e-a662-dab0b6cd9fc5.png" alt="drawing" width="400"/>|<img src="https://user-images.githubusercontent.com/8583900/265065370-734c66ab-b20e-40c8-b72b-88203ea4347b.gif" alt="drawing" width="400"/>|

# Local install

First you will need openmc installed, then you can install this package with pip

```bash
pip install openmc_regular_mesh_plotter
```

# Usage

See the [examples folder](https://github.com/fusion-energy/openmc_regular_mesh_plotter/tree/main/examples) for example scripts

# Web App

This package is deployed on [xsplot.com](https://www.xsplot.com) as part of the ```openmc_plot``` suite of plotting apps
