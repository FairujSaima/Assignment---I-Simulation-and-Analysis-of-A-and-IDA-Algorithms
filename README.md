# Assignment---I-Simulation-and-Analysis-of-A-and-IDA-Algorithms
Assignment - I: Simulation and Analysis of A* and IDA*  Algorithms

Introduction:

The assignment explores basic principles of autonomous navigation using an agent-based model. The robot (agent) navigates tasks while avoiding obstacles. It uses A* search and IDA* (iterative Deepening A*) to find the best routes. It chooses the nearest task to complete first rather than the 1st task. 

Running the simulation:

Each folder (A star simulator and IDA star simulator) contains a run.py file. Open the desired folder and execute run.py to run the desired algorithm. 
A pygame window will open which will display the grid, tasks, robot and obstacles. 

Observations:

The agent utilizes a pathfinding algorithm (either A* or IDA* depending on the implementation) to determine the shortest path to various tasks. It moves along the designated path by updating its position based on the move() method.

The environment is generated with random barriers and tasks. The Environment class manages the grid's dimensions and the placement of these elements, ensuring that the agent has to navigate around the barriers to complete its tasks.

The agent keeps track of completed tasks, and the system is designed to update the task locations dynamically. When a task is completed, it's removed from the list of active tasks, and the agent automatically seeks the nearest remaining task.

The simulation includes a graphical user interface (GUI) built with Pygame. It displays the grid, barriers, tasks, and a status section showing completed tasks, the agent's position, and the total path cost.

The approach utilizes a heuristic (Manhattan distance) to guide the pathfinding algorithms, which helps in efficiently determining the agent's routes across the grid.

Challenges and solution:

Randomly placing barriers and tasks can result in scenarios where tasks are completely unreachable due to walls blocking access. To address this, checks can be implemented to ensure at least one accessible path exists to each task before finalizing barrier placements.

Performance and efficiency issues arise with the IDA* algorithm in larger grids, which can be mitigated by optimizing the heuristic function and introducing memoization to store computed paths.

Tracking the agent's state accurately can lead to inconsistencies, such as attempting to move when no tasks are left.

