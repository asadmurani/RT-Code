import random
from typing import List
from Task import Task

class TaskSetGenerator:
    def __init__(self):
        self.task_counter = 1

    def generate_task_set(self, target_utilization, num_tasks, min_period=10, max_period=100) -> List[Task]:
        """
        Generates a set of tasks with a specific total utilization.
        
        :param target_utilization: Total U_sys to aim for (e.g., 2.8 for a 4-core system)
        :param num_tasks: Number of tasks to generate
        :return: A list of Task objects
        """
        tasks = []
        self.task_counter = 1
        
        # We use a simplified UUniFast-like approach: 
        # Divide total utilization into random chunks
        utilizations = self._generate_uunifast_utilizations(target_utilization, num_tasks)
        
        for u in utilizations:
            # 1. Randomly pick a period (T_i)
            period = random.randint(min_period, max_period)
            
            # 2. Calculate execution time (C_i = U_i * T_i)
            # We must ensure execution_time is an integer for discrete simulation
            execution_time = int(round(u * period))
            
            # Safety: Execution time must be at least 1, and cannot exceed period
            execution_time = max(1, execution_time)
            if execution_time > period:
                execution_time = period
            
            # Create the task
            new_task = Task(self.task_counter, execution_time, period)
            tasks.append(new_task)
            self.task_counter += 1
            
        return tasks

    def _generate_uunifast_utilizations(self, total_u, n):
        """
        Helper: Distributes total utilization 'total_u' across 'n' tasks randomly.
        This is a simplified version suitable for the project scope.
        """
        # Generate n random numbers
        random_values = [random.random() for _ in range(n)]
        sum_v = sum(random_values)
        
        # Normalize them to sum up to total_u
        utilizations = [(r / sum_v) * total_u for r in random_values]
        return utilizations

# --- QUICK TEST BLOCK ---
if __name__ == "__main__":
    generator = TaskSetGenerator()
    # Generate a "Heavy" load: 3 tasks taking up 90% of a single core (U=0.9)
    # This forces big C_i values relative to T_i
    heavy_tasks = generator.generate_task_set(target_utilization=0.9, num_tasks=3)
    
    print("Generated Task Set:")
    for t in heavy_tasks:
        print(t)