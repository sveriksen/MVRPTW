"""Naive Solver"""

from typing import List, Tuple
from random import choice

from models import Action, Vehicle
from solvers.selection_solvers.selection_solver import SelectionSolver

class RandomSolver(SelectionSolver):
    """
    Works by repeatedly selecting a random vehicle, alongside a random feasible action \\
    until no further actions are possible. Then it returns the associated vehicle action sequences.
    """

    def select_vehicle_action(self, active_vehicles : List[Vehicle]) -> Tuple[Vehicle, Action]:
        """
        Selects a vehicle from the set of active vehicles, and an action for the selected vehicle.
        """
        vehicle = choice(active_vehicles)
        action = choice(list(vehicle.current_state.next_states.keys()))
        return choice(active_vehicles), action
