'''
Pinterest has a content-processing pipeline where users upload images (Pins). Each uploaded Pin must go through a series of processing tasks, such as image resizing, thumbnail generation, and content moderation.
Each task has a unique ID, a priority, and may depend on other tasks completing first.
Your job is to implement a task scheduler that determines the order in which tasks should execute.
Task structure
Each task is represented as a dictionary:
{    "task_id": "T1",    "priority": 3,    "dependencies": []}

- task_id: Unique string identifier.
- priority: Integer from 1 to 10, where 10 is highest priority.
- dependencies: List of task IDs that must complete before this task can execute.

Requirements
1. Respect dependencies: A task can execute only after all its dependencies have completed.
2. Prioritize ready tasks: Among tasks whose dependencies are satisfied, always execute the task with the highest priority.
3. Tie-breaking: If two ready tasks have the same priority, execute the task with the lexicographically smaller task_id first.
4. Detect circular dependencies: If tasks form a cycle, return an empty list.
5. Validate dependencies: If a task references a task ID that doesn't exist, return an empty list.
6. Return execution order: Return a list of task IDs in their scheduled order.

Assume task IDs are unique, priorities are valid integers from 1 to 10, and the input structure is otherwise valid. Dependencies may be listed more than once; duplicate dependency IDs should count as a single dependency.

Example 1 — Normal execution
tasks = [    {"task_id": "T1", "priority": 3, "dependencies": []},    {"task_id": "T2", "priority": 8, "dependencies": ["T1"]},    {"task_id": "T3", "priority": 5, "dependencies": []},    {"task_id": "T4", "priority": 9, "dependencies": ["T2", "T3"]},    {"task_id": "T5", "priority": 7, "dependencies": []}]

Expected output:
["T5", "T3", "T1", "T2", "T4"]

Example 2 — Circular dependency
tasks = [    {"task_id": "T1", "priority": 5, "dependencies": ["T2"]},    {"task_id": "T2", "priority": 8, "dependencies": ["T1"]}]
Expected output:
[]
'''

"""
Approach - This is a graph problem disguised as a practical scheduling problem!!
Use Kahn's Algorithm with a priority queue.
1. in_degree dictionary: Track how many unresolved dependencies each task has.
2. dependents dictionary: Track which tasks depend on a particular task.
3. priorities dictionary: Store the priority of each task.
4. Min heap: Add all tasks with zero dependencies. Store (-priority, task_id) to execute the highest-priority task first.
5. Process tasks: Pop the highest-priority ready task, add it to the result, and decrement the dependency count of its dependent tasks.
6. Unlock tasks: When a dependent task's count becomes zero, add it to the heap.
7. Detect cycles: If the number of executed tasks is smaller than the total number of tasks, return [].
"""


from collections import defaultdict
import heapq

def task_scheduler(task_list):

    # Store unresolved dependency counts
    in_degree = {}

    # Store tasks that depend on each task
    dependents = defaultdict(list)

    # Store task priorities
    priorities = {}

    # Min heap for ready tasks
    ready_tasks = []

    # Store final execution order
    result = []

    # Step 1: Initialize task information
    for task in task_list:
        task_id = task["task_id"]
        priority = task["priority"]

        # Remove duplicate dependencies
        dependencies = set(task["dependencies"])

        # Count unresolved dependencies
        in_degree[task_id] = len(dependencies)

        # Save priority
        priorities[task_id] = priority

        # Build reverse dependency mapping
        for dep in dependencies:
            dependents[dep].append(task_id)

    # Step 2: Validate dependency references
    for dep in dependents:
        if dep not in in_degree:
            return []

    # Step 3: Add tasks with zero dependencies
    for task_id, count in in_degree.items():
        if count == 0:
            heapq.heappush(
                ready_tasks,
                (-priorities[task_id], task_id)
            )

    # Step 4: Process tasks in priority order
    while ready_tasks:

        # Get highest-priority ready task
        priority, task_id = heapq.heappop(ready_tasks)

        # Mark task as executed
        result.append(task_id)

        # Update tasks that depend on this task
        for dependent in dependents[task_id]:

            # One dependency is now completed
            in_degree[dependent] -= 1

            # Task becomes ready when count reaches zero
            if in_degree[dependent] == 0:

                # Add newly ready task to heap
                heapq.heappush(
                    ready_tasks,
                    (-priorities[dependent], dependent)
                )

    # Step 5: Detect circular dependencies
    if len(result) != len(task_list):
        return []

    return result


# Test input
tasks = [
    {"task_id": "T1", "priority": 3, "dependencies": []},
    {"task_id": "T2", "priority": 8, "dependencies": ["T1"]},
    {"task_id": "T3", "priority": 5, "dependencies": []},
    {"task_id": "T4", "priority": 9, "dependencies": ["T2", "T3"]},
    {"task_id": "T5", "priority": 7, "dependencies": []}
]

print(task_scheduler(tasks))