"""
This module implements a standard beam search algorithm utilizing a priority queue.
"""

import heapq

def is_terminal(state):
    """ 
    Defines when a state is considered terminal.
    Modify this based on your specific problem. 
    """
    return state >= 3


def beam_search(initial_state, expand_fn, beam_width, max_depth):
    """
    Performs beam search to find the best sequence.

    :param initial_state: The starting state.
    :param expand_fn: Function(state) -> List[(next_state, token, score)]
    :param beam_width: The number of top candidates to keep.
    :param max_depth: Maximum search depth before stopping.
    :return: The best sequence found.
    """
    # Priority queue (max-heap using negative cost for sorting)
    beam = [(0, initial_state, [])]  # (cost, state, sequence)

    for _ in range(max_depth):
        new_beam = []

        for cost, state, sequence in beam:
            new_states = expand_fn(state)

            for next_state, action, action_cost in new_states:
                new_sequence = sequence + [action]
                new_cost = cost + action_cost

                new_beam.append((new_cost, next_state, new_sequence))

        # Keep only the top-k sequences (lower cost is better)
        beam = heapq.nsmallest(beam_width, new_beam, key=lambda x: x[0])

        # Stop early if all states in the beam are terminal
        if all(is_terminal(state) for _, state, _ in beam):
            break

    # Return best sequence
    _, _, best_sequence = max(beam, key=lambda x: x[0])
    return best_sequence  # Only return the best sequence


def expand_state(state):
    """ 
    Example successor function.
    Replace with your own function for different problems.
    """
    if state >= 3:  # Terminal condition
        return []
    return [(state + 1, f"action_{state + 1}", state + 1)]  # (next_state, token, score)


# Parameters
INITIAL_STATE = 0
BEAM_WIDTH = 2
MAX_DEPTH = 5  # Max depth is effectively the max search steps

# Run beam search
result = beam_search(INITIAL_STATE, expand_state, BEAM_WIDTH, MAX_DEPTH)

# Print results
print("Best Sequence:", result)
