from Core import Core
from Job import Job
import heapq  # We use Python's heap queue algorithm for the priority queue

class PartitionedScheduler:
    def __init__(self, num_cores):
        self.num_cores = num_cores
        # Create the hardware
        self.cores = [Core(i) for i in range(num_cores)]
        
        # Core-specific queues: list of (Job) heaps
        # core_queues[0] is the priority queue for Core 0
        self.core_queues = [[] for _ in range(num_cores)]
        
        # Tracking metrics
        self.failed_assignments = []  # Stores tasks that couldn't fit
        self.assigned_tasks = {}      # Map: task_id -> core_id

    def partition_tasks(self, tasks):
        """
        OFFLINE PHASE: Bin-Packing Heuristic (First-Fit Decreasing).
        
        Strategy:
        1. Sort tasks by utilization (Largest first) - 'Decreasing' part.
           This is a standard strategy to minimize fragmentation, but we will 
           see that it still fails for heavy tasks.
        2. Try to fit the task into the first core where utilization <= 1.0.
        """
        # Sort tasks by utilization descending (heaviest tasks first)
        sorted_tasks = sorted(tasks, key=lambda t: t.utilization, reverse=True)
        
        # Track current utilization of each core
        core_utilizations = [0.0] * self.num_cores
        
        for task in sorted_tasks:
            assigned = False
            for core_idx in range(self.num_cores):
                # Check if task fits (Total U <= 1.0 is the bound for EDF)
                if core_utilizations[core_idx] + task.utilization <= 1.0:
                    # Assign task
                    self.assigned_tasks[task.task_id] = core_idx
                    core_utilizations[core_idx] += task.utilization
                    assigned = True
                    break
            
            if not assigned:
                self.failed_assignments.append(task)
                print(f"[Partitioned] Task {task.task_id} (U={task.utilization:.2f}) rejected due to Fragmentation.")

    def run_simulation(self, tasks, max_time):
        """
        RUNTIME PHASE: Discrete Event Simulation.
        """
        current_time = 0
        total_migrations = 0 # Should be 0 for Partitioned (Metric Check)
        missed_deadlines = 0
        
        # Run time loop
        while current_time < max_time:
            # 1. Check Task Arrivals (Release Jobs)
            for task in tasks:
                # If task wasn't assigned (rejected offline), skip it
                if task.task_id not in self.assigned_tasks:
                    continue
                
                # Check if it's time for a new job instance (t % Period == 0)
                if current_time % task.period == 0:
                    new_job = Job(task, current_time)
                    core_id = self.assigned_tasks[task.task_id]
                    # Push to the specific core's local priority queue
                    heapq.heappush(self.core_queues[core_id], new_job)

            # 2. Execute 1 Tick on Every Core
            for core_idx, core in enumerate(self.cores):
                queue = self.core_queues[core_idx]
                
                # Check if there is a job to run
                if queue:
                    # Peek at the highest priority job (Earliest Deadline)
                    job = queue[0]
                    
                    # Check for Missed Deadline
                    if current_time > job.absolute_deadline:
                        missed_deadlines += 1
                        print(f"Time {current_time}: Deadline Missed on Core {core_idx} for Job {job.id}")
                        heapq.heappop(queue) # Drop the failed job
                        continue
                    
                    # Assign to core (context switch check could go here)
                    core.assign_job(job)
                    
                    # Execute
                    completed_job = core.execute_tick(current_time)
                    
                    # If job finished, remove from queue
                    if completed_job:
                        heapq.heappop(queue)
                        core.assign_job(None) # Core is free
                else:
                    # Nothing to do
                    core.execute_tick(current_time)

            current_time += 1
            
        return {
            "strategy": "Partitioned EDF",
            "failed_assignments": len(self.failed_assignments),
            "migrations": total_migrations, # Must be 0
            "missed_deadlines": missed_deadlines
        }