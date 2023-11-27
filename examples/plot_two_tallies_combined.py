import openmc
from matplotlib.colors import LogNorm
from openmc_regular_mesh_plotter import plot_mesh_tally


# MATERIALS
mat_1 = openmc.Material()
mat_1.add_element("Li", 1)
mat_1.set_density("g/cm3", 0.1)
my_materials = openmc.Materials([mat_1])

# GEOMETRY
# surfaces
inner_surface = openmc.Sphere(r=200)
outer_surface = openmc.Sphere(r=400, boundary_type="vacuum")
# regions
inner_region = -inner_surface
outer_region = -outer_surface & +inner_surface
# cells
inner_cell = openmc.Cell(region=inner_region)
outer_cell = openmc.Cell(region=outer_region)
outer_cell.fill = mat_1
my_geometry = openmc.Geometry([inner_cell, outer_cell])

# SIMULATION SETTINGS
my_settings = openmc.Settings()
my_settings.batches = 10
my_settings.inactive = 0
my_settings.particles = 50000
my_settings.run_mode = "fixed source"
# my_settings.photon_transport = True # could be enabled but we have a photon source instead which converges a photon head deposition quicker

# Create a neutron and photon source
try:
    source_n = openmc.IndependentSource()
    source_p = openmc.IndependentSource()
except:
    # work with older versions of openmc
    source_n = openmc.Source()
    source_p = openmc.Source()
    
source_n.space = openmc.stats.Point((200, 0, 0))
source_n.angle = openmc.stats.Isotropic()
source_n.energy = openmc.stats.Discrete([0.1e6], [1])
source_n.strength = 1
source_n.particle='neutron'

source_p.space = openmc.stats.Point((-200, 0, 0))
source_p.angle = openmc.stats.Isotropic()
source_p.energy = openmc.stats.Discrete([10e6], [1])
source_p.strength = 10
source_p.particle='photon'

my_settings.source = [source_n, source_p]

# Tallies
mesh = openmc.RegularMesh().from_domain(
    my_geometry,  # the corners of the mesh are being set automatically to surround the geometry
    dimension=[40, 40, 40],
)

mesh_filter = openmc.MeshFilter(mesh)
neutron_filter = openmc.ParticleFilter("neutron")
photon_filter = openmc.ParticleFilter("photon")

mesh_tally_1 = openmc.Tally(name="mesh_tally_neutron")
mesh_tally_1.filters = [mesh_filter, neutron_filter]
mesh_tally_1.scores = ["heating"]

mesh_tally_2 = openmc.Tally(name="mesh_tally_photon")
mesh_tally_2.filters = [mesh_filter, photon_filter]
mesh_tally_2.scores = ["heating"]

my_tallies = openmc.Tallies([mesh_tally_1, mesh_tally_2])


model = openmc.model.Model(my_geometry, my_materials, my_settings, my_tallies)
sp_filename = model.run()

# post process simulation result
statepoint = openmc.StatePoint(sp_filename)

# extracts the mesh tally by name
my_mesh_tally_photon = statepoint.get_tally(name="mesh_tally_photon")
my_mesh_tally_neutron = statepoint.get_tally(name="mesh_tally_neutron")

# default tally units for heating are in eV per source neutron
# for this example plot we want Mega Joules per second per cm3 or Mjcm^-3s^-1
neutrons_per_second = 1e21
eV_to_joules = 1.60218e-19
joules_to_mega_joules = 1e-6
scaling_factor = neutrons_per_second * eV_to_joules * joules_to_mega_joules
# note that volume_normalization is enabled so this will also change the units to divide by the volume of each mesh voxel
# alternatively you could set volume_normalization to false and divide by the mesh.volume[0][0][0] in the scaling factor
# in a regular mesh all the voxels have the same volume so the [0][0][0] just picks the first volume

plot = plot_mesh_tally(
    tally=[my_mesh_tally_neutron],
    colorbar=True,
    # norm=LogNorm()
)
plot.title.set_text("neutron heating")
plot.figure.savefig("neutron_regular_mesh_plotter.png")
print('written file neutron_regular_mesh_plotter.png')

plot = plot_mesh_tally(
    tally=[my_mesh_tally_photon],
    colorbar=True,
    # norm=LogNorm()
)
plot.title.set_text("photon heating")
plot.figure.savefig("photon_regular_mesh_plotter.png")
print('written file photon_regular_mesh_plotter.png')

plot = plot_mesh_tally(
    tally=[my_mesh_tally_photon, my_mesh_tally_neutron],
    colorbar=True,
    # norm=LogNorm()
)
plot.title.set_text("photon and neutron heating")
plot.figure.savefig("photon_and_neutron_regular_mesh_plotter.png")
print('written file photon_and_neutron_regular_mesh_plotter.png')
