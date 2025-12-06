#!/usr/bin/env python3
"""
generate_deadlock_input.py

Generates a random system state for deadlock simulation and saves it
to a JSON file: deadlock_input.json

Structure of deadlock_input.json:

{
  "experiment_name": "DeadlockExp1",
  "num_processes": 5,
  "num_resources": 3,
  "max_demand": [[...], ...],
  "allocation": [[...], ...],
  "available": [...]
}
"""

import json
import random


def read_int(prompt: str, default: int) -> int:
    """Read an integer from user, allow empty for default."""
    while True:
        s = input(f"{prompt} [{default}]: ").strip()
        if not s:
            return default
        try:
            val = int(s)
            if val <= 0:
                print("Please enter a positive integer.")
                continue
            return val
        except ValueError:
            print("Please enter a valid integer.")


def generate_state(num_processes: int, num_resources: int):
    """
    Generate a random, consistent state:

    - max_demand[i][j] in [0, 9]
    - allocation[i][j] in [0, max_demand[i][j]]
    - available is derived as:
        total_instances[j] = sum(allocation[*][j]) + extra[j]
        extra[j] in [0, 3]
        available[j] = total_instances[j] - sum(allocation[*][j]) = extra[j]
    """
    max_demand = []
    allocation = []

    # Generate max_demand
    for _ in range(num_processes):
        row = [random.randint(0, 9) for _ in range(num_resources)]
        max_demand.append(row)

    # Generate allocation (respecting max_demand)
    for i in range(num_processes):
        row_alloc = []
        for j in range(num_resources):
            if max_demand[i][j] == 0:
                row_alloc.append(0)
            else:
                row_alloc.append(random.randint(0, max_demand[i][j]))
        allocation.append(row_alloc)

    # Compute available as extra capacity above total allocated
    allocated_sum = [0] * num_resources
    for j in range(num_resources):
        for i in range(num_processes):
            allocated_sum[j] += allocation[i][j]

    available = []
    for j in range(num_resources):
        extra = random.randint(0, 3)  # some extra free instances
        available.append(extra)

    return max_demand, allocation, available


def main():
    print("=== Deadlock Input Generator ===")
    n = read_int("Number of processes", default=5)
    m = read_int("Number of resource types", default=3)

    max_demand, allocation, available = generate_state(n, m)

    experiment_name = "DeadlockExp1"

    data = {
        "experiment_name": experiment_name,
        "num_processes": n,
        "num_resources": m,
        "max_demand": max_demand,
        "allocation": allocation,
        "available": available,
    }

    filename = "deadlock_input.json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    print(f"\nGenerated state saved to {filename}")
    print("You can now run: python deadlock_simulator_from_file.py")


if __name__ == "__main__":
    main()
