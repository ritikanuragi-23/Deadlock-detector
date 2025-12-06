#!/usr/bin/env python3
"""
===============================================================================
                DEADLOCK DETECTION, PREVENTION & RECOVERY SIMULATOR
===============================================================================

This project simulates complete deadlock handling in an Operating System.
It performs:
    ✔ Banker's Algorithm (Safety Check)
    ✔ Wait-For Graph Construction
    ✔ Deadlock Detection (Cycle detection using DFS)
    ✔ Deadlock Recovery (Process Termination)
    ✔ Graph Visualization (Before & After)

-------------------------------------------------------------------------------
                 HOW TO RUN THIS PROJECT (VERY IMPORTANT)
-------------------------------------------------------------------------------

STEP 1: INSTALL PYTHON
    Download Python from: https://www.python.org/
    During installation, CHECK THE BOX: "Add Python to PATH"

STEP 2: INSTALL REQUIRED LIBRARIES
    Open CMD or PowerShell and run:
        pip install matplotlib networkx

STEP 3: GENERATE INPUT FILE
    Run:
        python Input_generator.py
    This creates a file named: deadlock_input.json

STEP 4: RUN MAIN SIMULATOR
        python Deadlock_detection_and_recovery.py

The program will:
    ✔ Read the JSON
    ✔ Display Max, Allocation, Need, Available
    ✔ Check safe/unsafe state
    ✔ Build wait-for graph
    ✔ Detect deadlock cycles
    ✔ Perform recovery steps
    ✔ Save two graph images:
         → wait_for_graph_before.png
         → wait_for_graph_after.png

-------------------------------------------------------------------------------
                         ABOUT THE INPUT FILE
-------------------------------------------------------------------------------
deadlock_input.json will look like:

{
  "experiment_name": "DeadlockExp1",
  "num_processes": 4,
  "num_resources": 1,
  "max_demand": [[7],[5],[6],[1]],
  "allocation": [[2],[5],[6],[1]],
  "available": [0]
}

Need is computed automatically:
Need = Max - Allocation

-------------------------------------------------------------------------------
                   IMPORTANT FIX FOR WINDOWS USERS
-------------------------------------------------------------------------------
Tkinter sometimes fails with error:
    _tkinter.TclError: not enough memory for image buffer

To fix this, we FORCE a non-GUI matplotlib backend:
    matplotlib.use("Agg")
-------------------------------------------------------------------------------
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict
import json
import os

# ---------------------------------------------------------------------------
# FIX: FORCE MATPLOTLIB TO USE NON-GUI BACKEND (REQUIRED ON WINDOWS)
# ---------------------------------------------------------------------------
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import networkx as nx


# =============================================================================
#                           DATA STRUCTURE
# =============================================================================
@dataclass
class SystemState:
    allocation: List[List[int]]
    max_demand: List[List[int]]
    available: List[int]

    @property
    def processes(self) -> int:
        return len(self.allocation)

    @property
    def resources(self) -> int:
        return len(self.available)

    @property
    def need(self) -> List[List[int]]:
        return [
            [self.max_demand[i][j] - self.allocation[i][j] for j in range(self.resources)]
            for i in range(self.processes)
        ]


# =============================================================================
#                       BANKER'S ALGORITHM (SAFETY CHECK)
# =============================================================================
def bankers_is_safe(state: SystemState) -> Tuple[bool, List[int]]:
    n = state.processes
    m = state.resources
    work = state.available.copy()
    finish = [False] * n
    sequence = []
    need = state.need
    alloc = state.allocation

    while len(sequence) < n:
        found = False
        for i in range(n):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(m)):
                for j in range(m):
                    work[j] += alloc[i][j]
                finish[i] = True
                sequence.append(i)
                found = True
        if not found:
            break

    return all(finish), sequence


# =============================================================================
#                       BUILD WAIT-FOR GRAPH
# =============================================================================
def build_wait_for_graph(state: SystemState) -> Dict[int, List[int]]:
    n = state.processes
    m = state.resources
    need = state.need
    alloc = state.allocation
    avail = state.available

    graph = {i: [] for i in range(n)}

    for i in range(n):
        for r in range(m):
            if need[i][r] > 0 and need[i][r] > avail[r]:
                for j in range(n):
                    if alloc[j][r] > 0 and j != i:
                        graph[i].append(j)

    return graph


# =============================================================================
#                       DFS CYCLE DETECTION
# =============================================================================
def find_deadlocked_processes(graph: Dict[int, List[int]]) -> List[List[int]]:
    color = {u: 0 for u in graph}
    parent = {u: None for u in graph}
    cycles = []

    def dfs(u):
        color[u] = 1
        for v in graph[u]:
            if color[v] == 0:
                parent[v] = u
                dfs(v)
            elif color[v] == 1:
                cycle = [v]
                x = u
                while x != v:
                    cycle.append(x)
                    x = parent[x]
                cycle.reverse()
                if cycle not in cycles:
                    cycles.append(cycle)
        color[u] = 2

    for u in graph:
        if color[u] == 0:
            dfs(u)

    return cycles


# =============================================================================
#                       DEADLOCK RECOVERY
# =============================================================================
def terminate_process(state: SystemState, pid: int) -> SystemState:
    new_alloc = [row.copy() for row in state.allocation]
    new_max = [row.copy() for row in state.max_demand]
    new_avail = state.available.copy()

    for r in range(state.resources):
        new_avail[r] += new_alloc[pid][r]
        new_alloc[pid][r] = 0

    return SystemState(new_alloc, new_max, new_avail)


# =============================================================================
#                       DRAW WAIT-FOR GRAPH
# =============================================================================
def draw_wait_for_graph(graph, cycles, filename, title="Wait-For Graph"):
    G = nx.DiGraph()

    for src in graph:
        for dst in graph[src]:
            G.add_edge(src, dst)

    pos = nx.circular_layout(G)

    plt.figure(figsize=(6, 6))
    plt.title(title)

    cycle_edges = set()
    for cyc in cycles:
        for i in range(len(cyc)):
            u = cyc[i]
            v = cyc[(i + 1) % len(cyc)]
            cycle_edges.add((u, v))

    normal_edges = [e for e in G.edges if e not in cycle_edges]

    nx.draw_networkx_nodes(G, pos, node_color="lightblue")
    nx.draw_networkx_edges(G, pos, edgelist=normal_edges, edge_color="gray")
    nx.draw_networkx_edges(G, pos, edgelist=list(cycle_edges), edge_color="red", width=2)

    nx.draw_networkx_labels(G, pos, labels={n: f"P{n}" for n in G.nodes})

    plt.axis("off")
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    print(f"Graph saved to: {filename}")


# =============================================================================
#                       PRINT HELPERS
# =============================================================================
def print_matrix(name: str, mat):
    print(f"{name}:")
    for i, row in enumerate(mat):
        print(f"P{i}: " + " ".join(f"{x:3d}" for x in row))
    print()

def print_vector(name: str, vec):
    print(f"{name}: " + " ".join(f"{x:3d}" for x in vec))
    print()


# =============================================================================
#                       LOAD INPUT STATE FROM JSON
# =============================================================================
def load_state_from_file(filename="deadlock_input.json"):
    if not os.path.exists(filename):
        raise FileNotFoundError("ERROR: deadlock_input.json not found! Run Input_generator.py first.")

    with open(filename, "r") as f:
        data = json.load(f)

    exp_name = data.get("experiment_name", "Experiment")
    max_demand = data["max_demand"]
    allocation = data["allocation"]
    available = data["available"]

    return exp_name, SystemState(
        allocation=allocation,
        max_demand=max_demand,
        available=available
    )


# =============================================================================
#                                   MAIN PROGRAM
# =============================================================================
def main():
    print("=== Deadlock Detection, Prevention & Recovery Simulator ===\n")

    exp_name, state = load_state_from_file()
    print(f"Experiment: {exp_name}\n")

    print("--- INITIAL STATE ---")
    print_matrix("Max", state.max_demand)
    print_matrix("Allocation", state.allocation)
    print_matrix("Need", state.need)
    print_vector("Available", state.available)

    print("\n>>> Checking SAFETY...")
    safe, seq = bankers_is_safe(state)
    if safe:
        print("SAFE state. Sequence:", " -> ".join(f"P{i}" for i in seq))
    else:
        print("UNSAFE state.")

    print("\n>>> Building Wait-For Graph...")
    graph = build_wait_for_graph(state)
    print(graph)

    cycles = find_deadlocked_processes(graph)

    draw_wait_for_graph(graph, cycles, "wait_for_graph_before.png",
                        f"Wait-For Graph (Before Recovery) - {exp_name}")

    if not cycles:
        print("\nNo deadlock detected.")
        draw_wait_for_graph(graph, [], "wait_for_graph_after.png",
                            f"Wait-For Graph (After Recovery) - {exp_name}")
        return

    print("\nDeadlock cycles found:", cycles)

    current_state = state
    while True:
        graph = build_wait_for_graph(current_state)
        cycles = find_deadlocked_processes(graph)
        if not cycles:
            break

        victim = cycles[0][0]
        print(f"Terminating P{victim} to break deadlock...")
        current_state = terminate_process(current_state, victim)

    print("\n--- AFTER FULL RECOVERY ---")
    print_matrix("Allocation", current_state.allocation)
    print_matrix("Need", current_state.need)
    print_vector("Available", current_state.available)

    draw_wait_for_graph(build_wait_for_graph(current_state), [],
                        "wait_for_graph_after.png",
                        f"Wait-For Graph (After Recovery) - {exp_name}")


if __name__ == "__main__":
    main()
