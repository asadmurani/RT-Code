from Core import Core
from Job import Job
import heapq

class GlobalScheduler:
    def __init__(self, num_cores, migration_penalty=1):
        self.num_cores = num_cores
        self.migration_penalty = migration_penalty
        self.cores = [Core(i) for i in range(num_cores)]
        self.global_queue = [] 
        self.job_location_tracker = {} 

    def run_simulation(self, tasks, max_time):
        current_time = 0
        total_migrations = 0
        missed_deadlines = 0
        
        # This list tracks migration count at every tick for the graph
        migration_history = [] 
        
        while current_time < max_time:
            # 1. Check Task Arrivals
            for task in tasks:
                if current_time % task.period == 0:
                    new_job = Job(task, current_time)
                    heapq.heappush(self.global_queue, new_job)

            # 2. Global Scheduling Logic
            all_ready_jobs = []
            while self.global_queue:
                all_ready_jobs.append(heapq.heappop(self.global_queue))
            
            for core in self.cores:
                if core.current_job:
                    all_ready_jobs.append(core.current_job)
                    core.current_job = None 
            
            heapq.heapify(all_ready_jobs)
            
            for core in self.cores:
                if not all_ready_jobs:
                    break 
                
                job = heapq.heappop(all_ready_jobs)
                
                # Check Migration
                last_core = self.job_location_tracker.get(job.id)
                if last_core is not None and last_core != core.core_id:
                    total_migrations += 1
                    job.remaining_time += self.migration_penalty
                
                self.job_location_tracker[job.id] = core.core_id
                core.assign_job(job)
                
            while all_ready_jobs:
                heapq.heappush(self.global_queue, all_ready_jobs.pop())

            # 3. Execute Ticks
            for core in self.cores:
                completed_job = core.execute_tick(current_time)
                if completed_job:
                    if completed_job.id in self.job_location_tracker:
                        del self.job_location_tracker[completed_job.id]
                
                if core.current_job and current_time > core.current_job.absolute_deadline:
                     missed_deadlines += 1

            # CRITICAL: Append to history INSIDE the loop
            migration_history.append(total_migrations)
            current_time += 1

        return {
            "strategy": "Global EDF",
            "failed_assignments": 0,
            "migrations": total_migrations,
            "missed_deadlines": missed_deadlines,
            "history": migration_history
        }