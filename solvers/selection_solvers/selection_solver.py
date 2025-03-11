"""
Abstract base class for selection-based solvers.

This module defines a framework for solvers that iteratively select:
1. A vehicle from the set of active vehicles.
2. An action from the possible actions of the selected vehicle.

Classes:
- SelectionSolver: Abstract base class with select_vehicle and select_action methods.
"""

from abc import abstractmethod
from typing import List, Tuple

from solvers.base_solver import Solver
from models import Action, Delivery, Vehicle

class SelectionSolver(Solver):
    """
    A family of solvers that differ only in how they choose vehicles and actions.

    TODO: Implement select_vehicle_action
    """

    @abstractmethod
    def select_vehicle_action(self, active_vehicles : List[Vehicle]) -> Tuple[Vehicle, Action]:
        """Selects a vehicle and action from the set of active vehicles."""

    def solve(self) -> List[List[Action]]:
        """Runs the selection-based solving process."""
        for vehicle in self.vehicles:
            vehicle.expand(self.unanswered_calls)

        while True:
            active_vehicles = self.get_active_vehicles()
            if not active_vehicles:
                break

            vehicle, action = self.select_vehicle_action(active_vehicles)
            vehicle.select(action)
            self.unanswered_calls.difference_update({action.call})
            vehicle.expand(self.unanswered_calls)

            if isinstance(action, Delivery):
                continue

            for vehicle in self.vehicles:
                if vehicle == vehicle:
                    continue

                vehicle.remove(action.call)

        return self.get_action_sequences()
