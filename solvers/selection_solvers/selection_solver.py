"""
Abstract base class for selection-based solvers.

This module defines a framework for solvers that iteratively select:
1. A vehicle from the set of active vehicles.
2. An action from the possible actions of the selected vehicle.

Classes:
- SelectionSolver: Abstract base class with select_vehicle and select_action methods.
"""


from typing import List
from abc import abstractmethod

from solvers.base_solver import Solver
from models import Action, Delivery, Vehicle

class SelectionSolver(Solver):
    """
    A family of solvers that differ only in how they choose vehicles and actions.

    TODO: Implement select_vehicle & select_action
    """

    @abstractmethod
    def select_vehicle(self, active_vehicles : List[Vehicle]) -> Vehicle:
        """Selects a vehicle from the set of active vehicles."""

    @abstractmethod
    def select_action(self, vehicle : Vehicle) -> Action:
        """Selects an action for the selected vehicle."""

    def solve(self) -> List[List[Action]]:
        """Runs the selection-based solving process."""
        for vehicle in self.vehicles:
            vehicle.expand(self.unanswered_calls)

        while True:
            active_vehicles = self.get_active_vehicles()
            if not active_vehicles:
                break

            selected_vehicle = self.select_vehicle(active_vehicles)
            selected_action = self.select_action(selected_vehicle)
            selected_vehicle.select(selected_action)
            self.unanswered_calls.difference_update({selected_action.call})
            selected_vehicle.expand(self.unanswered_calls)

            if isinstance(selected_action, Delivery):
                continue

            for vehicle in self.vehicles:
                if vehicle == selected_vehicle:
                    continue

                vehicle.remove(selected_action.call)

        return self.get_action_sequences()
