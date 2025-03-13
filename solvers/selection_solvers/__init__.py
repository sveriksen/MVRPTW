"""
Selection Solver Package.

This module provides different solver implementations for vehicle routing problems.

Exposes:
- RandomSolver: A naive solver that selects vehicles and actions randomly.
- CostGreedySolver: A deterministic solver that chooses vehicles and actions greedily based on cost.
- TimeGreedySolver: A deterministic solver that chooses vehicles and actions greedily based on time.
"""

from solvers.selection_solvers.random_solver import RandomSolver
from solvers.selection_solvers.greedy_solvers import CostGreedySolver, TimeGreedySolver

__all__ = ["RandomSolver", "CostGreedySolver", "TimeGreedySolver"]
