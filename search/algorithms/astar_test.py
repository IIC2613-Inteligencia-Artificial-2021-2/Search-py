"""
Tests for A* Search algorithm.
"""

from typing import Optional

import pytest

from search.algorithms.astar import AStar
from search.algorithms.search import Node, SearchAlgorithm
from search.problems.grid.board2d import Grid2D, Grid2DMetaProblem
from search.space import Problem


@pytest.mark.skip(reason="AStar is not implemented yet.")
def test_no_solution():
    metaproblem = Grid2DMetaProblem(
        [
            "     ",
            " ####",
            "     ",
            "#### ",
            "     ",
            "S    ",
        ]
    )
    problem: Problem = next(iter(metaproblem.multi_goal_given()))
    # heuristic = Grid2DManhattanDistance(problem)
    astar: SearchAlgorithm = AStar(problem)

    # Search
    goal_node: Optional[Node] = astar.search()

    # A solution must be found
    assert goal_node is None
    # This maps needs to be completely expanded
    assert astar.expansions == 22
    assert 10_000 < astar.time_ns < 10_000_000


@pytest.mark.skip(reason="AStar is not implemented yet.")
def test_expansion_order():
    length = 100
    metaproblems = [
        Grid2DMetaProblem(
            [
                "G" + " " * length + "S" + " " * length,
            ]
        ),
        Grid2DMetaProblem(
            [
                " " * length + "S" + " " * length + "G",
            ]
        ),
    ]

    # pylint: disable=invalid-name
    for mp in metaproblems:
        problem: Problem = next(iter(mp.multi_goal_given()))
        # heuristic = Grid2DManhattanDistance(problem)
        astar: SearchAlgorithm = AStar(problem)

        # Search
        goal_node: Optional[Node] = astar.search()

        assert goal_node is not None
        assert goal_node.path(problem.space) is not None
        assert length < astar.expansions <= (length + 1)
        assert 100_000 < astar.time_ns < 100_000_000
        assert length < astar.states_reached <= length + 2
        assert (
            2 * length <= astar.states_generated <= 2 * (length + 1)
        )  # Expansions generate ~2 states
        assert astar.nodes_created == length + 3  # wrong way + s + length + goal
        assert astar.nodes_updated == 0  # The graph becomes a "tree" with Closed :/


@pytest.mark.skip(reason="AStar with tie-breaking is not implemented yet.")
def test_tie_breaking():
    state = Grid2D.State((0, 0))

    # pylint: disable=invalid-name
    # f = 5
    g1 = 3
    # h1 = f - g1
    node_1 = AStar.AStarNode(state, action=None, parent=None, g=g1)
    g2 = 2
    # h2 = f - g2
    node_2 = AStar.AStarNode(state, action=None, parent=None, g=g2)

    assert node_1 < node_2
