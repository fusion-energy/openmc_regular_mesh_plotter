import regular_mesh_plotter
import openmc

import openmc_geometry_plot  # extends openmc.Geometry class with plotting functions


# MATERIALS

mat_1 = openmc.Material()
mat_1.add_element("Li", 1)
mat_1.set_density("g/cm3", 3.2720171e-2)  # around 11 g/cm3

my_materials = openmc.Materials([mat_1])


# GEOMETRY

# surfaces
inner_surface = openmc.Sphere(r=500)
outer_surface = openmc.Sphere(r=1000, boundary_type="vacuum")

# cells
inner_region = -inner_surface
inner_cell = openmc.Cell(region=inner_region)

outer_region = -outer_surface & +inner_surface
outer_cell = openmc.Cell(region=outer_region)
outer_cell.fill = mat_1

my_geometry = openmc.Geometry([inner_cell, outer_cell])


# SIMULATION SETTINGS

# Instantiate a Settings object
my_settings = openmc.Settings()
my_settings.batches = 10
my_settings.inactive = 0
my_settings.particles = 500
my_settings.run_mode = "fixed source"

# Create a DT point source
source = openmc.Source()
source.space = openmc.stats.Point((0, 0, 0))
source.angle = openmc.stats.Isotropic()
source.energy = openmc.stats.Discrete([14e6], [1])
my_settings.source = source


my_tallies = openmc.Tallies()

mesh = openmc.RegularMesh().from_domain(
    my_geometry,  # the corners of the mesh are being set automatically to surround the geometry
    dimension=[10, 10, 10],
)
mesh_filter = openmc.MeshFilter(mesh)

mesh_tally_1 = openmc.Tally(name="mesh_tally")
mesh_tally_1.filters = [mesh_filter]
mesh_tally_1.scores = ["flux"]
my_tallies.append(mesh_tally_1)

model = openmc.model.Model(my_geometry, my_materials, my_settings, my_tallies)
sp_filename = model.run()

statepoint = openmc.StatePoint(sp_filename)

# extracts the mesh tally by name
my_mesh_tally = statepoint.get_tally(name="mesh_tally")

# converts the tally result into a VTK file
plot = mesh.plot_slice(dataset=my_mesh_tally.mean, slice_index=5, view_direction="x")
plot.figure.savefig("test.png")

# this section adds a contour line according the the material ids
material_ids = my_geometry.get_slice_of_material_ids(view_direction="x")
plot2 = my_geometry.get_outline_contour(outline_data=material_ids, view_direction="x")
import matplotlib.pyplot as plt

plt.savefig("test2.png")
