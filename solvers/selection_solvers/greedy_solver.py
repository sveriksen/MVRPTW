"""""Greedy Solver"""

from typing import List, Tuple
from solvers.selection_solvers.selection_solver import SelectionSolver
from models import Action, Vehicle

class GreedySolver(SelectionSolver):
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
        vehicle = min(active_vehicles, key=lambda v: (v.cost / max(1, v.route_length)))
        action = min(vehicle.current_state.next_states.keys(),
                     key=lambda a: vehicle.costs.travel_costs[vehicle.current_state.node, a.node] +
                                   vehicle.costs.service_costs[a.call_idx, a.action_idx] -
                                   a.call.void_cost / 2)

        return vehicle, action
