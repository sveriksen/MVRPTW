"""Module for loading problem instances from a file.

This module reads problem instance files and parses the data to create sets of 
"Vehicle" and "Call" objects. It structures vehicle information into separate 
dataclasses ("VehicleSpecs", "VehicleCosts", "VehicleTimes") for better modularity.

Functions:
    load_problem(path: str) -> Tuple[Set[Vehicle], Set[Call]]
"""

from pathlib import Path
from typing import Tuple, Dict, Set
from collections import defaultdict

from models.state import State
from models.vehicle import Vehicle, VehicleSpecs, VehicleCosts, VehicleTimes
from models.actions import Call, Pickup, Delivery


def load_problem(path: str) -> Tuple[Set[Vehicle], Set[Call]]:
    """Loads the problem instance from a file and returns sets of Vehicles and Calls."""

    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Problem file {path} not found!")

    vehicle_data: Dict[int, Dict] = {}
    call_data: Dict[int, Dict] = {}

    with open(path, mode="r", encoding="utf-8") as f:
        lines = f.readlines()

    index = -1
    for line in lines:
        line = line.strip()
        if not line or line.startswith("%"):
            index += 1
            continue

        data = [int(e) for e in line.split(",")]

        if index == 2:  # Vehicle specifications
            vehicle_idx, start_node, start_time, capacity = data
            vehicle_idx -= 1
            start_node -= 1

            vehicle_data.setdefault(vehicle_idx, {
                "state": State(start_node, float(start_time), frozenset()),
                "specs": {"idx": vehicle_idx, "capacity": float(capacity), "compatible_calls": set()},
                "times": {"travel_times": defaultdict(lambda: defaultdict(float)), "service_times": {}},
                "costs": {"travel_costs": defaultdict(lambda: defaultdict(float)), "service_costs": {}}
            })

        elif index == 4:  # Vehicle-call compatibility
            vehicle_idx = data[0] - 1
            compatible_calls = {call_idx - 1 for call_idx in data[1:]}
            vehicle_data[vehicle_idx]["specs"]["compatible_calls"].update(compatible_calls)

        elif index == 5:  # Call information
            c_idx, p_node, d_node, size, void_cost, p_low, p_high, d_low, d_high = data
            c_idx -= 1
            p_node -= 1
            d_node -= 1

            call_data[c_idx] = {
                "size": float(size),
                "void_cost": float(void_cost),
                "pickup": {"node": p_node, "window": (float(p_low), float(p_high))},
                "delivery": {"node": d_node, "window": (float(d_low), float(d_high))}
            }

        elif index == 6:  # Vehicle travel times and costs
            vehicle_idx, from_node, to_node, t_time, t_cost = data
            vehicle_idx -= 1
            from_node -= 1
            to_node -= 1

            vehicle_data[vehicle_idx]["times"]["travel_times"][from_node][to_node] = float(t_time)
            vehicle_data[vehicle_idx]["costs"]["travel_costs"][from_node][to_node] = float(t_cost)

        elif index == 7:  # Vehicle service times and costs
            vehicle_idx, c_idx, pickup_time, pickup_cost, delivery_time, delivery_cost = data
            vehicle_idx -= 1
            c_idx -= 1

            vehicle_data[vehicle_idx]["times"]["service_times"][c_idx] = (float(pickup_time), float(delivery_time))
            vehicle_data[vehicle_idx]["costs"]["service_costs"][c_idx] = (float(pickup_cost), float(delivery_cost))

    # Create Call objects
    call_instances: Dict[int, Call] = {}
    calls: Set[Call] = set()
    for c_idx, c_info in sorted(call_data.items()):
        pickup = Pickup(c_info["pickup"]["node"], *c_info["pickup"]["window"])
        delivery = Delivery(c_info["delivery"]["node"], *c_info["delivery"]["window"])
        call = Call(c_idx, pickup, delivery, c_info["size"], c_info["void_cost"])

        call_instances[c_idx] = call
        calls.add(call)

    # Create Vehicle objects
    vehicles: Set[Vehicle] = set()
    for v_idx, v_info in sorted(vehicle_data.items()):
        specs = VehicleSpecs(
            idx=v_idx,
            capacity=v_info["specs"]["capacity"],
            compatible_calls=frozenset(call_instances[c_idx] for c_idx in v_info["specs"]["compatible_calls"])
        )

        costs = VehicleCosts(
            travel_costs=v_info["costs"]["travel_costs"],
            service_costs=v_info["costs"]["service_costs"]
        )

        times = VehicleTimes(
            travel_times=v_info["times"]["travel_times"],
            service_times=v_info["times"]["service_times"]
        )

        vehicles.add(Vehicle(state=v_info["state"], specs=specs, costs=costs, times=times))

    return vehicles, calls
