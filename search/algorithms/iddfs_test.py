"""
Tests for the Breadth-first Search algorithm.
"""

from typing import Optional

import pytest  # type: ignore

from search.algorithms.iddfs import IDDFS
from search.algorithms.search import Node, SearchAlgorithm
from search.problems.grid.board2d import Grid2DMetaProblem
from search.space import Problem


@pytest.mark.skip(reason="IDDFS is not implemented yet.")
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
    iddfs: SearchAlgorithm = IDDFS(problem)

    # Search
    goal_node: Optional[Node] = iddfs.search()

    # A solution must not be found
    assert goal_node is None

    # This maps needs to be completely expanded
    assert iddfs.expansions == 22
    assert 10_000 < iddfs.time_ns < 10_000_000


@pytest.mark.skip(reason="IDDFS is not implemented yet.")
def test_solution():
    metaproblem = Grid2DMetaProblem(
        [
            "    G",
            " ####",
            "     ",
            "#### ",
            "     ",
            "S    ",
        ]
    )
    problem: Problem = next(iter(metaproblem.multi_goal_given()))
    iddfs: SearchAlgorithm = IDDFS(problem)

    # Search
    goal_node: Optional[Node] = iddfs.search()

    # A solution must be found
    assert goal_node is not None

    # We can get its path
    path = goal_node.path(problem.space)
    assert path is not None

    # And it should be optimal.
    assert path.cost() == 17

    # The map is more than completely expanded.
    assert iddfs.expansions > 21
    # It  might need more time
    assert 100_000 < iddfs.time_ns < 10_000_000


@pytest.mark.skip(reason="IDDFS is not implemented yet.")
def test_expansion_order():
    length = 100
    metaproblem = Grid2DMetaProblem(
        [
            "G" + " " * length + "S" + " " * length,
        ]
    )
    problem: Problem = next(iter(metaproblem.multi_goal_given()))
    iddfs: SearchAlgorithm = IDDFS(problem)

    # Search
    goal_node: Optional[Node] = iddfs.search()

    assert goal_node is not None
    assert goal_node.path(problem.space) is not None
    # It needs more expansions than BFS
    assert 2 * (length + 1) < iddfs.expansions
    # It  might need more time on slow puzzles.
    assert 100_000 < iddfs.time_ns < 100_000_000
