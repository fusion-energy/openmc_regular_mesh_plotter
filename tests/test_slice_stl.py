import unittest

import trimesh
from regular_mesh_plotter import plot_stl_slice


class TestShape(unittest.TestCase):
    def setUp(self):

        self.mesh = trimesh.load_mesh("tests/example.stl", process=False)

    def test_z_axis_slice(self):

        plot_stl_slice(self.mesh, plane_normal=[0, 0, 1])

    def test_offset_z_axis_slice(self):

        plot_stl_slice(self.mesh, plane_origin=[0, 0, 10], plane_normal=[0, 0, 1])

    def test_x_axis_slice(self):

        plot_stl_slice(self.mesh, plane_normal=[1, 0, 0])

    def test_offset_x_axis_slice(self):

        plot_stl_slice(self.mesh, plane_origin=[10, 0, 0], plane_normal=[1, 0, 0])
