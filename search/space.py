"""
Definitions for a Search Space and Search Problems over them.
"""

import copy
from enum import Enum
from typing import Iterable, Optional, Set, Tuple


class Space():
    """A generic search space."""

    class State():
        """A state in the Search Space."""

        def __hash__(self):
            """The hash of this state."""
            raise NotImplementedError("")

        def __str__(self) -> str:
            """The string representation of this state."""
            raise NotImplementedError("")

        def __eq__(self, other) -> bool:
            """Compares 2 states."""
            raise NotImplementedError(
                "The '{}' State does not implement __eq__ yet".format(
                    self.__class__))

    class Action(Enum):
        """A generic action."""

        # pylint: disable=unused-argument
        # pylint: disable=no-self-use
        def cost(self, state):
            """The cost of executing this action."""
            return 0

        def __str__(self) -> str:
            """The string representation of this action."""
            return str(self.value)

    def neighbors(self, state: State) -> Iterable[Tuple[Action, State]]:
        """The possible actions and their resulting State."""
        raise NotImplementedError("")

    def execute(self, state: State, action: Action) -> State:
        """Applies an action into some State.

        Reuses the neighbors(state) as this is not performance critical.
        """
        # pylint: disable=invalid-name
        for a, s in self.neighbors(state):
            if a == action:
                return copy.deepcopy(s)

        # Something is wrong, let's try to explain the current state.
        action_strs = [str(a) for a, _ in self.neighbors(state)]
        raise ValueError(
            "Received an action that can't be performed at this State. Can't perform {} from {}. Can only perform {}".format(action, state, ", ".join(action_strs)))

    def to_str(self, problem, state: State) -> str:
        """Formats a Problem over a Space to a string."""
        raise NotImplementedError(
            "The '{}' Space does not implement to_str yet".format(
                self.__class__))


class RandomAccessSpace(Space):
    """A generic Search Space where random States can be generated."""

    def random_state(self) -> Space.State:
        """Gets a random State with a Uniform distribution."""
        raise NotImplementedError("")


class PredefinedSpace(Space):
    """A search space with predefined start and goal states.

    Allows specifying problems for a given Space.
    """

    def predefined_starting_states(self) -> Iterable[Space.State]:
        """Generates starting states."""
        raise NotImplementedError("")

    def predefined_goal_states(self) -> Iterable[Space.State]:
        """Generates goal states."""
        raise NotImplementedError("")


class Problem():
    """A generic problem definition that uses a goal function."""

    def __init__(self, space: Space, starting_states: Set[Space.State]):
        self.space = space
        self.starting_states = starting_states

    def is_goal(self, state: Space.State) -> bool:
        """Checks if a state is a goal for this Problem."""
        raise NotImplementedError("")

    def to_str(self, state: Space.State) -> str:
        """The string representing some state over this Problem."""
        space_class = type(self.space)
        return space_class.to_str(problem=self, state=state)

    def start_to_str(self) -> str:
        """The string representing the starting states of this Problem."""
        if len(self.starting_states) == 0:
            raise RuntimeError("This problem does not have starting states.")

        if len(self.starting_states) == 1:
            unique_starting_state = next(iter(self.starting_states))
            return self.to_str(unique_starting_state)

        problem_str = "There's {} starting states,\n".format(
            len(self.starting_states))
        for starting_state in self.starting_states:
            problem_str += self.to_str(starting_state)
            problem_str += "\n"
        return problem_str


class SimpleProblem(Problem):
    """A simple problem implementation that has a Set of goal states."""

    def __init__(self,
                 space: Space,
                 starting_states: Set[Space.State],
                 fixed_goal_states: Set[Space.State]):
        super().__init__(space, starting_states)

        self.fixed_goal_states = fixed_goal_states

    def is_goal(self, state: Space.State):
        return state in self.fixed_goal_states

    # From PredefinedSpace
    @classmethod
    def simple_given(cls, space: PredefinedSpace):
        """Generates problems with a single start and goal."""
        for start in space.predefined_starting_states():
            for goal in space.predefined_goal_states():
                yield cls(space, set([start]), set([goal]))

    @classmethod
    def multi_goal_given(cls, space: PredefinedSpace):
        """Generates problems with a single start and all goals."""
        goals = set(space.predefined_goal_states())
        for start in space.predefined_starting_states():
            yield cls(space, set([start]), goals)

    @classmethod
    def multi_start_and_goal_given(cls, space: PredefinedSpace):
        """Generates problems with a all starts and goals."""
        return cls(space,
                   set(space.predefined_starting_states()),
                   set(space.predefined_goal_states()))

    # From RandomAccessSpace
    @classmethod
    def simple_random(cls, random_space: RandomAccessSpace):
        """Creates a random problem with a single start and goal."""
        start = random_space.random_state()
        goal = random_space.random_state()
        return cls(random_space, set([start]), set([goal]))
