"""
This module implements the State class which is used for search based solvers.
"""

from typing import Dict, FrozenSet, TYPE_CHECKING

if TYPE_CHECKING:
    from models.actions import Action, Delivery

class State:
    """Represents the state of a vehicle"""
    def __init__(
            self,
            node : int,
            time : float,
            commitments : FrozenSet["Delivery"]
    ):
        self.node = node
        self.time = time
        self.commitments = commitments

        self.next_states : Dict[Action, State] = {}
        self.selected_action = None

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"Node: {self.node}, Time: {self.time}, Commitments: {self.commitments}"
