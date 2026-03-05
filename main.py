from Task import Task 
from PartitionedScheduler import PartitionedScheduler
from GlobalScheduler import GlobalScheduler
from HybridScheduler import HybridScheduler
import Visualizer

def run_experiment():
    # --- CONFIGURATION ---
    NUM_CORES = 4
    SIMULATION_DURATION = 1000
    

    MIGRATION_PENALTY = 1  
    NUM_CLUSTERS = 2
    
    print(f"--- STARTING SIMULATION ---")
    print(f"Penalty for Migration: {MIGRATION_PENALTY} ticks")
    
 

    tasks = [
        Task(1, execution_time=26, period=50, deadline=60), 
        Task(2, execution_time=26, period=50, deadline=60), 
        Task(3, execution_time=26, period=50, deadline=60), 
        Task(4, execution_time=26, period=50, deadline=60), 
        Task(5, execution_time=26, period=50, deadline=60), 
    ]
    
    print(f"\n[Hybrid-Optimized Workload]")
    for t in tasks:
        print(f"  {t}")
    print("-" * 30)

    # ==========================================
    # STRATEGY 1: PARTITIONED EDF
    # ==========================================
    print("\nRunning Strategy 1: PARTITIONED EDF...")
    part_scheduler = PartitionedScheduler(NUM_CORES)
    part_scheduler.partition_tasks(tasks)
    res_part = part_scheduler.run_simulation(tasks, SIMULATION_DURATION)
    print_results(res_part)

    # ==========================================
    # STRATEGY 2: GLOBAL EDF
    # ==========================================
    print("\nRunning Strategy 2: GLOBAL EDF...")
    global_scheduler = GlobalScheduler(NUM_CORES, migration_penalty=MIGRATION_PENALTY)
    res_global = global_scheduler.run_simulation(tasks, SIMULATION_DURATION)
    print_results(res_global)

    # ==========================================
    # STRATEGY 3: HYBRID (CLUSTERED) EDF
    # ==========================================
    print("\nRunning Strategy 3: HYBRID EDF (Clusters)...")
    hybrid_scheduler = HybridScheduler(NUM_CORES, NUM_CLUSTERS, migration_penalty=MIGRATION_PENALTY)
    hybrid_scheduler.partition_tasks(tasks)
    res_hybrid = hybrid_scheduler.run_simulation(tasks, SIMULATION_DURATION)
    print_results(res_hybrid)

    # ==========================================
    # VISUALIZATION STEP
    # ==========================================
    print("\nGenerating Charts...")
    Visualizer.plot_comparison(res_part, res_global, res_hybrid)
    Visualizer.plot_timeline(SIMULATION_DURATION, res_global['history'], res_hybrid['history'])
    Visualizer.plot_utilization_heatmap(part_scheduler.cores, global_scheduler.cores, hybrid_scheduler.cores, SIMULATION_DURATION)


    
    # 1. The Original Bar Chart (Totals)
    Visualizer.plot_comparison(res_part, res_global, res_hybrid)

    # 2. The Line Graph (Performance over Time)
    Visualizer.plot_timeline(
        SIMULATION_DURATION, 
        res_global['history'], 
        res_hybrid['history']
    )
    
    # 3. [NEW] The Heatmap (Core Load Balancing)
    # We pass the scheduler objects' internal core lists directly to the visualizer
    Visualizer.plot_utilization_heatmap(
        part_scheduler.cores, 
        global_scheduler.cores, 
        hybrid_scheduler.cores, 
        SIMULATION_DURATION
    )

def print_results(results):
    print(f"  -> Strategy: {results['strategy']}")
    print(f"  -> Failed Assignments (Offline): {results['failed_assignments']}")
    print(f"  -> Total Migrations (Runtime):   {results['migrations']}")
    print(f"  -> Missed Deadlines:             {results['missed_deadlines']}")

if __name__ == "__main__":
    run_experiment()