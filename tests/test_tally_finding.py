
import openmc
from regular_mesh_plotter import get_all_tallies_with_regular_mesh_filters


def test_tally_with_reg_mesh_finding():
    # checks the correct number of tally score combinations are found

    statepoint = openmc.StatePoint('statepoint.3.h5')

    # one tally has a cell filter and another one has a cylinder mesh filter
    assert len(statepoint.tallies) == 4

    t_and_scores = get_all_tallies_and_with_regular_mesh_filters(statepoint)
    assert t_and_scores == [3, 4]
