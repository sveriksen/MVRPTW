"""
This module implements the State class which is used for search based solvers.
"""

from typing import Dict, FrozenSet, Optional, List, TYPE_CHECKING

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
        self.load = load if load is not None else sum(d.call.size for d in commitments)

        self.next_states : Dict["Action", "State"] = {}
        self.selected_action = None
        self.next_state = None

    def delete_children(self):
        """Deletes all children recursively. Resets selected_action and next_state."""
        for next_state in self.next_states.values():
            next_state.delete_children()

        self.next_states.clear()
        self.selected_action = None
        self.next_state = None

    def action_sequence(self) -> List["Action"]:
        """
        Returns the sequence of actions from this state, to the final \\
        state with no selected action.
        """
        if self.selected_action is None:
            return []

        return [self.selected_action] + self.next_state.action_sequence()

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

        for next_state in self.next_states.values():
            next_state.remove(call)

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"Node: {self.node}, Time: {self.time}, Commitments: {self.commitments}"
