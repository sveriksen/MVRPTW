"""Module for loading problem instances from a file."""

from pathlib import Path
from typing import Tuple, Set, List

import numpy as np

from models.state import State
from models.vehicle import Vehicle, VehicleSpecs, VehicleCosts, VehicleTimes
from models.actions import Call, Pickup, Delivery


def parse_header_info(lines : List[str]) -> Tuple[int, int, int]:
    """
    Reads lines 0, 1, and 3 to parse:
    - NUM_NODES  (line 0)
    - NUM_VEHICLES (line 1)
    - NUM_CALLS (line 3)
    """
    num_nodes = None
    num_vehicles = None
    num_calls = None

    data_line_idx = -1
    for raw_line in lines:
        line = raw_line.strip()
        if not line or line.startswith("%"):
            data_line_idx += 1
            continue

        data = [int(e) for e in line.split(",")]

        if data_line_idx == 0:
            num_nodes = data[0]

        elif data_line_idx == 1:
            num_vehicles = data[0]

        elif data_line_idx == 3:
            num_calls = data[0]
            break


    if num_nodes is None or num_vehicles is None or num_calls is None:
        raise ValueError("Missing header info (NUM_NODES, NUM_VEHICLES, NUM_CALLS).")

    return num_nodes, num_vehicles, num_calls


def load_problem(path: str) -> Tuple[Set[Vehicle], Set[Call]]:
    """
    Loads the problem instance from a file, returning sets of Vehicles and Calls.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Problem file {path} not found!")

    with open(path, "r", encoding="utf-8") as f:
        raw_lines = f.readlines()

    num_nodes, _, num_calls = parse_header_info(raw_lines)

    vehicle_data = {}
    call_data = {}

    data_line_idx = -1
    for raw_line in raw_lines:
        line = raw_line.strip()
        if not line or line.startswith("%"):
            data_line_idx += 1
            continue

        data = [int(e) for e in line.split(",")]

        if data_line_idx == 2:
            vehicle_idx, start_node, start_time, capacity = data
            vehicle_idx -= 1
            start_node -= 1

            travel_times = np.zeros((num_nodes, num_nodes), dtype=float)
            travel_costs = np.zeros((num_nodes, num_nodes), dtype=float)

            service_times = np.zeros((num_calls, 2), dtype=float)
            service_costs = np.zeros((num_calls, 2), dtype=float)

            vehicle_data.setdefault(vehicle_idx, {
                "state": State(start_node, float(start_time), frozenset()),
                "specs": {
                    "idx": vehicle_idx,
                    "capacity": float(capacity),
                    "compatible_calls": set()
                },
                "times": {
                    "travel_times": travel_times,
                    "service_times": service_times
                },
                "costs": {
                    "travel_costs": travel_costs,
                    "service_costs": service_costs
                }
            })

        elif data_line_idx == 4:
            vehicle_idx = data[0] - 1
            compatible_calls = {c - 1 for c in data[1:]}
            vehicle_data[vehicle_idx]["specs"]["compatible_calls"].update(compatible_calls)

        elif data_line_idx == 5:
            c_idx, p_node, d_node, size, void_cost, p_low, p_high, d_low, d_high = data
            c_idx -= 1
            p_node -= 1
            d_node -= 1

            call_data[c_idx] = {
                "size": float(size),
                "void_cost": float(void_cost),
                "pickup":  {"node": p_node, "window": (float(p_low), float(p_high))},
                "delivery":{"node": d_node, "window": (float(d_low), float(d_high))}
            }

        elif data_line_idx == 6:
            vehicle_idx, from_node, to_node, t_time, t_cost = data
            vehicle_idx -= 1
            from_node -= 1
            to_node -= 1

            vinfo = vehicle_data[vehicle_idx]
            vinfo["times"]["travel_times"][from_node, to_node] = float(t_time)
            vinfo["costs"]["travel_costs"][from_node, to_node] = float(t_cost)

        elif data_line_idx == 7:
            vehicle_idx, c_idx, pickup_time, pickup_cost, delivery_time, delivery_cost = data
            vehicle_idx -= 1
            c_idx -= 1

            vinfo = vehicle_data[vehicle_idx]
            vinfo["times"]["service_times"][c_idx, 0] = float(pickup_time)
            vinfo["times"]["service_times"][c_idx, 1] = float(delivery_time)

            vinfo["costs"]["service_costs"][c_idx, 0] = float(pickup_cost)
            vinfo["costs"]["service_costs"][c_idx, 1] = float(delivery_cost)

    call_instances = {}
    calls = set()
    for c_idx, c_info in sorted(call_data.items()):
        pickup = Pickup(c_info["pickup"]["node"], *c_info["pickup"]["window"])
        delivery = Delivery(c_info["delivery"]["node"], *c_info["delivery"]["window"])
        call_obj = Call(c_idx, c_info["size"], c_info["void_cost"], pickup, delivery)

        call_instances[c_idx] = call_obj
        calls.add(call_obj)

    vehicles = set()
    for v_idx, vdict in sorted(vehicle_data.items()):
        specs = VehicleSpecs(
            idx=v_idx,
            capacity=vdict["specs"]["capacity"],
            compatible_calls=frozenset(
                call_instances[cidx] for cidx in vdict["specs"]["compatible_calls"]
            )
        )
        costs = VehicleCosts(
            travel_costs=vdict["costs"]["travel_costs"],
            service_costs=vdict["costs"]["service_costs"]
        )
        times = VehicleTimes(
            travel_times=vdict["times"]["travel_times"],
            service_times=vdict["times"]["service_times"]
        )

        vehicle_obj = Vehicle(
            state=vdict["state"],
            specs=specs,
            costs=costs,
            times=times
        )
        vehicles.add(vehicle_obj)

    return vehicles, calls
