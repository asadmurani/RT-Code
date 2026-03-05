from Core import Core
from Job import Job
import heapq

class GlobalScheduler:
    def __init__(self, num_cores, migration_penalty=1):
        """
        :param num_cores: Number of processors
        :param migration_penalty: Time penalty (in ticks) added when a job moves cores.
                                  This simulates cache invalidation and lock contention.
        """
        self.num_cores = num_cores
        self.migration_penalty = migration_penalty
        self.cores = [Core(i) for i in range(num_cores)]
        
        # Single Global Priority Queue (The critical architectural difference)
        self.global_queue = [] 
        
        # We need to track where a job ran last to detect migration
        # Map: job_unique_id -> last_core_id
        self.job_location_tracker = {} 

    def run_simulation(self, tasks, max_time):
        current_time = 0
        total_migrations = 0
        missed_deadlines = 0
        # NEW: List to store migration count at every single tick
        migration_history = []
        
        while current_time < max_time:
            # 1. Check Task Arrivals
            for task in tasks:
                if current_time % task.period == 0:
                    new_job = Job(task, current_time)
                    heapq.heappush(self.global_queue, new_job)

            # 2. Assign Jobs to Cores (Global EDF Logic)
            # In Global EDF, m cores pick the m highest priority jobs.
            
            # First, update currently running jobs
            # If a job finished in the last tick, the core is now free.
            # If it's not finished, it stays on the core UNLESS a higher priority job pre-empts it.
            # (For simplicity in this simulation, we assume non-preemptive for the running tick, 
            # but we re-evaluate assignment every tick).
            
            # Gather all available cores (those not busy or those willing to switch)
            # In a discrete step sim, it's easier to collect all active jobs + queue, 
            # sort them, and redistribute.
            
            # A. Collect all runnable jobs (from queue + currently on cores)
            all_ready_jobs = []
            
            # Pull from queue
            while self.global_queue:
                all_ready_jobs.append(heapq.heappop(self.global_queue))
                
            # Pull from cores (preemption logic)
            for core in self.cores:
                if core.current_job:
                    all_ready_jobs.append(core.current_job)
                    core.current_job = None # Temporarily remove to re-evaluate priority
            
            # B. Sort by Deadline (EDF)
            heapq.heapify(all_ready_jobs)
            
            # C. Assign top m jobs to m cores
            # We want to keep jobs on the same core if possible to avoid migration,
            # BUT Global EDF is greedy: it just picks the best available core.
            
            # We iterate through cores. In a real OS, there's a lock here (High Overhead).
            for core in self.cores:
                if not all_ready_jobs:
                    break # No more work
                
                # Pick highest priority job
                job = heapq.heappop(all_ready_jobs)
                
                # --- CRITICAL: MIGRATION CHECK ---
                # Check if this job ran somewhere else previously
                last_core = self.job_location_tracker.get(job.id)
                
                if last_core is not None and last_core != core.core_id:
                    # MIGRATION DETECTED
                    total_migrations += 1
                    # Apply Penalty: The job effectively "pauses" to reload cache
                    # We model this by adding to its required execution time
                    job.remaining_time += self.migration_penalty
                    # Optional: Log it
                    # print(f"Time {current_time}: Job {job.id} migrated Core {last_core} -> {core.core_id}")
                
                # Update tracker
                self.job_location_tracker[job.id] = core.core_id
                
                # Assign to core
                core.assign_job(job)
                
            # D. Put unassigned jobs back in the global queue
            while all_ready_jobs:
                heapq.heappush(self.global_queue, all_ready_jobs.pop())

            # 3. Execute Ticks
            for core in self.cores:
                completed_job = core.execute_tick(current_time)
                
                if completed_job:
                    # Job done, remove from tracker to save memory (optional)
                    if completed_job.id in self.job_location_tracker:
                        del self.job_location_tracker[completed_job.id]
                
                # Check active deadlines (for jobs currently running or in queue)
                # (Simplified check: usually done on job completion or periodically)
                if core.current_job and current_time > core.current_job.absolute_deadline:
                     missed_deadlines += 1
                     # print(f"Deadline Missed: Job {core.current_job.id}")

            # NEW: Record the current total at the end of every tick
            migration_history.append(total_migrations)
            current_time += 1

        return {
            "strategy": "Global EDF",
            "failed_assignments": 0, # Global accepts everything initially
            "migrations": total_migrations,
            "missed_deadlines": missed_deadlines,
            "history": migration_history # <--- RETURN THIS
        }