import openmc


mat1 = openmc.Material()
mat1.add_nuclide("He4", 1)
mat1.set_density("g/cm3", 1)
my_materials = openmc.Materials([mat1])
surf1 = openmc.Sphere(r=10, boundary_type="vacuum")
region1 = -surf1
cell1 = openmc.Cell(region=region1)
my_geometry = openmc.Geometry([cell1])
my_settings = openmc.Settings()
my_settings.batches = 3
my_settings.particles = 500
my_settings.run_mode = "fixed source"
my_source = openmc.Source()
my_source.space = openmc.stats.Point((0, 0, 0))
my_source.angle = openmc.stats.Isotropic()
my_source.energy = openmc.stats.Discrete([14e6], [1])
my_settings.source = my_source
cymesh = openmc.CylindricalMesh().from_domain(my_geometry)
regmesh = openmc.RegularMesh().from_domain(my_geometry)
regmesh_filter = openmc.MeshFilter(regmesh)
cmesh_filter = openmc.MeshFilter(cymesh)
cell_filter = openmc.CellFilter(cell1)

cell_tally_1 = openmc.Tally(name="tallies_on_cell_flux_and_heating")
cell_tally_1.id = 1
cell_tally_1.filters = [cell_filter]
cell_tally_1.scores = ["flux", "heating"]

mesh_tally_1 = openmc.Tally(name="tallies_on_regmesh_flux_and_heating")
mesh_tally_1.id = 4
mesh_tally_1.filters = [regmesh_filter]
mesh_tally_1.scores = ["flux", "heating"]

mesh_tally_2 = openmc.Tally(name="tallies_on_regmesh_absorption")
mesh_tally_2.id = 3
mesh_tally_2.filters = [regmesh_filter]
mesh_tally_2.scores = ["absorption"]

mesh_tally_3 = openmc.Tally(name="tallies_on_cymesh_absorption")
mesh_tally_3.id = 5
mesh_tally_3.filters = [cmesh_filter]
mesh_tally_3.scores = ["absorption"]

my_tallies = openmc.Tallies([cell_tally_1, mesh_tally_1, mesh_tally_2, mesh_tally_3])
model = openmc.model.Model(my_geometry, my_materials, my_settings, my_tallies)
output_filename = model.run()
