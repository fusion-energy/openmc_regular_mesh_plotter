# this example is used to make the animation in the readme.
# It is also set up to accept any geometry and the mesh tally will adapt to the geometry dimensions


import openmc
import numpy as np
from matplotlib.colors import LogNorm
from openmc_regular_mesh_plotter import plot_mesh_tally
from matplotlib import cm

# MATERIALS

breeder_material = openmc.Material()  # Pb84.2Li15.8
breeder_material.add_element("Pb", 84.2, percent_type="ao")
breeder_material.add_element(
    "Li",
    15.8,
    percent_type="ao",
    enrichment=7.0,
    enrichment_target="Li6",
    enrichment_type="ao",
)  # natural enrichment = 7% Li6
breeder_material.set_density("atom/b-cm", 3.2720171e-2)  # around 11 g/cm3

copper_material = openmc.Material()
copper_material.set_density("g/cm3", 8.5)
copper_material.add_element("Cu", 1.0)

eurofer_material = openmc.Material()
eurofer_material.set_density("g/cm3", 7.75)
eurofer_material.add_element("Fe", 89.067, percent_type="wo")

my_materials = openmc.Materials([breeder_material, eurofer_material, copper_material])


# GEOMETRY

# surfaces
central_sol_surface = openmc.ZCylinder(r=100)
central_shield_outer_surface = openmc.ZCylinder(r=110)
vessel_inner_surface = openmc.Sphere(r=500)
first_wall_outer_surface = openmc.Sphere(r=510)
breeder_blanket_outer_surface = openmc.Sphere(r=610, boundary_type="vacuum")
# regions
central_sol_region = -central_sol_surface & -breeder_blanket_outer_surface
central_shield_region = (
    +central_sol_surface
    & -central_shield_outer_surface
    & -breeder_blanket_outer_surface
)
inner_vessel_region = -vessel_inner_surface & +central_shield_outer_surface
first_wall_region = -first_wall_outer_surface & +vessel_inner_surface
breeder_blanket_region = (
    +first_wall_outer_surface
    & -breeder_blanket_outer_surface
    & +central_shield_outer_surface
)
# cells
central_sol_cell = openmc.Cell(region=central_sol_region)
central_shield_cell = openmc.Cell(region=central_shield_region)
inner_vessel_cell = openmc.Cell(region=inner_vessel_region)
first_wall_cell = openmc.Cell(region=first_wall_region)
breeder_blanket_cell = openmc.Cell(region=breeder_blanket_region)
# filling cells with materials
central_sol_cell.fill = copper_material
first_wall_cell.fill = eurofer_material
central_shield_cell.fill = eurofer_material
breeder_blanket_cell.fill = breeder_material

my_geometry = openmc.Geometry(
    [
        central_sol_cell,
        central_shield_cell,
        inner_vessel_cell,
        first_wall_cell,
        breeder_blanket_cell,
    ]
)

# source
# work with older versions of openmc
try:
    source = openmc.IndependentSource()
except:
    source = openmc.Source()
source.angle = openmc.stats.Isotropic()
source.energy = openmc.stats.Discrete([14e6], [1])
radius = openmc.stats.Discrete([150], [1])
z_values = openmc.stats.Discrete([300], [1])
angle = openmc.stats.Uniform(a=0.0, b=2 * 3.14159265359)
source.space = openmc.stats.CylindricalIndependent(
    r=radius, phi=angle, z=z_values, origin=(0.0, 0.0, 0.0)
)

# Instantiate a Settings object
my_settings = openmc.Settings()
my_settings.output = {"tallies": False}
my_settings.batches = 2
my_settings.particles = (
    50000  # increase this to 5000000 to make the same plot as the readme
)
my_settings.run_mode = "fixed source"
my_settings.source = source

# tallies
bb = my_geometry.bounding_box
wedge_length = 40  # set to 4 to make plot from readme
# this just makes the number of mesh voxels in each dimension proportional to the size of the geometry in that dimension.
# this means we get cube shaped voxels instead of stretched out rectangles
dimension = [
    int(bb.width[0] / wedge_length),
    int(bb.width[1] / wedge_length),
    int(bb.width[2] / wedge_length),
]
mesh = openmc.RegularMesh().from_domain(my_geometry, dimension=dimension)
mesh_filter = openmc.MeshFilter(mesh)
mesh_tally = openmc.Tally(name="mesh_tally")
mesh_tally.filters = [mesh_filter]
mesh_tally.scores = ["(n,Xt)"]  # tritium production
my_tallies = openmc.Tallies([mesh_tally])

model = openmc.Model(my_geometry, my_materials, my_settings, my_tallies)

statepoint_filename = model.run()

# makes use of a context manager "with" to automatically close the statepoint file
with openmc.StatePoint(statepoint_filename) as statepoint:
    my_mesh_tally_result = statepoint.get_tally(name="mesh_tally")

# set the same color range across all the plots
data = my_mesh_tally_result.mean.flatten()
lower_limit = np.min(data[np.nonzero(data)])
upper_limit = np.max(data[np.nonzero(data)])

for slice_index in range(0, mesh.dimension[1]):
    plot = plot_mesh_tally(
        tally=my_mesh_tally_result,
        basis="xz",
        slice_index=slice_index,
        outline=True,  # enables an outline around the geometry
        geometry=my_geometry,
        outline_by="cell",
        pixels=80000,  # double the default pixels to get a better resolution on the geometry outline curve
        outline_kwargs={
            "colors": "green",
            "linewidths": 2,
        },  # setting the outline color and thickness, otherwise this defaults to black and 1
        norm=LogNorm(vmin=lower_limit, vmax=upper_limit),  # log scale
        volume_normalization=False,
        # colorbar=False, removing color bar from plot
        cmap=cm.get_cmap("gnuplot"),  # color map contrasts with outline color
    )

    # adding a title to the plot
    plot.title.set_text(f"Slice {slice_index}.")
    plot.figure.savefig(f"plot_slice_index_{str(slice_index).zfill(4)}.png")

import os

os.system("convert -delay 20 plot_slice*.png animated_openmc_regular_mesh_tally.gif")
