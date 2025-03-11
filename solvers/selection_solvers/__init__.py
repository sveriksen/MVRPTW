"""
Selection Solver Package.

This module provides different solver implementations for vehicle routing problems.

Exposes:
- RandomSolver: A naive solver that selects vehicles and actions randomly.
- GreedySolver: A deterministic solver that chooses vehicles and actions greedily based on cost.
"""

from solvers.selection_solvers.random_solver import RandomSolver
from solvers.selection_solvers.greedy_solver import GreedySolver

__all__ = ["RandomSolver", "GreedySolver"]
