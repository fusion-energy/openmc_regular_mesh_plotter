import os
import unittest
from pathlib import Path

import numpy as np
from regular_mesh_plotter import plot_regular_mesh_values


class TestPlotRegularMeshValues(unittest.TestCase):
    def setUp(self):
        self.values = np.array(
            [
                [
                    1.64565869e09,
                    2.59505642e09,
                    3.06732422e09,
                    2.64141597e09,
                    1.76520128e09,
                    2.14909584e09,
                    3.70513916e09,
                    4.99737560e09,
                    3.86795536e09,
                    2.21272467e09,
                ],
                [
                    2.92406594e09,
                    5.91396360e09,
                    9.39595883e09,
                    5.94102629e09,
                    2.78174231e09,
                    3.47563407e09,
                    1.02570496e10,
                    2.50416310e10,
                    1.01248003e10,
                    3.34937674e09,
                ],
                [
                    3.99684099e09,
                    1.72147289e10,
                    3.68431465e11,
                    1.64968908e10,
                    3.74168705e09,
                    3.90640820e09,
                    1.65505774e10,
                    3.66837062e11,
                    1.65568070e10,
                    3.65646431e09,
                ],
                [
                    3.27796129e09,
                    1.01456714e10,
                    2.45757058e10,
                    1.00180127e10,
                    3.45105436e09,
                    2.63214911e09,
                    5.95924816e09,
                    9.43589769e09,
                    5.71740137e09,
                    2.75163850e09,
                ],
                [
                    2.37324680e09,
                    3.77339226e09,
                    5.01889988e09,
                    3.58500172e09,
                    2.16754228e09,
                    1.81599509e09,
                    2.57229036e09,
                    3.09622197e09,
                    2.50136006e09,
                    1.72280196e09,
                ],
            ]
        )

    def test_plot_regular_mesh_values(self):
        plot_regular_mesh_values(values=self.values)

    def test_plot_regular_mesh_values_with_output(self):
        os.system("rm test.png")

        plot_regular_mesh_values(values=self.values, filename="test.png")

        assert Path("test.png").is_file()

    def test_plot_regular_mesh_values_with_custom_colorbar(self):
        """Checks that other parameters can be used such as cmap"""

        os.system("rm test.png")

        plot_regular_mesh_values(values=self.values, filename="test.png", cmap="jet")

        assert Path("test.png").is_file()
