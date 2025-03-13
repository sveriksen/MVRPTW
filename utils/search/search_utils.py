"""DOCSTRING HERE"""

from typing import Set, List, TYPE_CHECKING

if TYPE_CHECKING:
    from models.state import State
    from models.vehicle import Vehicle
    from models.actions import Action, Call

def expand_state(state: "State", vehicle: "Vehicle", unanswered_calls: Set["Call"], depth: int = 1):
    """Expands the state by computing feasible actions by vehicle"""
    if depth <= 0:
        return

    potential_actions : List["Action"] = []

    for delivery in state.commitments:
        if delivery in state.next_states:
            continue
        potential_actions.append(delivery)

    for pickup in {c.pickup for c in vehicle.specs.compatible_calls & unanswered_calls}:
        if pickup in state.next_states:
            continue
        potential_actions.append(pickup)

    for action in potential_actions:
        resulting_state = vehicle.perform(action)
        if resulting_state is None:
            continue

        state.add_transition(action, resulting_state)
        expand_state(resulting_state, vehicle, unanswered_calls - {action.call}, depth=depth-1)

def delete_children(state : "State"):
    """Deletes all children recursively. Resets selected_action and next_state."""
    for next_state in state.next_states.values():
        delete_children(next_state)

    state.next_states.clear()
    state.selected_action = None
    state.next_state = None
