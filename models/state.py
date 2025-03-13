"""
This module implements the State class which is used for search based solvers.
"""

from typing import Dict, FrozenSet, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from models.actions import Action, Call, Delivery

class State:
    """Represents the state of a vehicle"""
    def __init__(
            self,
            node : int,
            time : float,
            commitments : FrozenSet["Delivery"],
            load : Optional[float] = None
    ):
        self.node = node
        self.time = time
        self.commitments = commitments
        self._load = load

        self.next_states : Dict["Action", "State"] = {}
        self.selected_action = None
        self.next_state = None

    def add_transition(self, action : "Action", next_state : "State"):
        """Adds (action, next_state) to self.next_states"""
        self.next_states[action] = next_state

    def select(self, action : "Action"):
        """Selects the provided action if in self.current_state.next_states"""
        if action not in self.next_states:
            raise ValueError(f"Provided action '{action}' not in the dictionary of next states")

        self.selected_action = action
        self.next_state = self.next_states[action]

    def remove(self, call: "Call"):
        """Removes all occurrences of call in the tree."""

        to_remove = [action for action in self.next_states if action.call == call]

        for action in to_remove:
            del self.next_states[action]

        for state in self.next_states.values():
            state.remove(call)

    @property
    def load(self) -> float:
        """Lazily computes and caches the load only if it was not explicitly provided."""
        if self._load is None:
            self._load = sum(d.call.size for d in self.commitments)
        return self._load

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"Node: {self.node}, Time: {self.time}, Commitments: {self.commitments}"
