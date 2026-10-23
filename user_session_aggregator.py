'''
Social Media Company wants to understand how users interact with the platform during individual browsing sessions.
You are given a list of user activity events. Each event contains:
- user_id: Unique user identifier.
- timestamp: Unix timestamp in seconds.
- event_type: Type of activity (view, click, or save).

A session is a sequence of events belonging to the same user where the time gap between consecutive events is at most 30 minutes (1,800 seconds).
Your task is to implement a function that groups events into sessions and calculates engagement metrics for each session.

Requirements
1. Group events by user using their user_id.
2. Sort events by timestamp because input events may arrive out of order.
3. Identify sessions: Start a new session when the gap between consecutive events exceeds 1,800 seconds.
4. Calculate session metrics:
   - start_time: Timestamp of first event.
   - end_time: Timestamp of last event.
   - event_count: Total number of events in the session.
   - unique_event_types: Number of distinct event types in the session.

5. Validate input: Ignore records with missing fields, invalid types, unknown event types, or negative timestamps. User IDs must be nonempty strings, and timestamps must be integers (excluding booleans).

6. Return sessions sorted by user_id ascending, then start_time ascending.
Events occurring at the same timestamp are all counted.

Example input
events = [    
{"user_id": "u1", "timestamp": 100,  "event_type": "view"},    {"user_id": "u2", "timestamp": 200,  "event_type": "click"},    {"user_id": "u1", "timestamp": 500,  "event_type": "save"},    {"user_id": "u1", "timestamp": 2500, "event_type": "view"},    {"user_id": "u2", "timestamp": 800,  "event_type": "save"},    {"user_id": "u1", "timestamp": 2600, "event_type": "click"},    {"user_id": "u2", "timestamp": 3000, "event_type": "view"},    {"user_id": "u1", "timestamp": 400,  "event_type": "click"}
]

Expected output
[    
{        "user_id": "u1",        "start_time": 100,        "end_time": 500,        "event_count": 3,        "unique_event_types": 3    },    
{        "user_id": "u1",        "start_time": 2500,        "end_time": 2600,        "event_count": 2,        "unique_event_types": 2    },    
{        "user_id": "u2",        "start_time": 200,        "end_time": 800,        "event_count": 2,        "unique_event_types": 2    },    
{        "user_id": "u2",        "start_time": 3000,        "end_time": 3000,        "event_count": 1,        "unique_event_types": 1    }]


Important clarification
For user u1, events at timestamps 100, 400, and 500 belong to one session. The next event at 2500 starts a new session because the gap from 500 is 2,000 seconds, exceeding the 1,800-second threshold.
For user u2, the gap between timestamps 800 and 3000 is 2,200 seconds, so a new session begins.
'''

"""
My approach
Read the events into json format, then run for loop to read events
- store {user: eventcount} map | Actually thinking of using a custom map {user: {ev_count:1,start:"", end:"", unique_event_types:""}} 
- The composite dict should get added to the result_list when timestamp exceeds 1800secs from the last event

"""
import json
from collections import defaultdict
import pytest

def analyze_sessions(events):
    data = json.loads(events)

    # Group valid events by user
    user_map = defaultdict(list)

    # Supported event types
    valid_types = {"view", "click", "save"}

    for item in data:
        uid = item.get("user_id")
        ts = item.get("timestamp")
        event_type = item.get("event_type")

        if not isinstance(uid, str) or not uid.strip():
            continue
        if type(ts) is not int or ts < 0:
            continue
        if event_type not in valid_types if isinstance(event_type, str) else True:
            continue

        # Store timestamp and event type for the user
        user_map[uid].append((ts, event_type))

    # Store all completed sessions
    result = []
    
    # Step 2: Process users in sorted order
    for uid in sorted(user_map):                #sorts by UID asc
        user_events = sorted(user_map[uid])     #just gets the sorted user events
        # Initialize the first session
        start = user_events[0][0]
        end = start
        count = 0
        unique_types = set()

        # Step 3: Traverse the user's events
        for ts, event_type in user_events:
            # Start a new session if inactivity exceeds 30 min
            if ts - end > 1800:
                # Save the completed session
                result.append({
                    "user_id": uid,
                    "start_time": start,
                    "end_time": end,
                    "event_count": count,
                    "unique_event_types": len(unique_types)
                })

                # Reset metrics for the new session
                start = ts
                count = 0
                unique_types = set()

            # Update the current session
            end = ts
            count += 1
            unique_types.add(event_type)

        # Step 4: Save the last session for this user
        result.append({
            "user_id": uid,
            "start_time": start,
            "end_time": end,
            "event_count": count,
            "unique_event_types": len(unique_types)
        })

    return result

####### Test Cases: #######
def happy_path_test():
    events = """ [{"user_id": "u1", "timestamp": 100,  "event_type": "view"},    {"user_id": "u2", "timestamp": 200,  "event_type": "click"},    {"user_id": "u1", "timestamp": 500,  "event_type": "save"},    {"user_id": "u1", "timestamp": 2500, "event_type": "view"},    {"user_id": "u2", "timestamp": 800,  "event_type": "save"},    {"user_id": "u1", "timestamp": 2600, "event_type": "click"},    {"user_id": "u2", "timestamp": 3000, "event_type": "view"},    {"user_id": "u1", "timestamp": 400,  "event_type": "click"}]"""

    expected_result = [{        "user_id": "u1",        "start_time": 100,        "end_time": 500,        "event_count": 3,        "unique_event_types": 3    },{        "user_id": "u1",        "start_time": 2500,        "end_time": 2600,        "event_count": 2,        "unique_event_types": 2    },    {        "user_id": "u2",        "start_time": 200,        "end_time": 800,        "event_count": 2,        "unique_event_types": 2    },{        "user_id": "u2",        "start_time": 3000,        "end_time": 3000,        "event_count": 1,        "unique_event_types": 1    }]

    result = analyze_sessions(events) 
    assert expected_result == result

def session_split_test():
    events = """[{"user_id": "u1", "timestamp": 100,  "event_type": "view"},{"user_id": "u1", "timestamp": 2000,  "event_type": "view"}]"""
    result = analyze_sessions(events)
    print(result)
    assert len(result) == 2
    assert result[0] == {"user_id": "u1", "start_time": 100, "end_time": 100, "event_count": 1, "unique_event_types": 1}
    assert result[1] == {"user_id": "u1", "start_time": 2000, "end_time": 2000, "event_count": 1, "unique_event_types": 1}


##### CODE RUN #####
events = """ [{"user_id": "u1", "timestamp": 100,  "event_type": "view"},    {"user_id": "u2", "timestamp": 200,  "event_type": "click"},    {"user_id": "u1", "timestamp": 500,  "event_type": "save"},    {"user_id": "u1", "timestamp": 2500, "event_type": "view"},    {"user_id": "u2", "timestamp": 800,  "event_type": "save"},    {"user_id": "u1", "timestamp": 2600, "event_type": "click"},    {"user_id": "u2", "timestamp": 3000, "event_type": "view"},    {"user_id": "u1", "timestamp": 400,  "event_type": "click"}]"""

res = analyze_sessions(events)
for i in res:
    print(i)

#### TEST CASE RUN
happy_path_test()
session_split_test()