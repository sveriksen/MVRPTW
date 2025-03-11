"""
Cost calculation utilities.

Functions:
- get_cost(vehicles, calls): Computes the total cost, considering vehicle movements and void costs.
"""

from typing import List, Set

from models import Vehicle, Call

def get_cost(vehicles : List[Vehicle], calls : Set[Call]) -> float:
    """Calculates the cost of the current solution."""
    cost = sum(call.void_cost for call in calls)

    for vehicle in vehicles:
        cost += vehicle.cost

    return cost
