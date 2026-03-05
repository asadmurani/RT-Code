from Job import Job

class Core:
    def __init__(self, core_id):
        self.core_id = core_id
        self.current_job = None  # The Job currently running on this core
        self.idle_time = 0
        self.active_time = 0
        
        # History is useful for debugging specific schedules
        self.history = [] # List of (time, job_id) tuples

    def assign_job(self, job: Job):
        """
        Assigns a job to this core.
        """
        self.current_job = job

    def execute_tick(self, time):
        """
        Advances the simulation by 1 unit of time.
        """
        if self.current_job:
            # Work on the job
            self.current_job.execute(time_step=1)
            self.active_time += 1
            self.history.append((time, self.current_job.id))
            
            # Check completion
            if self.current_job.is_complete():
                self.current_job.completion_time = time + 1
                completed_job = self.current_job
                self.current_job = None
                return completed_job # Return it so Scheduler knows it's done
        else:
            # CPU is Idle
            self.idle_time += 1
            self.history.append((time, None))
            
        return None

    def __repr__(self):
        return f"Core({self.core_id}) - Job: {self.current_job}"