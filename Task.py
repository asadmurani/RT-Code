class Task:
    def __init__(self, task_id, execution_time, period, deadline=None):
        """
        Represents a Periodic Real-Time Task.
        
        :param task_id: Unique identifier for the task (tau_i)
        :param execution_time: (C_i) The worst-case execution time (WCET)
        :param period: (T_i) The time interval between job releases
        :param deadline: (D_i) Relative deadline. If None, assumes implicit deadline (D_i = T_i)
        """
        self.task_id = task_id
        self.execution_time = execution_time  # C_i
        self.period = period                  # T_i
        self.deadline = deadline if deadline else period # D_i
        
        # Calculated Property: Utilization (U_i = C_i / T_i)
        self.utilization = self.execution_time / self.period

    def __repr__(self):
        return f"Task(ID={self.task_id}, C={self.execution_time}, T={self.period}, U={self.utilization:.2f})"