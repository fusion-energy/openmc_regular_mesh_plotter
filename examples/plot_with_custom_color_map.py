# this example is used to make the animation in the readme.
# It is also set up to accept any geometry and the mesh tally will adapt to the geometry dimensions


import openmc
from matplotlib.colors import LogNorm
from openmc_regular_mesh_plotter import plot_mesh_tally
from matplotlib import cm
import matplotlib.pyplot as plt


# materials
mat_concrete = openmc.Material()
mat_concrete.add_element("H", 0.168759)
mat_concrete.add_element("C", 0.001416)
mat_concrete.add_element("O", 0.562524)
mat_concrete.add_element("Na", 0.011838)
mat_concrete.add_element("Mg", 0.0014)
mat_concrete.add_element("Al", 0.021354)
mat_concrete.add_element("Si", 0.204115)
mat_concrete.add_element("K", 0.005656)
mat_concrete.add_element("Ca", 0.018674)
mat_concrete.add_element("Fe", 0.00426)
mat_concrete.set_density("g/cm3", 0.5)
my_materials = openmc.Materials([mat_concrete])

# geometry
width_a = 100
width_b = 200
width_c = 500
width_d = 250
width_e = 200
width_f = 200
width_g = 100
depth_a = 100
depth_b = 200
depth_c = 700
depth_d = 600
depth_e = 200
depth_f = 100
height_j = 10
height_k = 50
height_l = 10
xplane_0 = openmc.XPlane(x0=0, boundary_type="vacuum")
xplane_1 = openmc.XPlane(x0=xplane_0.x0 + width_a)
xplane_2 = openmc.XPlane(x0=xplane_1.x0 + width_b)
xplane_3 = openmc.XPlane(x0=xplane_2.x0 + width_c)
xplane_4 = openmc.XPlane(x0=xplane_3.x0 + width_d)
xplane_5 = openmc.XPlane(x0=xplane_4.x0 + width_e)
xplane_6 = openmc.XPlane(x0=xplane_5.x0 + width_f)
xplane_7 = openmc.XPlane(x0=xplane_6.x0 + width_g, boundary_type="vacuum")
yplane_0 = openmc.YPlane(y0=0, boundary_type="vacuum")
yplane_1 = openmc.YPlane(y0=yplane_0.y0 + depth_a)
yplane_2 = openmc.YPlane(y0=yplane_1.y0 + depth_b)
yplane_3 = openmc.YPlane(y0=yplane_2.y0 + depth_c)
yplane_4 = openmc.YPlane(y0=yplane_3.y0 + depth_d)
yplane_5 = openmc.YPlane(y0=yplane_4.y0 + depth_e)
yplane_6 = openmc.YPlane(y0=yplane_5.y0 + depth_f, boundary_type="vacuum")
zplane_1 = openmc.ZPlane(z0=0, boundary_type="vacuum")
zplane_2 = openmc.ZPlane(z0=zplane_1.z0 + height_j)
zplane_3 = openmc.ZPlane(z0=zplane_2.z0 + height_k)
zplane_4 = openmc.ZPlane(z0=zplane_3.z0 + height_l, boundary_type="vacuum")
outside_left_region = (
    +xplane_0 & -xplane_1 & +yplane_1 & -yplane_5 & +zplane_1 & -zplane_4
)
wall_left_region = +xplane_1 & -xplane_2 & +yplane_2 & -yplane_4 & +zplane_2 & -zplane_3
wall_right_region = (
    +xplane_5 & -xplane_6 & +yplane_2 & -yplane_5 & +zplane_2 & -zplane_3
)
wall_top_region = +xplane_1 & -xplane_4 & +yplane_4 & -yplane_5 & +zplane_2 & -zplane_3
outside_top_region = (
    +xplane_0 & -xplane_7 & +yplane_5 & -yplane_6 & +zplane_1 & -zplane_4
)
wall_bottom_region = (
    +xplane_1 & -xplane_6 & +yplane_1 & -yplane_2 & +zplane_2 & -zplane_3
)
outside_bottom_region = (
    +xplane_0 & -xplane_7 & +yplane_0 & -yplane_1 & +zplane_1 & -zplane_4
)
wall_middle_region = (
    +xplane_3 & -xplane_4 & +yplane_3 & -yplane_4 & +zplane_2 & -zplane_3
)
outside_right_region = (
    +xplane_6 & -xplane_7 & +yplane_1 & -yplane_5 & +zplane_1 & -zplane_4
)
room_region = +xplane_2 & -xplane_3 & +yplane_2 & -yplane_4 & +zplane_2 & -zplane_3
gap_region = +xplane_3 & -xplane_4 & +yplane_2 & -yplane_3 & +zplane_2 & -zplane_3
corridor_region = +xplane_4 & -xplane_5 & +yplane_2 & -yplane_5 & +zplane_2 & -zplane_3
roof_region = +xplane_1 & -xplane_6 & +yplane_1 & -yplane_5 & +zplane_1 & -zplane_2
floor_region = +xplane_1 & -xplane_6 & +yplane_1 & -yplane_5 & +zplane_3 & -zplane_4
outside_left_cell = openmc.Cell(region=outside_left_region)
outside_right_cell = openmc.Cell(region=outside_right_region)
outside_top_cell = openmc.Cell(region=outside_top_region)
outside_bottom_cell = openmc.Cell(region=outside_bottom_region)
wall_left_cell = openmc.Cell(region=wall_left_region, fill=mat_concrete)
wall_right_cell = openmc.Cell(region=wall_right_region, fill=mat_concrete)
wall_top_cell = openmc.Cell(region=wall_top_region, fill=mat_concrete)
wall_bottom_cell = openmc.Cell(region=wall_bottom_region, fill=mat_concrete)
wall_middle_cell = openmc.Cell(region=wall_middle_region, fill=mat_concrete)
room_cell = openmc.Cell(region=room_region)
gap_cell = openmc.Cell(region=gap_region)
corridor_cell = openmc.Cell(region=corridor_region)
roof_cell = openmc.Cell(region=roof_region, fill=mat_concrete)
floor_cell = openmc.Cell(region=floor_region, fill=mat_concrete)
my_geometry = openmc.Geometry(
    [
        outside_bottom_cell,
        outside_top_cell,
        outside_left_cell,
        outside_right_cell,
        wall_left_cell,
        wall_right_cell,
        wall_top_cell,
        wall_bottom_cell,
        wall_middle_cell,
        room_cell,
        gap_cell,
        corridor_cell,
        roof_cell,
        floor_cell,
    ]
)

# settings
# location of the point source
source_x = width_a + width_b + width_c * 0.5
source_y = depth_a + depth_b + depth_c * 0.75
source_z = height_j + height_k * 0.5
space = openmc.stats.Point((source_x, source_y, source_z))
angle = openmc.stats.Isotropic()
# all (100%) of source particles are 2.5MeV energy
energy = openmc.stats.Discrete([2.5e6], [1.0])

# work with older versions of openmc
try:
    source = openmc.IndependentSource(space=space, angle=angle, energy=energy)
except:
    source = openmc.Source(space=space, angle=angle, energy=energy)
source.particle = "neutron"
# Instantiate a Settings object
my_settings = openmc.Settings()
my_settings.output = {"tallies": False}
my_settings.batches = 2
my_settings.particles = 50  # set this to 500000000 to get a full image
my_settings.run_mode = "fixed source"
my_settings.source = source

# tallies
bb = my_geometry.bounding_box
wedge_length = 10
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
mesh_tally.scores = ["flux"]
my_tallies = openmc.Tallies([mesh_tally])

model = openmc.Model(my_geometry, my_materials, my_settings, my_tallies)

statepoint_filename = model.run()

# makes use of a context manager "with" to automatically close the statepoint file
with openmc.StatePoint(statepoint_filename) as statepoint:
    my_mesh_tally_result = statepoint.get_tally(name="mesh_tally")

# makes a discrete color map from a Perceptually Uniform Sequential colormap
cmap = cm.get_cmap(
    "viridis", 11
)  # gets 10 discrete colors as we have 10 ticks on the colorbar this should match up

plot = plot_mesh_tally(
    tally=my_mesh_tally_result,
    basis="xy",
    # slice_index,  # middle value of slice selected automatically, but you can set the slide index if preferred
    axis_units="m",  # set to meters otherwise this defaults to cm
    value="mean",  # set to mean but could also be set to std_dev
    outline=True,  # enables an outline around the geometry
    geometry=my_geometry,
    outline_by="material",
    colorbar_kwargs={
        "label": "Neutron Flux",  # labels support latex formatting
        "ticks": [1e-2, 1e-1, 1, 1e1, 1e2, 1e3, 1e4, 1e5, 1e6, 1e7, 1e8],
    },
    outline_kwargs={
        "colors": "darkgrey",
        "linewidths": 2,
    },  # setting the outline color and thickness, otherwise this defaults to black and 1
    norm=LogNorm(vmin=1e-2, vmax=1e8),  # log scale
    scaling_factor=1e10,  # multiplies the tally result by scaling_factor which is source strength (neutrons per second)
    volume_normalization=True,
    cmap=cmap,
)

plot.figure.savefig(f"plot_custom_color_map.png")
plot.title.set_text("Example regular mesh plot with outline geometry.")
