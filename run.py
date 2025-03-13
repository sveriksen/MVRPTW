"""Main Script"""

from solvers.selection_solvers import TimeGreedySolver

MAX_DEPTH = 2
BEAM_SIZE = 2
DATA_PATH = "data/Call_130_Vehicle_40.txt"
solver = TimeGreedySolver(DATA_PATH)
action_sequences = solver.multi_solve(1)
