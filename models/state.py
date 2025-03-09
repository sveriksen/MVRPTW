"""
This module implements the State class which is used for search based solvers.
"""

from typing import FrozenSet, TYPE_CHECKING

if TYPE_CHECKING:
    from models.actions import Delivery

class State:
    """Implements the state class. Represents the state of a vehicle"""
    def __init__(self, node : int, time : float, commitments : FrozenSet["Delivery"]):
        self.node = node
        self.time = time
        self.commitments = commitments
