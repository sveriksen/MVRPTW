"""Naive Solver"""

from typing import List
from random import choice

from models import Action, Vehicle
from solvers.selection_solvers.selection_solver import SelectionSolver

class RandomSolver(SelectionSolver):
    """
    Works by repeatedly selecting a random vehicle, alongside a random feasible action \\
    until no further actions are possible. Then it returns the associated vehicle action sequences.
    """

    def select_vehicle(self, active_vehicles : List[Vehicle]) -> Vehicle:
        """Selects a vehicle from the set of active vehicles."""
        return choice(active_vehicles)

    def select_action(self, vehicle : Vehicle) -> Action:
        """Selects an action for the selected vehicle."""
        return choice(list(vehicle.current_state.next_states.keys()))
