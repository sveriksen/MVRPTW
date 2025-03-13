"""DOCSTRING"""

from abc import abstractmethod
from typing import List, Tuple

from solvers.base_solver import Solver
from models import Action, Delivery, Vehicle

class SearchSolver(Solver):
    """
    TODO:\n
    initialize_search_tree\n
    expand_vehicle_search_tree\n
    select_vehicle_action\n
    remove_answered_call
    """

    @abstractmethod
    def initialize_search_tree(self, vehicle : "Vehicle"):
        """Initializes vehicle's search tree"""

    @abstractmethod
    def expand_vehicle_search_tree(self, selected_vehicle : Vehicle):
        """Expands the search tree of the selected vehicle"""

    @abstractmethod
    def select_vehicle_action(self, active_vehicles : List[Vehicle]) -> Tuple[Vehicle, Action]:
        """Selects a vehicle and action from the set of active vehicles."""

    @abstractmethod
    def remove_answered_call(self, selected_vehicle : "Vehicle", selected_action : "Action"):
        """Removes the call of the selected action from all vehicles except selected vehicle"""

    def initialize_search_trees(self):
        """Initializes the search tree for each vehicle"""
        for vehicle in self.vehicles:
            self.initialize_search_tree(vehicle)

    def solve(self) -> List[List[Action]]:
        """Runs the selection-based solving process."""
        self.initialize_search_trees()

        while True:
            active_vehicles = self.get_active_vehicles()

            if not active_vehicles:
                break

            selected_vehicle, selected_action = self.select_vehicle_action(active_vehicles)
            selected_vehicle.select(selected_action)
            self.unanswered_calls.difference_update({selected_action.call})
            self.expand_vehicle_search_tree(selected_vehicle)

            if isinstance(selected_action, Delivery):
                continue

            self.remove_answered_call(selected_vehicle, selected_action)

        return self.get_action_sequences()
