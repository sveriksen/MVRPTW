"""[SEARCH-BASED VEHICLE MODEL]"""

from dataclasses import dataclass
from typing import FrozenSet, Set, Union, List

import numpy as np

from models.state import State
from models.actions import Action, Call
from models.actions import Delivery, Pickup


@dataclass(frozen=True)
class VehicleSpecs:
    """Encapsulates basic vehicle attributes."""
    idx: int
    capacity: float
    compatible_calls: FrozenSet["Call"]


@dataclass(frozen=True)
class VehicleCosts:
    """Encapsulates vehicle travel and service costs."""
    travel_costs: np.ndarray
    service_costs: np.ndarray


@dataclass(frozen=True)
class VehicleTimes:
    """Encapsulates vehicle travel and service times."""
    travel_times: np.ndarray
    service_times: np.ndarray


class Vehicle:
    """
    Represents a vehicle in a scheduling or routing system with search-based state tracking.

    Attributes:
        initial_state (VehicleState): Initial state (position, time, commitments).
        specs (VehicleSpec): Basic vehicle attributes.
        costs (VehicleCosts): Cost data for travel and services.
        times (VehicleTimes): Time data for travel and services.
    """

    def __init__(
        self,
        initial_state: "State",
        specs: VehicleSpecs,
        costs: VehicleCosts,
        times: VehicleTimes,
    ):
        """
        Initializes a Vehicle instance.

        Args:
            initial_state (State): Initial state of the vehicle.
            spec (VehicleSpec): Basic vehicle attributes.
            costs (VehicleCosts): Encapsulates travel and service costs.
            times (VehicleTimes): Encapsulates travel and service times.
        """
        self.initial_state = initial_state
        self.current_state = initial_state
        self.route_length = 0

        self.specs = specs
        self.costs = costs
        self.times = times

        self._hash = hash(self.specs.idx)

    def reset(self):
        """Resets search tree, and sets current_state to initial_state"""
        self.initial_state.delete_children()
        self.current_state = self.initial_state
        self.route_length = 0

    def select(self, action : "Action"):
        """Selects the provided action if in self.current_state.next_states"""
        self.current_state.select(action)
        self.current_state = self.current_state.next_state
        self.route_length += 1

    def remove(self, call : "Call"):
        """Removes all occurances of this call in this vehicle's state tree"""
        self.initial_state.remove(call)

    def expand(self, unanswered_calls : Set["Call"]):
        """Expands the search tree by computing feasible next states"""
        potential_actions = []

        for delivery in self.current_state.commitments:
            if delivery in self.current_state.next_states:
                continue
            potential_actions.append(delivery)

        for pickup in {c.pickup for c in self.specs.compatible_calls & unanswered_calls}:
            if pickup in self.current_state.next_states:
                continue
            potential_actions.append(pickup)

        for action in potential_actions:
            resulting_state = self.perform(action)
            if resulting_state is None:
                continue

            self.current_state.next_states[action] = resulting_state

    def perform(self, action : "Action") -> Union["State", None]:
        """
        Simulates performing an action. Returns the resulting state.\n
        If it is not possible for this vehicle to perform the action, we return None.
        """
        def get_new_time() -> Union[float, None]:
            arrival_time = self.current_state.time + \
                           self.times.travel_times[self.current_state.node, action.node]
            if arrival_time > action.latest_time:
                return None

            new_time = max(arrival_time, action.earliest_time) + \
                       self.times.service_times[action.call_idx, action.action_idx]

            return new_time

        new_time = get_new_time()
        if new_time is None:
            return None

        new_node = action.node
        new_load = self.current_state.load + action.load_delta

        if isinstance(action, Pickup):
            if action.call not in self.specs.compatible_calls:
                return None
            new_commitments = self.current_state.commitments.union({action.delivery})
            new_state = State(new_node, new_time, new_commitments, load=new_load)

        elif isinstance(action, Delivery):
            if action not in self.current_state.commitments:
                return None
            new_commitments = self.current_state.commitments.difference({action})
            new_state = State(new_node, new_time, new_commitments, load=new_load)

        else:
            raise ValueError(f"Provided action '{action}' not feasible for this vehicle '{self}'.")

        if not self.is_feasible(new_state):
            return None

        return new_state

    def is_feasible(self, state : "State") -> bool:
        """Returns True if this vehicle can deliver all provided commitments."""
        commitments = state.commitments

        if not commitments:
            return True

        sorted_commitments = sorted(
            commitments,
            key = lambda delivery : delivery.latest_time
        )

        for i, delivery in enumerate(sorted_commitments):
            new_load = state.load + delivery.load_delta
            if new_load > self.specs.capacity:
                continue

            travel_time = self.times.travel_times[state.node][delivery.node]
            arrival_time = state.time + travel_time

            if arrival_time > delivery.latest_time:
                continue

            wait_time = max(0.0, delivery.earliest_time - arrival_time)
            service_time = self.times.service_times[delivery.call_idx][1]
            new_time = arrival_time + wait_time + service_time

            remaining_commitments = frozenset(sorted_commitments[:i] + sorted_commitments[i+1:])

            new_state = State(delivery.node, new_time, remaining_commitments, load=new_load)

            if self.is_feasible(new_state):
                return True

        return False

    @property
    def action_sequence(self) -> List["Action"]:
        """
        Returns the sequence of actions from the initial node to the \\
        final node with no selected action.
        """
        return self.initial_state.action_sequence()

    @property
    def cost(self) -> float:
        """Calculates total cost for this vehicle's assigned actions."""
        total_cost = 0.0
        current_node = self.initial_state.node

        for action in self.action_sequence:
            total_cost += self.costs.travel_costs[current_node, action.node]
            total_cost += self.costs.service_costs[action.call_idx, action.action_idx]
            total_cost -= action.call.void_cost / 2
            current_node = action.node

        return total_cost

    def __eq__(self, other : object) -> bool:
        if not isinstance(other, Vehicle):
            return False
        return self.specs.idx == other.specs.idx

    def __hash__(self) -> int:
        return self._hash

    def __str__(self) -> str:
        return f"Vehicle-{self.specs.idx}"
