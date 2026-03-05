from Core import Core
from Job import Job
import heapq

class HybridScheduler:
    def __init__(self, num_cores, num_clusters, migration_penalty=1):
        self.num_cores = num_cores
        self.num_clusters = num_clusters
        self.cores_per_cluster = num_cores // num_clusters
        self.migration_penalty = migration_penalty
        
        self.cores = [Core(i) for i in range(num_cores)]
        
        self.clusters = []
        for i in range(num_clusters):
            start_index = i * self.cores_per_cluster
            end_index = start_index + self.cores_per_cluster
            self.clusters.append(self.cores[start_index:end_index])
            
        self.cluster_queues = [[] for _ in range(num_clusters)]
        self.task_cluster_map = {}
        self.failed_assignments = []
        self.job_location_tracker = {}

    def partition_tasks(self, tasks):
        sorted_tasks = sorted(tasks, key=lambda t: t.utilization, reverse=True)
        cluster_utilizations = [0.0] * self.num_clusters
        cluster_capacity = self.cores_per_cluster * 1.0 
        
        for task in sorted_tasks:
            assigned = False
            for c_idx in range(self.num_clusters):
                if cluster_utilizations[c_idx] + task.utilization <= cluster_capacity:
                    self.task_cluster_map[task.task_id] = c_idx
                    cluster_utilizations[c_idx] += task.utilization
                    assigned = True
                    break
            if not assigned:
                self.failed_assignments.append(task)

    def run_simulation(self, tasks, max_time):
        current_time = 0
        total_migrations = 0
        missed_deadlines = 0
        
        migration_history = []
        
        while current_time < max_time:
            # 1. Check Arrivals
            for task in tasks:
                if task.task_id not in self.task_cluster_map:
                    continue 
                if current_time % task.period == 0:
                    new_job = Job(task, current_time)
                    c_idx = self.task_cluster_map[task.task_id]
                    heapq.heappush(self.cluster_queues[c_idx], new_job)

            # 2. Schedule Clusters
            for c_idx in range(self.num_clusters):
                cluster_cores = self.clusters[c_idx]
                queue = self.cluster_queues[c_idx]
                
                ready_jobs = []
                while queue:
                    ready_jobs.append(heapq.heappop(queue))
                for core in cluster_cores:
                    if core.current_job:
                        ready_jobs.append(core.current_job)
                        core.current_job = None
                
                heapq.heapify(ready_jobs)
                
                for core in cluster_cores:
                    if not ready_jobs:
                        break
                    job = heapq.heappop(ready_jobs)
                    
                    last_core = self.job_location_tracker.get(job.id)
                    if last_core is not None and last_core != core.core_id:
                        total_migrations += 1
                        job.remaining_time += self.migration_penalty
                    
                    self.job_location_tracker[job.id] = core.core_id
                    core.assign_job(job)
                
                while ready_jobs:
                    heapq.heappush(queue, ready_jobs.pop())

            # 3. Execute
            for core in self.cores:
                completed_job = core.execute_tick(current_time)
                if completed_job:
                     if completed_job.id in self.job_location_tracker:
                        del self.job_location_tracker[completed_job.id]
                if core.current_job and current_time > core.current_job.absolute_deadline:
                    missed_deadlines += 1

            # CRITICAL: Append history here
            migration_history.append(total_migrations)
            current_time += 1
            
        return {
            "strategy": f"Hybrid EDF ({self.num_clusters} Clusters)",
            "failed_assignments": len(self.failed_assignments),
            "migrations": total_migrations,
            "missed_deadlines": missed_deadlines,
            "history": migration_history
        }