class Job:
    def __init__(self, task, release_time):
        """
        Represents a specific instance of a Task (a 'Job').
        
        :param task: The Task object this job belongs to
        :param release_time: The specific time (t) this job became ready to run
        """
        self.task = task
        self.id = task.task_id  # Matches Task ID
        self.release_time = release_time
        
        # Absolute Deadline = Release Time + Relative Deadline
        self.absolute_deadline = release_time + task.deadline
        
        # Initially, remaining execution time is the full WCET
        self.remaining_time = task.execution_time
        
        # Metrics for the report
        self.start_time = None
        self.completion_time = None

    def execute(self, time_step=1):
        """
        Simulates running this job for a specific time step.
        Reduces remaining execution time.
        """
        if self.start_time is None:
            # We will set this externally, but good to track logic here or in Core
            pass
            
        self.remaining_time -= time_step
        
    def is_complete(self):
        return self.remaining_time <= 0

    def __lt__(self, other):
        """
        Comparators for Priority Queue (EDF Logic).
        Returns True if self has an earlier deadline than other.
        If deadlines are equal, use Task ID as tie-breaker (fixed priority tie-breaking).
        """
        if self.absolute_deadline == other.absolute_deadline:
            return self.id < other.id
        return self.absolute_deadline < other.absolute_deadline

    def __repr__(self):
        return f"Job(T{self.id}, Rem={self.remaining_time}, DL={self.absolute_deadline})"