

from regular_mesh_plotter import plot_regular_mesh_tally_with_geometry
import openmc

# loads in the statepoint file containing tallies
statepoint = openmc.StatePoint(filepath="statepoint.3.h5")

# gets one tally from the available tallies
my_tally = statepoint.get_tally(name="neutron_effective_dose_on_2D_mesh_xy")

# creates the matplotlib mesh plot with geometry
plot = plot_regular_mesh_tally_with_geometry(
    tally=my_tally,
    mesh_file_or_trimesh_object="dagmc.h5m",
)

plot.show()