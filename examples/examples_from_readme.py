# this examples requires additional python packages

from dagmc_geometry_slice_plotter import plot_slice_of_dagmc_geometry
from stl_to_h5m import stl_to_h5m

import paramak

my_reactor = paramak.SubmersionTokamak(
    inner_bore_radial_thickness=30,
    inboard_tf_leg_radial_thickness=30,
    center_column_shield_radial_thickness=30,
    divertor_radial_thickness=80,
    inner_plasma_gap_radial_thickness=50,
    plasma_radial_thickness=200,
    outer_plasma_gap_radial_thickness=50,
    firstwall_radial_thickness=30,
    blanket_rear_wall_radial_thickness=30,
    number_of_tf_coils=16,
    rotation_angle=360,
    support_radial_thickness=90,
    inboard_blanket_radial_thickness=30,
    outboard_blanket_radial_thickness=30,
    elongation=2.00,
    triangularity=0.50,
    pf_coil_case_thicknesses=[10, 10, 10, 10],
    pf_coil_radial_thicknesses=[20, 50, 50, 20],
    pf_coil_vertical_thicknesses=[20, 50, 50, 20],
    pf_coil_radial_position=[500, 550, 550, 500],
    pf_coil_vertical_position=[270, 100, -100, -270],
    rear_blanket_to_tf_gap=50,
    outboard_tf_coil_radial_thickness=30,
    outboard_tf_coil_poloidal_thickness=30,
)


stl_filenames = my_reactor.export_stl()


stl_to_h5m(
    files_with_tags=[
        (stl_filename, name)
        for name, stl_filename in zip(my_reactor.name, stl_filenames)
    ],
    h5m_filename="dagmc.h5m",
)


plot = plot_slice_of_dagmc_geometry(
    dagmc_file_or_trimesh_object="dagmc.h5m",
    plane_normal=[0, 0, 1],
    output_filename="my_plot1.png",
)


plot = plot_slice_of_dagmc_geometry(
    dagmc_file_or_trimesh_object="dagmc.h5m",
    plane_origin=[0, 0, 300],
    plane_normal=[0, 0, 1],
    output_filename="my_plot2.png",
)


plot = plot_slice_of_dagmc_geometry(
    dagmc_file_or_trimesh_object="dagmc.h5m",
    plane_normal=[0, 1, 0],
    rotate_plot=45,
    output_filename="my_plot3.png",
)

plot.savefig("big.png", dpi=600)

plot_slice_of_dagmc_geometry(
    dagmc_file_or_trimesh_object="dagmc.h5m",
    plane_normal=[1, 0, 0],
    rotate_plot=270,
    output_filename="my_plot4.png",
)
