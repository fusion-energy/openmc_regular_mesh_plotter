
import regular_mesh_plotter as rmp
import openmc

# loads in the statepoint file containing tallies
statepoint = openmc.StatePoint(filepath="statepoint.2.h5")

# gets one tally from the available tallies
my_tally = statepoint.get_tally(name="2_neutron_effective_dose")

# creates a plot of the mesh
plot_regular_mesh_values(
    values: np.ndarray,
    filename: Optional[str] = None,
    scale=None,  # LogNorm(),
    vmin=None,
    label="",
    base_plt=None,
    extent=None,
    x_label="X [cm]",
    y_label="Y [cm]",
    rotate_plot: float = 0,
)