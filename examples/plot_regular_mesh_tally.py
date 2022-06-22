import regular_mesh_plotter as rmp
import openmc

# loads in the statepoint file containing tallies
statepoint = openmc.StatePoint(filepath="statepoint.2.h5")

# gets one tally from the available tallies
my_tally = statepoint.get_tally(name="neutron_effective_dose_on_2D_mesh_xy")

# creates a plot of the mesh
rmp.plot_regular_mesh_tally(
    tally=my_tally,
    filename="neutron_effective_dose_on_2D_mesh_xy.png",
    label="",
    base_plt=None,
    x_label="X [cm]",
    y_label="Y [cm]",
    # rotate_plot: float = 0,
    # required_units: str = None,
    # source_strength: float = None,
)
