Real-Time Multi-Core Scheduling Simulator
This project is a discrete-event simulation framework designed to analyze and compare the performance of various real-time scheduling algorithms on multi-core systems. It specifically evaluates the trade-offs between Partitioned, Global, and Hybrid (Clustered) Earliest Deadline First (EDF) scheduling strategies.

Table of Contents
Overview

Core Metrics

Scheduling Strategies

Key Components

Simulation & Visualization

Getting Started

Overview
In real-time multi-core systems, scheduling involves assigning periodic tasks to multiple processors while ensuring all deadlines are met. This simulator provides a controlled environment to observe how different architectural approaches handle task distribution, preemption, and core migration overhead.

Core Metrics
The simulator evaluates performance based on three critical real-time systems metrics:

Failed Assignments (Fragmentation): Tasks that cannot be scheduled during the offline phase due to capacity constraints or core fragmentation.

Migrations (Jitter): The number of times a job moves from one core to another during execution. Migrations typically incur a performance penalty to account for cache invalidation and context switching.

Missed Deadlines (Performance): The count of job instances that fail to complete their worst-case execution time (WCET) before their absolute deadline.

Scheduling Strategies
1. Partitioned EDF
Tasks are permanently assigned to a specific core using a First-Fit Decreasing bin-packing heuristic.

Pros: Zero migration overhead; easy to implement using standard single-core scheduling theory.

Cons: Susceptible to core fragmentation; cannot utilize idle time on other cores if the assigned core is overloaded.

2. Global EDF
All ready jobs are placed into a single global priority queue. The top m jobs (where m is the number of cores) are dispatched to any available core every clock tick.

Pros: Highly flexible; minimizes idle cores; theoretically higher system utilization.

Cons: High migration overhead; significant contention for the global queue lock in real hardware.

3. Hybrid (Clustered) EDF
Cores are grouped into clusters (e.g., two clusters of two cores each). Tasks are partitioned into specific clusters, but within each cluster, they are scheduled globally.

Pros: Balances the utilization benefits of global scheduling with the reduced migration scope of partitioning.

Cons: Requires a more complex offline partitioning phase than standard Global EDF.

Key Components
Core.py: Simulates the physical hardware, tracking active and idle time while maintaining a history of executed job IDs.

Task.py & Job.py: Define the periodic task parameters (Execution Time, Period, Utilization) and the individual job instances released during simulation.

TaskGenerator.py: Generates synthetic workloads using a simplified UUniFast-like approach to randomly distribute system utilization across tasks.

Visualizer.py: Utilizes Matplotlib to generate comparative bar charts, migration timelines, and core utilization heatmaps.

Simulation & Visualization
The simulator produces three primary visual outputs to aid in performance analysis:

Comparative Analysis: A log-scale bar chart showing totals for failed assignments, migrations, and missed deadlines.

Migration Timeline: A line graph tracking the cumulative accumulation of migration overhead throughout the simulation duration.

Utilization Heatmap: A grid showing the percentage load for every core under each strategy, highlighting how well-balanced the system is.

Getting Started
Prerequisites
Python 3.x

Matplotlib

NumPy

Running the Experiment
To execute the default simulation (4 cores, 1000 ticks, with a 1-tick migration penalty):

Bash
python main.py
The script will output the simulation results to the console and save the generated charts as PNG files in the project directory.
