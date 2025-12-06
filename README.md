# Deadlock Detection, Prevention & Recovery Simulator  
---

## 📖 Project Overview
This project implements a complete **Deadlock Detection, Prevention, and Recovery** system in Python.  
It simulates how an Operating System manages resources, detects deadlocks using wait-for graphs, and recovers by terminating processes.

The simulator includes:
- ✔ Banker’s Algorithm (Safety Check)
- ✔ Wait-For Graph Construction
- ✔ Deadlock Detection using DFS Cycle Finding
- ✔ Deadlock Recovery by Process Termination
- ✔ Graph Visualization (Before & After Recovery)
- ✔ JSON-based Input Generator

---

## 🚀 How to Run This Project

### **STEP 1 — Install Python**
Download Python from: https://www.python.org  
Make sure to check: **“Add Python to PATH”**

---

### **STEP 2 — Install Required Libraries**

```bash
pip install matplotlib networkx
STEP 3 — Generate Input File
Run the input generator:

bash
Copy code
python Input_generator.py
This creates:

pgsql
Copy code
deadlock_input.json
Example JSON:

json
Copy code
{
  "experiment_name": "DeadlockExp1",
  "num_processes": 4,
  "num_resources": 1,
  "max_demand": [[7],[5],[6],[1]],
  "allocation": [[2],[5],[6],[1]],
  "available": [0]
}
STEP 4 — Run Main Deadlock Simulator
bash
Copy code
python Deadlock_detection_and_recovery.py
The program will:

Display Max, Allocation, Need, Available matrices

Run Banker’s Algorithm

Build Wait-For Graph

Detect deadlock via cycle detection

Recover by terminating processes

Save graph images:

wait_for_graph_before.png

wait_for_graph_after.png

🖼 Output Graphs
Before Recovery (Deadlock Detected)
<img width="600" height="600" alt="wait_for_graph_before" src="https://github.com/user-attachments/assets/868d3879-0840-40b7-b7cf-1190d6de2111" />

Shows several red-colored cycles indicating deadlock.

After Recovery (Deadlock Resolved)
Graph becomes acyclic; no cycles remain.
<img width="600" height="600" alt="wait_for_graph_after" src="https://github.com/user-attachments/assets/191d78a5-1930-43ad-a04a-fd43dddbfee5" />


Add these images in your PPT/report for perfect explanation.

🧠 Algorithms Used
1️⃣ Banker's Algorithm
Checks if the system is in a safe state.

Finds a valid safe sequence.

2️⃣ Wait-For Graph
Node = Process

Edge P → Q means P is waiting for Q

A cycle indicates deadlock.

3️⃣ DFS Cycle Detection
Detects cycles in the wait-for graph.

All processes in a cycle are considered deadlocked.

4️⃣ Deadlock Recovery
Terminates one or more victim processes.

Releases their resources.

Reconstructs the wait-for graph.

Repeats until no cycles remain.

📂 Project File Structure
File Name	Description
Input_generator.py	Generates random valid JSON input file
Deadlock_detection_and_recovery.py	Main deadlock simulator
deadlock_input.json	Input resource allocation state
wait_for_graph_before.png	Deadlock visualization before recovery
wait_for_graph_after.png	Graph after deadlock is removed
Deadlock_Project_PPT_Final.pptx	Project presentation
README.md	Documentation file
