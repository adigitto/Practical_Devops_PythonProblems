'''
Problem statement
A Social Media Company processes millions of API requests from users. To protect its backend services, the platform enforces rate limits.
Your task is to implement a rate limit violation detector that analyzes API request logs and identifies users who exceed the allowed request rate.
The system allows a maximum of 3 requests per user within any rolling 10-second window.

Input format
Each request is represented as a dictionary:
{ "user_id": "u1",    "timestamp": 12,    "endpoint": "/pins"}

The input is a list of request records, which may arrive out of chronological order.

Requirements
1. Group requests by user using a dictionary.
2. Validate input: Ignore records with missing fields, empty user IDs, invalid timestamps, or missing/empty endpoints. User IDs and endpoints must be nonempty strings. Timestamps must be nonnegative integers (excluding booleans).
3. Sort requests chronologically for each user.
4. Apply a rolling 10-second window: For a request at timestamp t, count requests whose timestamps fall within [t - 9, t], inclusive.
5. Detect violations: A violation occurs whenever the request count within the current window exceeds 3.
6. Return results: For each user who violated the limit, return the timestamp of their first violating request and the number of requests in that request's rolling window.
7. Sort the final results by user_id ascending.

All valid requests count, including requests to different endpoints and multiple requests at the same timestamp.

Example 1
requests = [    {"user_id": "u1", "timestamp": 1,  "endpoint": "/pins"},    
{"user_id": "u2", "timestamp": 2,  "endpoint": "/feed"},    
{"user_id": "u1", "timestamp": 4,  "endpoint": "/pins"},    
{"user_id": "u1", "timestamp": 7,  "endpoint": "/save"},    
{"user_id": "u2", "timestamp": 5,  "endpoint": "/feed"},    
{"user_id": "u1", "timestamp": 9,  "endpoint": "/pins"},   
{"user_id": "u1", "timestamp": 15, "endpoint": "/pins"},    
{"user_id": "u2", "timestamp": 8,  "endpoint": "/feed"},    
{"user_id": "u2", "timestamp": 20, "endpoint": "/feed"}]

Expected output:
[{"user_id": "u1",        "first_violation": 9,        "request_count": 4    }]

Explanation: User u1 has four requests at timestamps 1, 4, 7, and 9. All four fall within the window [0, 9], so the request at timestamp 9 is the first violation.
User u2 never exceeds three requests in any rolling 10-second window.

Example 2 — Window boundary
requests = [    {"user_id": "u1", "timestamp": 1,  "endpoint": "/pins"},    {"user_id": "u1", "timestamp": 2,  "endpoint": "/pins"},    {"user_id": "u1", "timestamp": 3,  "endpoint": "/pins"},    {"user_id": "u1", "timestamp": 11, "endpoint": "/pins"}]

Expected output:
[]
At timestamp 11, the window is [2, 11], so the request at timestamp 1 is no longer counted. There are only three requests.'''

"""
>>> Approach — Hash Map + "Deque (Sliding Window)"
1. Validate requests — Ignore records with missing or invalid user_id, timestamp, or endpoint.
2. Sort requests — Sort by (user_id, timestamp) so requests for each user are processed chronologically.
3. Maintain a dictionary — Map each user to a deque containing timestamps within the current 10-second window.
4. Remove expired requests — For each timestamp ts, remove timestamps less than ts - 9.
5. Detect violations — Append the current timestamp. If the deque contains more than 3 requests, record the violation.
6. Record only the first violation for each user.
7. Return results sorted by user ID.
"""

from collections import defaultdict, deque

def rolling_rate_limiter(requests):
    valid_requests = []
    
    # Step 1: Validate input records
    for req in requests:
        uid = req.get("user_id")
        ts = req.get("timestamp")
        endpoint = req.get("endpoint")

        if not isinstance(uid, str) or not uid.strip():
            continue

        # Validate timestamp (bool is not allowed)
        if type(ts) is not int or ts < 0:
            continue

        if not isinstance(endpoint, str) or not endpoint.strip():
            continue

        # Store validated request information
        valid_requests.append((uid, ts))
        
    # Step 2: Sort by user ID, then timestamp
    valid_requests.sort()       #sorts by first element then second element

    # Store rolling timestamps for each user
    user_windows = defaultdict(deque)

    # Track users who have already violated the limit
    violated_users = set()

    # Store first violation for each user
    result = []

    # Step 3: Process requests chronologically
    for uid, ts in valid_requests:
        # Skip users whose first violation is recorded
        if uid in violated_users:
            continue

        # Get the user's rolling window
        window = user_windows[uid]

        # Step 4: Remove requests outside the 10-second window
        while window and window[0] < ts - 9:
            window.popleft()

        # Add the current request
        window.append(ts)

        # Step 5: Check whether the limit is exceeded
        if len(window) > 3:

            # Record the first violation
            result.append({
                "user_id": uid,
                "first_violation": ts,
                "request_count": len(window)
            })

            # Prevent duplicate violation records
            violated_users.add(uid)

    # Requests were sorted by user ID
    return result
                

requests = [    {"user_id": "u1", "timestamp": 1,  "endpoint": "/pins"},    
{"user_id": "u2", "timestamp": 2,  "endpoint": "/feed"},    
{"user_id": "u1", "timestamp": 4,  "endpoint": "/pins"},    
{"user_id": "u1", "timestamp": 7,  "endpoint": "/save"},    
{"user_id": "u2", "timestamp": 5,  "endpoint": "/feed"},    
{"user_id": "u1", "timestamp": 9,  "endpoint": "/pins"},   
{"user_id": "u1", "timestamp": 15, "endpoint": "/pins"},    
{"user_id": "u2", "timestamp": 8,  "endpoint": "/feed"},    
{"user_id": "u2", "timestamp": 20, "endpoint": "/feed"}]

res = rolling_rate_limiter(requests)
print(res)
