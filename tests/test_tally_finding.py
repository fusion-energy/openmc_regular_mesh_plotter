import openmc
from regular_mesh_plotter import (
    get_tallies_with_regular_mesh_filters,
    get_regularmesh_tallies_and_scores,
)


def test_tally_with_reg_mesh_finding():
    # checks the correct number of tally score combinations are found

    statepoint = openmc.StatePoint("statepoint.3.h5")

    # one tally has a cell filter and another one has a cylinder mesh filter
    assert len(statepoint.tallies) == 4

    t_and_scores = get_tallies_with_regular_mesh_filters(statepoint)
    assert t_and_scores == [3, 4]


def test_get_regularmesh_tallies_and_scores():
    statepoint = openmc.StatePoint("statepoint.3.h5")

    t_and_c = get_regularmesh_tallies_and_scores(statepoint)

    assert t_and_c == [
        {"id": 3, "name": "tallies_on_regmesh_absorption", "score": "absorption"},
        {"id": 4, "name": "tallies_on_regmesh_flux_and_heating", "score": "flux"},
        {"id": 4, "name": "tallies_on_regmesh_flux_and_heating", "score": "heating"},
    ]
