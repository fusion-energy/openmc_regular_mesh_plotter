import openmc
import regular_mesh_plotter


def test_simple_mesh():
    mesh = openmc.RegularMesh()
    mesh.lower_left = (-10, -10, -10)
    mesh.upper_right = (10, 10, 10)
    mesh.dimension = (10, 10, 10)

    assert (
        mesh.get_slice_axis_value_from_index(view_direction="x", slice_index=5) == 1.0
    )
    assert (
        mesh.get_slice_axis_value_from_index(view_direction="x", slice_index=4) == -1.0
    )
    assert (
        mesh.get_slice_axis_value_from_index(view_direction="y", slice_index=5) == 1.0
    )
    assert (
        mesh.get_slice_axis_value_from_index(view_direction="y", slice_index=4) == -1.0
    )
    assert (
        mesh.get_slice_axis_value_from_index(view_direction="z", slice_index=5) == 1.0
    )
    assert (
        mesh.get_slice_axis_value_from_index(view_direction="z", slice_index=4) == -1.0
    )

    mesh = openmc.RegularMesh()
    mesh.lower_left = (-5, -5, -5)
    mesh.upper_right = (5, 5, 5)
    mesh.dimension = (10, 10, 10)

    assert (
        mesh.get_slice_axis_value_from_index(view_direction="x", slice_index=5) == 0.5
    )
    assert (
        mesh.get_slice_axis_value_from_index(view_direction="x", slice_index=4) == -0.5
    )
    assert (
        mesh.get_slice_axis_value_from_index(view_direction="y", slice_index=5) == 0.5
    )
    assert (
        mesh.get_slice_axis_value_from_index(view_direction="y", slice_index=4) == -0.5
    )
    assert (
        mesh.get_slice_axis_value_from_index(view_direction="z", slice_index=5) == 0.5
    )
    assert (
        mesh.get_slice_axis_value_from_index(view_direction="z", slice_index=4) == -0.5
    )


def test_non_central_mesh():
    mesh = openmc.RegularMesh()
    mesh.lower_left = (0, 0, 0)
    mesh.upper_right = (10, 10, 10)
    mesh.dimension = (10, 10, 10)

    assert (
        mesh.get_slice_axis_value_from_index(view_direction="x", slice_index=5) == 5.5
    )
    assert (
        mesh.get_slice_axis_value_from_index(view_direction="x", slice_index=4) == 4.5
    )


def test_unequal_dimensions():
    mesh = openmc.RegularMesh()
    mesh.lower_left = (0, 0, 0)
    mesh.upper_right = (10, 10, 10)
    mesh.dimension = (1, 2, 4)

    assert (
        mesh.get_slice_axis_value_from_index(view_direction="x", slice_index=0) == 5.0
    )
    assert (
        mesh.get_slice_axis_value_from_index(view_direction="y", slice_index=0) == 2.5
    )
    assert (
        mesh.get_slice_axis_value_from_index(view_direction="z", slice_index=0) == 1.25
    )


# TODO
# def test_simple_mesh():

#     mesh = openmc.RegularMesh()
#     mesh.lower_left = (-10, -10, -10)
#     mesh.upper_right = (10, 10, 10)
#     mesh.dimension = (10, 10, 10)

#     assert get_slice_index_from_axis_value(view_direction='x', axis_value=-10) == 0
#     assert get_slice_index_from_axis_value(view_direction='y', axis_value=-10) == 0
#     assert get_slice_index_from_axis_value(view_direction='z', axis_value=-10) == 0

#     assert get_slice_index_from_axis_value(view_direction='x', axis_value=10) == 10
#     assert get_slice_index_from_axis_value(view_direction='y', axis_value=10) == 10
#     assert get_slice_index_from_axis_value(view_direction='z', axis_value=10) == 10

#     assert get_slice_index_from_axis_value(view_direction='x', axis_value=0.1) == 5
#     assert get_slice_index_from_axis_value(view_direction='y', axis_value=0.1) == 5
#     assert get_slice_index_from_axis_value(view_direction='z', axis_value=0.1) == 5

#     assert get_slice_index_from_axis_value(view_direction='x', axis_value=-0.1) == 4
#     assert get_slice_index_from_axis_value(view_direction='y', axis_value=-0.1) == 4
#     assert get_slice_index_from_axis_value(view_direction='z', axis_value=-0.1) == 4
