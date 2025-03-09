"""
This module implements a base Action class, which is inherited by Pickup and Delivery.
It also defines the Call class, which represents a request or task.

Classes:
- Action: Abstract base class for an action (pickup or delivery).
- Pickup: Represents the pickup action.
- Delivery: Represents the delivery action.
- Call: Represents a task with a pickup and delivery action.
"""

from abc import ABC
from weakref import ref
from typing import Literal


class Action(ABC):
    """
    Abstract base class for actions (Pickup or Delivery).

    Attributes:
        action_idx (Literal[0, 1]): 0 for Pickup, 1 for Delivery.
        node_idx (int): The node where the action takes place.
        earliest_time (float): Earliest allowed time for the action.
        latest_time (float): Latest allowed time for the action.
        _call (weakref.ref or None): Weak reference to the linked Call object.
        _hash (int or None): Hash value for the action.
        _load_delta (float or None): Load change caused by the action.
    """

    def __init__(
        self,
        action_idx: Literal[0, 1],
        node_idx: int,
        earliest_time: float,
        latest_time: float
    ):
        """
        Initializes an Action.

        Args:
            action_idx (Literal[0, 1]): Either 0 (Pickup) or 1 (Delivery).
            node_idx (int): The index of the node where the action occurs.
            earliest_time (float): The earliest possible time to execute the action.
            latest_time (float): The latest possible time to execute the action.

        Raises:
            ValueError: If action_idx is not 0 or 1.
            ValueError: If earliest_time > latest_time.
        """
        if action_idx not in [0, 1]:
            raise ValueError(f"'action_idx' must be 0 (Pickup) or 1 (Delivery), got {action_idx}.")

        if earliest_time > latest_time:
            raise ValueError(f"'earliest_time' ({earliest_time}) cannot be "
                             f"greater than 'latest_time' ({latest_time}).")

        self.action_idx = action_idx
        self.node_idx = node_idx
        self.earliest_time = earliest_time
        self.latest_time = latest_time

        self._call = None  # Weak reference to Call
        self._hash = None
        self._load_delta = None

    def link_call(self, call: "Call"):
        """
        Links a Call object to this action.

        Args:
            call (Call): The Call object to link.
        """

        self._call = ref(call)
        self._hash = hash((call.idx << 1) | self.action_idx)
        self._load_delta = call.size if self.action_idx == 0 else -call.size

    @property
    def call_idx(self) -> int:
        """Returns the index of the linked Call."""
        if self._call is None:
            raise ValueError("Action is not linked to a Call.")
        return self.call.idx

    @property
    def call(self) -> "Call":
        """Returns the Call object linked to this action."""
        if self._call is None:
            raise ValueError("Action is not linked to a Call.")
        return self._call()

    @property
    def load_delta(self) -> float:
        """Returns the load change caused by the action."""
        if self._load_delta is None:
            raise ValueError("Action is not linked to a Call. Cannot access call size.")
        return self._load_delta

    def __eq__(self, other : object) -> bool:
        if not isinstance(other, Action):
            return False
        return self._hash == other._hash

    def __hash__(self) -> int:
        if self._hash is None:
            raise ValueError("Hash is not set. Ensure action is linked to a Call.")
        return self._hash

    def __repr__(self) -> str:
        return (
            f"Call-{self.call_idx} - {self.__class__.__name__} "
            f"- [{self.earliest_time}, {self.latest_time}]"
        )

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.call_idx})"


class Pickup(Action):
    """Represents picking up a Call. Inherits from Action."""

    def __init__(self, node_idx: int, earliest_time: float, latest_time: float):
        """
        Args:
            node_idx (int): The node index where the pickup occurs.
            earliest_time (float): Earliest allowed time for pickup.
            latest_time (float): Latest allowed time for pickup.
        """
        super().__init__(0, node_idx, earliest_time, latest_time)


class Delivery(Action):
    """Represents the delivery of a Call. Inherits from Action."""

    def __init__(self, node_idx: int, earliest_time: float, latest_time: float):
        """
        Args:
            node_idx (int): The node index where the delivery occurs.
            earliest_time (float): Earliest allowed time for delivery.
            latest_time (float): Latest allowed time for delivery.
        """
        super().__init__(1, node_idx, earliest_time, latest_time)


class Call:
    """
    Represents a request/task consisting of a Pickup and a Delivery action.

    Attributes:
        idx (int): Unique identifier for the call.
        size (float): The size of the request.
        void_cost (float): Cost incurred if the call is not completed.
        pickup (Pickup): The associated Pickup action.
        delivery (Delivery): The associated Delivery action.
    """

    def __init__(self, idx: int, size: float, void_cost: float, pickup: Pickup, delivery: Delivery):
        """
        Initializes a Call instance.

        Args:
            idx (int): Unique identifier for the call.
            size (float): The size of the request.
            void_cost (float): Cost incurred if the call is not completed.
            pickup (Pickup): The associated Pickup action.
            delivery (Delivery): The associated Delivery action.
        """
        self.idx = idx
        self.size = size
        self.void_cost = void_cost
        self.pickup = pickup
        self.delivery = delivery

        self.pickup.link_call(self)
        self.delivery.link_call(self)

        self._hash = hash(self.idx)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Call):
            return False
        return self.idx == other.idx

    def __hash__(self) -> int:
        return self._hash

    def __str__(self) -> str:
        return f"Call-{self.idx}"
