'''
Problem 1: Detect a burst of failed requests
You’re building an alerting tool that processes request logs. Each record contains:
(timestamp, service, status_code)
Implement:
def detect_error_bursts(logs, window_seconds, threshold):
    ...
Return a list of (timestamp, service) alerts whenever a service has at least threshold failed requests within the trailing time window.
Rules
- Logs arrive in nondecreasing timestamp order. Timestamps are integer seconds.
- A status code from 500 through 599 counts as a failure.
- At timestamp t, the window includes failures where:t - window_seconds < failure_timestamp <= t
- Evaluate alerts only when processing a failed request.
- Emit an alert for each failed request that brings or keeps its service’s count at or above the threshold.
- Services are tracked independently.
- Preserve processing order in the returned alerts.
- Assume valid records and positive window_seconds and threshold.
- The input may contain up to one million records.
Example
logs = [
    (1,  "api",    500),
    (2,  "worker", 503),
    (3,  "api",    502),
    (4,  "api",    200),
    (5,  "api",    503),
    (6,  "api",    500),
    (12, "api",    502),
]

detect_error_bursts(logs, window_seconds=5, threshold=3)
Expected result:
[(5, "api"), (6, "api")]
At time 5, the API failures at 1, 3, and 5 count. At time 6, the failure at 1 expires, but those at 3, 5, and 6 count.
'''
"""
My approach -- Create a dictionary storing service: deque(<timestamps>). eg: {"api":deque(1,3,5)}. Will get threshold by calculating deque length and use poplefts for removing expired timestamp

Thus, main datastructure needed for this -- deque
"""

from collections import defaultdict, deque

from collections import defaultdict, deque

def detect_error_bursts(logs, window_seconds, threshold):
    freq_map = defaultdict(deque)
    alerts = []

    for timestamp, service, status_code in logs:
        if not 500 <= status_code <= 599:
            continue

        recent = freq_map[service]  #initiates {api: <deque>}
        cutoff = timestamp - window_seconds

        while recent and recent[0] <= cutoff:  #checks q exists and first element is less than cutoff
            recent.popleft()

        recent.append(timestamp)

        if len(recent) >= threshold:
            alerts.append((timestamp, service))

    return alerts

logs = [
    (1,  "api",    500),
    (2,  "worker", 503),
    (3,  "api",    502),
    (4,  "api",    200),
    (5,  "api",    503),
    (6,  "api",    500),
    (12, "api",    502),
]

print(detect_error_bursts(logs, 5, 3, 10))