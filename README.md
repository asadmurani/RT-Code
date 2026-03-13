Comparative Analysis of Real-Time Scheduling Algorithms on a Multicore Processor via Event Simulator in Python
==============================================================================================================

This repository contains a Python-based discrete-event simulation framework designed to evaluate and compare real-time scheduling algorithms on multi-core systems. The project specifically analyzes the trade-offs between **Partitioned**, **Global**, and **Hybrid (Clustered)** Earliest Deadline First (EDF) scheduling strategies.

📖 Project Overview
-------------------

In real-time systems, the challenge of multi-core scheduling involves balancing processor utilization against system overheads. This simulator models a hardware environment where periodic tasks are released as jobs, each with specific execution times and deadlines.

The simulation focuses on three critical performance metrics:

*   **Offline Fragmentation:** Tasks rejected because they cannot "fit" into a core or cluster during the initial assignment phase.
    
*   **Runtime Migrations:** The overhead caused when a job moves from one core to another, potentially invalidating caches and increasing execution time.
    
*   **Deadline Performance:** The count of jobs that fail to complete their work before their absolute deadline.
    

🛠 Scheduling Strategies
------------------------

### 1\. Partitioned EDF

*   **Logic:** Uses a "First-Fit Decreasing" bin-packing heuristic to assign tasks to specific cores permanently.
    
*   **Advantages:** Zero migration overhead since jobs never leave their assigned core.
    
*   **Disadvantages:** Subject to heavy fragmentation; a core may be idle while another is overloaded simply because a task was not assigned to it.
    

### 2\. Global EDF

*   **Logic:** All ready jobs are placed in a single global priority queue. At every tick, the $m$ highest-priority jobs (those with the earliest deadlines) are assigned to the $m$ available cores.
    
*   **Advantages:** Theoretically optimal for utilization as it prevents cores from being idle while work is available.
    
*   **Disadvantages:** High migration frequency as jobs are frequently moved between cores to maintain priority, leading to significant performance penalties.
    

### 3\. Hybrid (Clustered) EDF

*   **Logic:** Cores are grouped into clusters (e.g., a 4-core system split into two 2-core clusters). Tasks are partitioned into these clusters, but once inside, they are scheduled globally across all cores within that cluster.
    
*   **Advantages:** A middle-ground approach that reduces global migration while providing better flexibility than strict partitioning.
    

📂 File Structure
-----------------

*   Core.py: Models the hardware CPU, tracking active time, idle time, and execution history.
    
*   Task.py & Job.py: Define the parameters of periodic real-time tasks (Period, WCET, Deadline) and their runtime instances.
    
*   PartitionedScheduler.py: Implements the offline bin-packing and partitioned runtime logic.
    
*   GlobalScheduler.py: Implements the single-queue global scheduling architecture.
    
*   HybridScheduler.py: Implements cluster-level partitioning and intra-cluster global scheduling.
    
*   TaskGenerator.py: Generates synthetic task sets using a UUniFast-style distribution to reach target system utilizations.
    
*   Visualizer.py: Contains the logic for generating performance charts using Matplotlib.
    
*   main.py: The central execution script to run simulations and output results.
    

📊 Visualization and Analysis
-----------------------------

The simulator produces three primary visual outputs to aid in performance analysis:

1.  **Comparative Bar Chart:** A high-level view of failed assignments, migrations, and missed deadlines across the three strategies.
    
2.  **Migration Timeline:** A line graph tracking how cumulative migration overhead grows over the simulation duration, illustrating system stability.
    
3.  **Utilization Heatmap:** A grid showing the load distribution (active vs. idle time) for every core in every strategy, highlighting load balancing efficiency.
    

🚀 Getting Started
------------------

### Prerequisites

*   Python 3.x
    
*   Matplotlib
    
*   NumPy
    

### Running the Simulation

Execute the main script to run a pre-configured experiment involving a 4-core system and a 1000-tick duration:

### Prerequisites

The project requires Python 3.x and a few standard data science libraries:

```bash
pip install matplotlib numpy heapq
```
Running the Simulation

To execute the default experiment, simply run main.py:

```Bash
python main.py   `
```

The console will output the configuration, the generated tasks, and the simulation results (Failed Assignments, Migrations, and Missed Deadlines) for each strategy.

📊 Outputs & Visualizations
---------------------------

Upon running main.py, the simulator will automatically generate and save three visualization files to the root directory:

1.  **comparative\_analysis.png**: A log-scale bar chart comparing the three strategies based on Failed Assignments (Fragmentation), Total Migrations (Jitter), and Missed Deadlines (Performance).
    
2.  **migration\_timeline.png**: A line graph plotting the cumulative migrations over time. This clearly illustrates the constant overhead of Global EDF compared to the stabilized bounds of Hybrid EDF and the zero-migration characteristic of Partitioned EDF.
    
3.  **utilization\_heatmap.png**: A heatmap displaying the percentage of time each core spent actively executing jobs, providing visual insight into how well each strategy balances the load across the hardware.
    

⚙️ Configuration
----------------

You can easily adjust the simulation parameters at the top of main.py:

```python
NUM_CORES = 4
SIMULATION_DURATION = 1000
MIGRATION_PENALTY = 1      # Ticks added to a job's remaining time upon migration
NUM_CLUSTERS = 2           # For Hybrid Scheduling   `
```

📊 Results & Analysis
---------------------

The simulator outputs high-resolution PNG files for reporting:

*   **comparative\_analysis.png**: Provides a log-scale comparison of strategy failures.
    
*   **migration\_timeline.png**: Shows how the Global strategy often results in a steep linear increase in migrations compared to the more stable Hybrid approach.
    
*   **utilization\_heatmap.png**: Visualizes how Partitioned scheduling can lead to "hot" and "cold" cores due to fragmentation, while Global/Hybrid strategies spread load more evenly.




🤝 Contributing
---------------

This project was developed as an academic exercise by students from the **Frankfurt University of Applied Sciences, Department of Engineering** 🏛️.

### 👨‍💻 Contributors

*   🎓 **Asad Ismail** (Matriculation No: 1542529)
    
*   🎓 **Akbar Khan** (Matriculation No: 1612839)
    
*   🎓 **Muhammad Suhaib Khalid** (Matriculation No: 1542491)
    

We welcome contributions to improve the simulator! 🚀

If you would like to contribute, please feel free to fork the repository, experiment with new scheduling heuristics (such as Least Laxity First), and submit a pull request. For major changes, please open an issue first to discuss what you would like to change. All feedback and improvements are highly appreciated! 💡
