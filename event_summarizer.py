"""
Asked in Series A startup interview
 * LIVE CODING — SUMMARIZING BENCHMARK RESULTS (no AI)
 * Background: we run benchmark scenarios against AI models. Each scenario
 * will run M times. We want to generate a summary of the events to display.

// An event looks like this:
// {
//   eventId: "e1",                 // unique per event
//   scenarioId: "s1",
//   attempt: 1,                    // which attempt this is, 1 to M
//   type: "completed" | "failed",  // "failed" = the attempt errored (e.g. a timeout)
//   score: 0.9,                    // 0 to 1, only on "completed" events
//   timestamp: 100,
// }

const M = 3;

/**
 * Return a summary for every scenario that appears in `events`:
 *
 *   {
 *     s1: { completed: 3, averageScore: 0.5, status: "done" },
 *     ...
 *   }
 *
 *   completed     number of completed attempts
 *   averageScore  mean score of the completed attempts, or null if none
 *   status        "done" once the scenario has M completed attempts,
 *                 otherwise "in_progress"
 *
 * For now, you can assume each (scenario, attempt) pair appears at most once.
 */
function summarize(events) {
  // your code here
}

const events = [
  { eventId: "e1", scenarioId: "s1", attempt: 1, type: "completed", score: 0.9, timestamp: 100 },
  { eventId: "e2", scenarioId: "s1", attempt: 2, type: "completed", score: 0.6, timestamp: 110 },
  { eventId: "e3", scenarioId: "s1", attempt: 3, type: "completed", score: 0.0, timestamp: 120 },
  { eventId: "e4", scenarioId: "s2", attempt: 1, type: "completed", score: 0.8, timestamp: 105 },
  { eventId: "e5", scenarioId: "s2", attempt: 2, type: "failed", timestamp: 115 },
  { eventId: "e6", scenarioId: "s3", attempt: 1, type: "failed", timestamp: 130 },
];

// Expected:
// {
//   s1: { completed: 3, averageScore: 0.5, status: "done" },
//   s2: { completed: 1, averageScore: 0.8, status: "in_progress" },
//   s3: { completed: 0, averageScore: null, status: "in_progress" },
// }

"""
from collections import defaultdict

def event_summarizer(events, M):
    #group events by scenario_id
    scenario_dict = defaultdict(list)
    return_dict = defaultdict()
    
    for event in events:
        scenario_dict[event["scenarioId"]].append(event)
    
    for scenario, evs in scenario_dict.items():
        total_score = 0
        average_score = 0
        status = "in-progress"
        completed_events = [e for e in evs if e["type"]=="completed"]
        completed_event_len = len(completed_events)

        #score calculation
        if completed_event_len > 0:
            for event in completed_events:
                total_score = total_score + event.get("score")
            average_score = total_score / completed_event_len
        else:
            average_score = "None"
        
        if completed_event_len >= M:
            status = "done"
        
        return_dict[scenario] = {
            "completed": completed_event_len,
            "averageScore": average_score,
            "status": status,
        }
    
    return return_dict

events = [
  {"eventId": "e1", "scenarioId": "s1", "attempt": 1, "type": "completed", "score": 0.9, "timestamp": 100},
  {"eventId": "e2", "scenarioId": "s1", "attempt": 2, "type": "completed", "score": 0.6, "timestamp": 110},
  {"eventId": "e3", "scenarioId": "s1", "attempt": 3, "type": "completed", "score": 0.0, "timestamp": 120},
  {"eventId": "e4", "scenarioId": "s2", "attempt": 1, "type": "completed", "score": 0.8, "timestamp": 105},
  {"eventId": "e5", "scenarioId": "s2", "attempt": 2, "type": "failed", "timestamp": 115},
  {"eventId": "e6", "scenarioId": "s3", "attempt": 1, "type": "failed", "timestamp": 130}
]


result = event_summarizer(events, 3)
for k,v in result.items():
    print(k,v)
