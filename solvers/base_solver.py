"""Base Class for all solver classes"""

from typing import List
from pathlib import Path
from abc import ABC, abstractmethod

from tqdm import tqdm

from models import Action, Vehicle
from utils.cost import get_cost
from utils.problem import load_problem
from utils.formatting import format_number

class Solver(ABC):
    """
    Solver Base Class
    Attributes:
        data_path (str): Path to the data of the problem
        instance_name (str): Name of the problem instance
        vehicles (Set[Vehicle]): Vehicles from problem
        calls (Set[Call]): Calls from problem
    """
    def __init__(self, data_path : str):
        self.data_path = data_path
        self.instance_name = Path(data_path).stem
        self.vehicles, self.calls = load_problem(data_path)
        self.unanswered_calls = self.calls.copy()

    def reset(self):
        """Calls vehicle.reset() for all vehicles."""
        for vehicle in self.vehicles:
            vehicle.reset()

        self.unanswered_calls = self.calls.copy()

    def get_active_vehicles(self) -> List[Vehicle]:
        """Returns set of vehicles which can perform any actions"""
        return [v for v in self.vehicles if v.current_state.next_states]

    def get_action_sequences(self) -> List[List[Action]]:
        """
        Returns a list of the action sequences of each vehicle \\
        in ascending order by vehicle index
        """
        action_sequences = {}

        for vehicle in self.vehicles:
            action_sequences[vehicle.specs.idx] = vehicle.action_sequence

        return [e[1] for e in sorted(action_sequences.items(), key=lambda x : x[0])]

    @abstractmethod
    def solve(self):
        """Required method for all Solver instances. Solves the problem at data_path."""

    def multi_solve(self, n : int) -> List[List[Action]]:
        """Calls .solve() n times, and returns the best found solution."""
        best_cost = float("inf")
        best_action_sequence = None

        progressbar = tqdm(
            total=n,
            desc=f"Instance: '{self.instance_name}', "
            f"Solver: {self.__class__.__name__}, "
            f"Cost: {best_cost}, "
            f"Unanswered Calls: {len(self.unanswered_calls)}"
        )

        for _ in range(n):
            action_sequence = self.solve()

            cost = get_cost(self.vehicles, self.calls)
            if cost < best_cost:
                best_cost = cost
                best_action_sequence = action_sequence
                progressbar.set_description(
                    desc=f"Instance: '{self.instance_name}', "
                    f"Solver: {self.__class__.__name__}, "
                    f"Cost: {format_number(int(best_cost))}, "
                    f"Unanswered Calls: {len(self.unanswered_calls)}"
                )

            self.reset()

            progressbar.update()
        progressbar.close()

        return best_action_sequence
