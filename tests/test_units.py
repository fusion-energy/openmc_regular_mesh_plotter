import openmc
from matplotlib.colors import LogNorm
from openmc_regular_mesh_plotter import plot_mesh_tally
import pytest


@pytest.fixture()
def model():
    mat1 = openmc.Material()
    mat1.add_nuclide("Li6", 1, percent_type="ao")
    mats = openmc.Materials([mat1])

    # this shape is chose to create axis with testable ranges
    surface1 = openmc.model.RectangularParallelepiped(
        -50, 25, -100, 125, -150, 175, boundary_type="vacuum"
    )
    surface = openmc.model.RectangularParallelepiped(
        -100, 50, -200, 250, -300, 350, boundary_type="vacuum"
    )
    cell1 = openmc.Cell(region=-surface1)
    cell2 = openmc.Cell(region=-surface & +surface1)
    cell1.fill = mat1
    cell2.fill = mat1
    geom = openmc.Geometry([cell1, cell2])

    # work with older versions of openmc
    try:
        source = openmc.IndependentSource()
    except:
        source = openmc.Source()
    source.angle = openmc.stats.Isotropic()
    source.energy = openmc.stats.Discrete([14e6], [1])
    # puts the source in the center of the RectangularParallelepiped
    source.space = openmc.stats.Point([-25.0, 25.0, 25.0])
    # newer versions of openmc support cell2.bounding_box.center

    sett = openmc.Settings()
    sett.batches = 2
    sett.inactive = 0
    sett.particles = 5000
    sett.run_mode = "fixed source"
    sett.source = source

    model = openmc.Model(geom, mats, sett)

    return model


def test_plot_3d_mesh_tally(model):
    geometry = model.geometry

    mesh = openmc.RegularMesh().from_domain(geometry, dimension=[10, 20, 30])
    mesh_filter = openmc.MeshFilter(mesh)
    mesh_tally = openmc.Tally(name="mesh-tal")
    mesh_tally.filters = [mesh_filter]
    mesh_tally.scores = ["flux"]
    tallies = openmc.Tallies([mesh_tally])

    model.tallies = tallies

    sp_filename = model.run()
    with openmc.StatePoint(sp_filename) as statepoint:
        tally_result = statepoint.get_tally(name="mesh-tal")

    plot = plot_mesh_tally(
        tally=tally_result, basis="xy", slice_index=29  # max value of slice selected
    )
    # axis_units defaults to cm
    assert plot.xaxis.get_label().get_text() == "x [cm]"
    assert plot.yaxis.get_label().get_text() == "y [cm]"
    assert plot.get_xlim() == (-100.0, 50)
    assert plot.get_ylim() == (-200.0, 250.0)

    plot = plot_mesh_tally(
        tally=tally_result,
        basis="yz",
        axis_units="m",
        # slice_index=9,  # max value of slice selected
        value="std_dev",
    )
    plot.figure.savefig("x.png")
    assert plot.xaxis.get_label().get_text() == "y [m]"
    assert plot.yaxis.get_label().get_text() == "z [m]"
    assert plot.get_xlim() == (-2.0, 2.5)  # note that units are in m
    assert plot.get_ylim() == (-3.0, 3.5)

    plot = plot_mesh_tally(
        tally=tally_result,
        basis="xz",
        slice_index=19,  # max value of slice selected
        axis_units="mm",
        score="flux",
        value="mean",
        outline=True,
        geometry=geometry,
        outline_by="material",
        colorbar_kwargs={"label": "neutron flux"},
        norm=LogNorm(vmin=1e-6, vmax=max(tally_result.mean.flatten())),
    )
    assert plot.xaxis.get_label().get_text() == "x [mm]"
    assert plot.yaxis.get_label().get_text() == "z [mm]"
    assert plot.get_xlim() == (-1000.0, 500)  # note that units are in mm
    assert plot.get_ylim() == (-3000.0, 3500.0)
    plot.figure.savefig("z.png")


def test_plot_2d_mesh_tally(model):
    geometry = model.geometry

    mesh = openmc.RegularMesh().from_domain(geometry, dimension=[1, 20, 30])
    mesh_filter = openmc.MeshFilter(mesh)
    mesh_tally = openmc.Tally(name="mesh-tal")
    mesh_tally.filters = [mesh_filter]
    mesh_tally.scores = ["flux"]
    tallies = openmc.Tallies([mesh_tally])

    model.tallies = tallies

    sp_filename = model.run()
    with openmc.StatePoint(sp_filename) as statepoint:
        tally_result = statepoint.get_tally(name="mesh-tal")

    plot = plot_mesh_tally(
        tally=tally_result, basis="yz", slice_index=29  # max value of slice selected
    )
    # axis_units defaults to cm
    assert plot.xaxis.get_label().get_text() == "y [cm]"
    assert plot.yaxis.get_label().get_text() == "z [cm]"
    assert plot.get_xlim() == (-200.0, 250.0)
    assert plot.get_ylim() == (-300.0, 350.0)
    plot.figure.savefig("t.png")

    plot = plot_mesh_tally(
        tally=tally_result,
        basis="yz",
        axis_units="m",
        # slice_index=9,  # max value of slice selected
        value="std_dev",
    )
    plot.figure.savefig("x.png")
    assert plot.xaxis.get_label().get_text() == "y [m]"
    assert plot.yaxis.get_label().get_text() == "z [m]"
    assert plot.get_xlim() == (-2.0, 2.5)  # note that units are in m
    assert plot.get_ylim() == (-3.0, 3.5)


# todo catch errors when 2d mesh used and 1d axis selected for plotting'
