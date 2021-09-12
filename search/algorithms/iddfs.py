"""
Iterative deepening Depth-first Search specialization of a generic search algorithm.
"""

from typing import Optional

from search.algorithms.search import Node, SearchAlgorithm
from search.space import Space


class IDDFS(SearchAlgorithm):
    """Iterative deepening Depth-first Search."""

    def __init__(self, problem):
        super().__init__(problem)

    def __str__(self) -> str:
        """The string representation of this Node."""
        return "{}[]".format(
            self.__class__.__name__,
        )

    @classmethod
    def name(cls) -> str:
        """Returns the name of the Algorithm."""
        return "Iterative deepening Depth-first Search"

    # pylint: no-self-argument
    def create_starting_node(self, state: Space.State) -> Node:
        """Create an Starting Node."""
        self.nodes_created += 1
        return Node(state, action=None, parent=None)

    def _actually_search(self) -> Optional[Node]:
        """Finds a single goal Node."""
        return None
