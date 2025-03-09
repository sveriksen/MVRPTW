"""[SEARCH-BASED VEHICLE MODEL]"""

from dataclasses import dataclass
from typing import FrozenSet, TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from state import State
    from actions import Call


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
        spec (VehicleSpec): Basic vehicle attributes.
        state (VehicleState): Current state (position, time, commitments).
        costs (VehicleCosts): Cost data for travel and services.
        times (VehicleTimes): Time data for travel and services.
    """

    def __init__(
        self,
        state: "State",
        specs: VehicleSpecs,
        costs: VehicleCosts,
        times: VehicleTimes,
    ):
        """
        Initializes a Vehicle instance.

        Args:
            state (State): Initial state of the vehicle.
            spec (VehicleSpec): Basic vehicle attributes.
            costs (VehicleCosts): Encapsulates travel and service costs.
            times (VehicleTimes): Encapsulates travel and service times.
        """
        self.state = state
        self.specs = specs
        self.costs = costs
        self.times = times

        self._hash = hash(self.specs.idx)

    def __eq__(self, other : object) -> bool:
        if not isinstance(other, Vehicle):
            return False
        return self.specs.idx == other.specs.idx

    def __hash__(self) -> int:
        return self._hash

    def __str__(self) -> str:
        return f"Vehicle-{self.specs.idx}"
