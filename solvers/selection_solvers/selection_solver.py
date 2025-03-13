"""
Classes:
- SelectionSolver: Abstract base class for one step look-ahead selection-based solvers.
"""

from models import Action, Vehicle
from solvers.search_solvers import SearchSolver

class SelectionSolver(SearchSolver):
    """
    A family of solvers that differ only in how they choose vehicles and actions.

    TODO: Implement select_vehicle_action
    """

    def initialize_search_tree(self, vehicle : "Vehicle"):
        vehicle.expand(self.unanswered_calls)

    def expand_vehicle_search_tree(self, selected_vehicle : "Vehicle"):
        selected_vehicle.expand(self.unanswered_calls)

    def remove_answered_call(self, selected_vehicle : "Vehicle", selected_action : "Action"):
        for vehicle in self.vehicles:
            if vehicle == selected_vehicle:
                continue

            vehicle.remove(selected_action.call)
