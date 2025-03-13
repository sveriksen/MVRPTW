"""""Greedy Solvers"""

from typing import List, Tuple

from models import Action, Vehicle
from solvers.selection_solvers.selection_solver import SelectionSolver

class CostGreedySolver(SelectionSolver):
    """
    GreedySolver selects actions based on a heuristic:
    - Selects the vehicle with the lowest mean cost per action.
    - Selects the action that results in the smallest immediate cost increase.
    """

    def select_vehicle_action(self, active_vehicles: List[Vehicle]) -> Tuple[Vehicle, Action]:
        """
        Selects the vehicle with the lowest mean cost per action.
        Then selects the action that results in the smallest immediate cost increase.
        """

        min_cost_per_action = float("inf")
        selected_vehicle = None
        selected_action = None
        for vehicle in active_vehicles:
            for action in vehicle.current_state.next_states:
                cost_per_action = vehicle.get_action_cost(action)
                if cost_per_action < min_cost_per_action:
                    min_cost_per_action = cost_per_action
                    selected_vehicle = vehicle
                    selected_action = action

        return selected_vehicle, selected_action


class TimeGreedySolver(SelectionSolver):
    """
    Greedy solver with respect to time. Looks one step ahead for all vehicles.
    """

    def select_vehicle_action(self, active_vehicles : List[Vehicle]) -> Tuple[Vehicle, Action]:
        """
        Selects vehicle and action with lowest time spent per action. Looks one step ahead.\n
        Always selects the vehicle action pair with the lowest time spent on the action.
        """

        lowest_action_rate = float("inf")
        selected_vehicle = None
        selected_action = None

        for vehicle in active_vehicles:
            current_time = vehicle.current_state.time
            for action, next_state in vehicle.current_state.next_states.items():
                action_rate = next_state.time - current_time

                if action_rate < lowest_action_rate:
                    lowest_action_rate = action_rate
                    selected_vehicle = vehicle
                    selected_action = action

        return selected_vehicle, selected_action
