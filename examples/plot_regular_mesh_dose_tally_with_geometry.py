import regular_mesh_plotter as rmp
import openmc
import matplotlib.pyplot as plt

# loads in the statepoint file containing tallies
statepoint = openmc.StatePoint(filepath="statepoint.2.h5")

# gets one tally from the available tallies
my_tally = statepoint.get_tally(name="neutron_effective_dose_on_2D_mesh_xy")

# creates a plot of the mesh
rmp.plot_regular_mesh_dose_tally_with_geometry(
    tally=my_tally,
    dagmc_file_or_trimesh_object="dagmc.h5m",
    filename="plot_regular_mesh_dose_tally_with_geometry.png",
    scale=None,  # LogNorm(),
    vmin=None,
    label="Effective dose [picosievert / second]",
    x_label="X [cm]",
    y_label="Y [cm]",
    plane_origin=None,  # this could be skipped as it defaults to None, which uses the center of the mesh
    plane_normal=[0, 0, 1],
    rotate_mesh=0,
    rotate_geometry=0,
    required_units="picosievert / second",
    source_strength=1e20,
)

plt.show()
