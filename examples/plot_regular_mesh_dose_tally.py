import regular_mesh_plotter as rmp
import openmc
import matplotlib.pyplot as plt

# loads in the statepoint file containing tallies
statepoint = openmc.StatePoint(filepath="statepoint.2.h5")

# gets one tally from the available tallies
my_tally = statepoint.get_tally(name="neutron_effective_dose_on_2D_mesh_xy")

# creates a plot of the mesh tally
rmp.plot_regular_mesh_dose_tally(
    tally=my_tally,  # the openmc tally object to plot, must be a 2d mesh tally
    filename="plot_regular_mesh_dose_tally.png",  # the filename of the picture file saved
    x_label="X [cm]",
    y_label="Y [cm]",
    rotate_plot=0,
    required_units="picosievert / source_particle",
    source_strength=None,
    label="Effective dose [picosievert / source_particle]",
)

# displays the plot
plt.show()
