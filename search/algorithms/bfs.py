"""
Breadth-first Search specialization of a generic search algorithm.
"""

from typing import Hashable

from search.algorithms.search import SearchAlgorithm, Node
from search.space import Space


class BFS(SearchAlgorithm):
    """Breadth-first Search.

    Implements Open with a List and a set.
    It uses the base Node class as we don't need to extend it.
    """
    class Open(SearchAlgorithm.Open):
        """An Open set implementation using a Queue."""

        def __init__(self):
            self.nodes = []
            self.states = set()

        def insert(self, node: Node):
            """Appends a Node into the Open list."""
            if node.state in self.states:
                # If the state was already in Open, then we know that this new
                # path to it is not better.
                return

            self.states.add(node.state)
            self.nodes.append(node)

        def pop(self) -> Node:
            """Takes the first (oldest) Node from the Open list."""
            node = self.nodes.pop(0)
            self.states.remove(node.state)
            return node

        def __len__(self) -> int:
            """Counts the Nodes in Open."""
            return len(self.nodes)

        def __bool__(self) -> bool:
            """Checks if there's Nodes in Open."""
            return len(self.nodes) > 0

    @classmethod
    def name(cls) -> str:
        """Returns the name of the Algorithm."""
        return "Breadth-first Search"

    @classmethod
    def create_open(cls) -> Open:
        """Returns the container to use for the Open set."""
        return BFS.Open()

    @classmethod
    def create_starting_node(cls, state: Hashable) -> Node:
        """Create an Starting Node."""
        return Node(state, action=None, parent=None)

    def reach(self, state: Hashable, action: Space.Action, parent: Node):
        """Reaches a state and updates Open."""
        node = Node(state, action, parent)

        self.open.insert(node)
