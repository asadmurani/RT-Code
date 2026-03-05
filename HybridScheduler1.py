from Core import Core
from Job import Job
import heapq

class HybridScheduler:
    def __init__(self, num_cores, num_clusters, migration_penalty=1):
        """
        :param num_clusters: How many groups to split the cores into.
                             e.g., 4 cores / 2 clusters = 2 cores per cluster.
        """
        self.num_cores = num_cores
        self.num_clusters = num_clusters
        self.cores_per_cluster = num_cores // num_clusters
        self.migration_penalty = migration_penalty
        
        # Create Hardware
        self.cores = [Core(i) for i in range(num_cores)]
        
        # Cluster structures
        # self.clusters[k] holds the list of core objects for cluster k
        self.clusters = []
        for i in range(num_clusters):
            start_index = i * self.cores_per_cluster
            end_index = start_index + self.cores_per_cluster
            self.clusters.append(self.cores[start_index:end_index])
            
        # Priority Queues (One per cluster)
        self.cluster_queues = [[] for _ in range(num_clusters)]
        
        # Map: task_id -> cluster_index
        self.task_cluster_map = {}
        self.failed_assignments = []
        
        # Migration tracking: job_id -> last_core_id
        self.job_location_tracker = {}

    def partition_tasks(self, tasks):
        """
        OFFLINE PHASE: Cluster-level Bin Packing.
        Instead of fitting tasks into 1 core (capacity 1.0),
        we fit them into a cluster (capacity = cores_per_cluster * 1.0).
        """
        sorted_tasks = sorted(tasks, key=lambda t: t.utilization, reverse=True)
        
        # Track utilization of each CLUSTER
        cluster_utilizations = [0.0] * self.num_clusters
        cluster_capacity = self.cores_per_cluster * 1.0 # e.g., 2.0 for dual-core cluster
        
        for task in sorted_tasks:
            assigned = False
            for c_idx in range(self.num_clusters):
                # Heuristic: Can the task fit in this cluster?
                # Note: In strict Real-Time theory, the bound is more complex, 
                # but for this simulation, Sum(U) <= m is the necessary condition.
                if cluster_utilizations[c_idx] + task.utilization <= cluster_capacity:
                    self.task_cluster_map[task.task_id] = c_idx
                    cluster_utilizations[c_idx] += task.utilization
                    assigned = True
                    break
            
            if not assigned:
                self.failed_assignments.append(task)
                print(f"[Hybrid] Task {task.task_id} (U={task.utilization:.2f}) rejected. Cluster Cap={cluster_capacity}")

    def run_simulation(self, tasks, max_time):
        """
        RUNTIME PHASE: Global EDF *within* each cluster.
        """
        current_time = 0
        total_migrations = 0
        missed_deadlines = 0

        # NEW: List to store cumulative migrations
        migration_history = []
        
        while current_time < max_time:
            # 1. Check Task Arrivals
            for task in tasks:
                if task.task_id not in self.task_cluster_map:
                    continue # Rejected task
                    
                if current_time % task.period == 0:
                    new_job = Job(task, current_time)
                    c_idx = self.task_cluster_map[task.task_id]
                    heapq.heappush(self.cluster_queues[c_idx], new_job)

            # 2. Schedule Each Cluster Independently
            for c_idx in range(self.num_clusters):
                cluster_cores = self.clusters[c_idx]
                queue = self.cluster_queues[c_idx]
                
                # --- Global EDF Logic (Scoped to this Cluster) ---
                
                # Gather runnable jobs (Queue + Currently Running on these cores)
                ready_jobs = []
                
                while queue:
                    ready_jobs.append(heapq.heappop(queue))
                    
                for core in cluster_cores:
                    if core.current_job:
                        ready_jobs.append(core.current_job)
                        core.current_job = None
                
                # Sort by Deadline
                heapq.heapify(ready_jobs)
                
                # Assign to Cores in this Cluster
                for core in cluster_cores:
                    if not ready_jobs:
                        break
                    
                    job = heapq.heappop(ready_jobs)
                    
                    # Migration Check (Restricted to within cluster)
                    last_core = self.job_location_tracker.get(job.id)
                    if last_core is not None and last_core != core.core_id:
                        total_migrations += 1
                        job.remaining_time += self.migration_penalty
                    
                    self.job_location_tracker[job.id] = core.core_id
                    core.assign_job(job)
                
                # Return unassigned jobs to queue
                while ready_jobs:
                    heapq.heappush(queue, ready_jobs.pop())

            # 3. Execute Ticks (Across all hardware)
            for core in self.cores:
                completed_job = core.execute_tick(current_time)
                if completed_job:
                     if completed_job.id in self.job_location_tracker:
                        del self.job_location_tracker[completed_job.id]
                
                if core.current_job and current_time > core.current_job.absolute_deadline:
                    missed_deadlines += 1

            current_time += 1
            
        return {
            "strategy": f"Hybrid EDF ({self.num_clusters} Clusters)",
            "failed_assignments": len(self.failed_assignments),
            "migrations": total_migrations,
            "missed_deadlines": missed_deadlines,
            "history": migration_history # <--- RETURN THE NEW LIST
        }