"""Main Script"""
from solvers.selection_solvers import SearchSolver

solver = SearchSolver(
    "data/Call_80_Vehicle_20.txt"
)
action_sequences = solver.multi_solve(100)
