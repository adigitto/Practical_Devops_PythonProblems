'''
Problem 2: Find a safe service deployment order
Level -- Difficult!
Your deployment tool must deploy services after their dependencies. Given a dictionary of services and their dependencies, return a valid deployment order.
def deployment_order(dependencies):
    ...
Example
dependencies = {
    "frontend": ["api"],
    "api": ["database", "cache"],
    "worker": ["database"],
    "database": [],
    "cache": [],
}
One valid result:
["database", "cache", "api", "worker", "frontend"]
database must appear before both api and worker. cache must appear before api, and api before frontend.
Rules
- Every service appears as a dictionary key, including services with no dependencies.
- Dependency lists contain no duplicates.
- Return every service exactly once.
- If several orders are valid, return any of them.
- If dependencies contain a cycle, return None.
- For an empty dictionary, return [].
- Assume valid strings and that every referenced dependency exists.
Cycle example
dependencies = {
    "api": ["worker"],
    "worker": ["api"],
}
Expected:
None
Neither service can deploy first because each waits for the other.
Aim for an approach that handles thousands of services without repeatedly scanning the entire dictionary.
'''

"""
Approach - Use a queue, a dictionary of remaining dependency counts, and a reverse mapping that tells you which services become closer to ready after each deployment.
"""

from collections import deque

def deployment_order(dependencies):
    remaining = {
        service: len(required)
        for service, required in dependencies.items()
    }

    dependents = {service: [] for service in dependencies}

    for service, required in dependencies.items():
        for dependency in required:
            dependents[dependency].append(service)

    ready = deque(
        service
        for service, count in remaining.items()
        if count == 0
    )

    order = []

    while ready:
        service = ready.popleft()
        order.append(service)

        for dependent in dependents[service]:
            remaining[dependent] -= 1

            if remaining[dependent] == 0:
                ready.append(dependent)

    if len(order) != len(dependencies):
        return None

    return order